import cv2
import numpy as np

import torch
import torch.nn as nn

from torchvision import models, transforms
from huggingface_hub import hf_hub_download


# ==============================================================
# FUNDUS VALIDATOR
# ==============================================================

VALIDATOR_REPO = "ishiragarwal16/fundus-validator"
VALIDATOR_FILENAME = "best_validator.pth"

CLASS_NAMES = [
    "fundus",
    "non_fundus"
]


def create_validator():

    model = models.resnet18(weights=None)

    model.fc = nn.Linear(
        model.fc.in_features,
        2
    )

    return model


def load_validator():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = create_validator()

    model_path = hf_hub_download(
        repo_id=VALIDATOR_REPO,
        filename=VALIDATOR_FILENAME
    )

    checkpoint = torch.load(
        model_path,
        map_location=device
    )

    if "model_state_dict" in checkpoint:

        model.load_state_dict(
            checkpoint["model_state_dict"]
        )

    else:

        model.load_state_dict(
            checkpoint
        )

    model.to(device)

    model.eval()

    return model, device


def validate_fundus(image):

    model, device = load_validator()

    transform = transforms.Compose([

        transforms.Resize(
            (224, 224)
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[
                0.485,
                0.456,
                0.406
            ],

            std=[
                0.229,
                0.224,
                0.225
            ]
        )
    ])

    image = image.convert("RGB")

    image_tensor = transform(
        image
    ).unsqueeze(0).to(device)

    with torch.no_grad():

        output = model(
            image_tensor
        )

        probabilities = torch.softmax(
            output,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    predicted_class = CLASS_NAMES[
        prediction.item()
    ]

    confidence = (
        confidence.item() * 100
    )

    return (
        predicted_class,
        confidence
    )


# ==============================================================
# IMAGE QUALITY CHECK
# ==============================================================

def check_image_quality(image):

    """
    Basic fundus image quality assessment.

    Returns:
        quality:
            "good" or "poor"

        details:
            dictionary containing quality measurements
    """

    # ----------------------------------------------------------
    # PIL Image → NumPy
    # ----------------------------------------------------------

    image = np.array(
        image.convert("RGB")
    )


    # ----------------------------------------------------------
    # RGB → Grayscale
    # ----------------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )


    # ----------------------------------------------------------
    # 1. Sharpness / Blur Detection
    # ----------------------------------------------------------

    sharpness = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()


    # ----------------------------------------------------------
    # 2. Brightness
    # ----------------------------------------------------------

    brightness = np.mean(
        gray
    )


    # ----------------------------------------------------------
    # 3. Contrast
    # ----------------------------------------------------------

    contrast = np.std(
        gray
    )


    # ----------------------------------------------------------
    # Quality Rules
    # ----------------------------------------------------------

    # Prototype threshold
    blur_ok = sharpness >= 10

    brightness_ok = (
        30 <= brightness <= 220
    )

    contrast_ok = (
        contrast >= 25
    )


    # ----------------------------------------------------------
    # Final Quality
    # ----------------------------------------------------------

    quality = (
        blur_ok
        and brightness_ok
        and contrast_ok
    )


    # ----------------------------------------------------------
    # Details
    # ----------------------------------------------------------

    details = {

        "sharpness":
            round(
                float(sharpness),
                2
            ),

        "brightness":
            round(
                float(brightness),
                2
            ),

        "contrast":
            round(
                float(contrast),
                2
            ),

        "blur_ok":
            blur_ok,

        "brightness_ok":
            brightness_ok,

        "contrast_ok":
            contrast_ok,
    }


    return (

        "good"
        if quality
        else "poor",

        details
    )