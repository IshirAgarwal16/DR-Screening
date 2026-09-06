import torch
import torch.nn as nn
from torchvision import models
from huggingface_hub import hf_hub_download


MODEL_REPO = "ishiragarwal16/dr-screening-resnet18"
MODEL_FILENAME = "best_model.pth"

CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR",
]


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(
        model.fc.in_features,
        5
    )
    return model


def load_model():
    device = get_device()
    model = create_model()

    # Download model from Hugging Face
    model_path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILENAME,
    )

    checkpoint = torch.load(
        model_path,
        map_location=device
    )

    # Our training script saved the model inside "model_state_dict"
    if "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model.to(device)
    model.eval()

    return model, device


if __name__ == "__main__":
    model, device = load_model()

    print("Model loaded successfully!")
    print("Device:", device)
    print("Classes:", CLASS_NAMES)