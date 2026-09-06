import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from torchvision import transforms
import cv2


def generate_gradcam(model, image, device):
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])

    input_tensor = transform(image.convert("RGB"))
    input_tensor = input_tensor.unsqueeze(0).to(device)
    input_tensor.requires_grad = True

    # ResNet18 ka last convolutional layer
    target_layer = model.layer4[-1]

    activations = []
    gradients = []

    def forward_hook(module, inp, output):
        activations.append(output)

    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    forward_handle = target_layer.register_forward_hook(forward_hook)
    backward_handle = target_layer.register_full_backward_hook(backward_hook)

    output = model(input_tensor)

    predicted_class = output.argmax(dim=1).item()

    model.zero_grad()
    output[0, predicted_class].backward()

    activation = activations[0]
    gradient = gradients[0]

    weights = gradient.mean(dim=(2, 3), keepdim=True)

    cam = (weights * activation).sum(dim=1).squeeze()

    cam = F.relu(cam)
    cam -= cam.min()

    if cam.max() != 0:
        cam /= cam.max()

    cam = cam.detach().cpu().numpy()

    cam = cv2.resize(
        cam,
        (image.width, image.height)
    )

    heatmap = np.uint8(255 * cam)
    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    original = np.array(image.convert("RGB"))

    heatmap = cv2.cvtColor(
        heatmap,
        cv2.COLOR_BGR2RGB
    )

    overlay = cv2.addWeighted(
        original,
        0.6,
        heatmap,
        0.4,
        0
    )

    forward_handle.remove()
    backward_handle.remove()

    return Image.fromarray(overlay), predicted_class