from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import base64

from quality_check import validate_fundus, check_image_quality
from model import load_model, CLASS_NAMES
from gradcam import generate_gradcam

import torch
from torchvision import transforms


app = FastAPI(
    title="DR Screening AI API",
    description="AI service for Diabetic Retinopathy screening",
    version="1.0"
)


# =========================
# LOAD DR MODEL ONCE
# =========================

model, device = load_model()


# =========================
# IMAGE TRANSFORM
# =========================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "DR Screening AI API is running"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "DR Screening AI"
    }


# =========================
# ANALYZE IMAGE
# =========================

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...)
):

    # =========================
    # READ UPLOADED IMAGE
    # =========================

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")


    # =========================
    # STEP 1: FUNDUS VALIDATION
    # =========================

    fundus_class, fundus_confidence = validate_fundus(
        image
    )


    if fundus_class == "non_fundus":

        return {

            "success": False,

            "stage": "fundus_validation",

            "message":
                "Uploaded image does not appear to be a fundus image.",

            "fundus": False,

            "confidence":
                round(
                    fundus_confidence,
                    1
                )
        }


    # =========================
    # STEP 2: IMAGE QUALITY
    # =========================

    quality, quality_details = check_image_quality(
        image
    )


    if quality == "poor":

        return {

            "success": False,

            "stage": "quality_check",

            "message":
                "Fundus image quality is poor. Please capture another image.",

            "fundus": True,

            "fundus_confidence":
                round(
                    fundus_confidence,
                    1
                ),

            "quality": "poor",

            "quality_details":
                quality_details
        }


    # =========================
    # STEP 3: DR CLASSIFICATION
    # =========================

    image_tensor = transform(
        image
    )

    image_tensor = image_tensor.unsqueeze(
        0
    ).to(device)


    with torch.no_grad():

        outputs = model(
            image_tensor
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )


    prediction = torch.argmax(
        probabilities,
        dim=1
    )


    grade = prediction.item()


    confidence = (
        probabilities[0, grade].item()
        * 100
    )


    # =========================
    # STEP 4: REFERABLE DR
    # =========================

    referable_probability = (
        probabilities[0, 2:].sum().item()
    )


    REFERABLE_THRESHOLD = 0.46


    if referable_probability >= REFERABLE_THRESHOLD:

        referable_status = "Referable DR"

    else:

        referable_status = "Non-Referable DR"


    # =========================
    # STEP 5: RECOMMENDATION
    # =========================

    if referable_status == "Referable DR":

        recommendation = (
            "Refer to an ophthalmologist "
            "for further evaluation."
        )

    else:

        recommendation = (
            "No referable DR detected. "
            "Continue routine diabetic eye screening."
        )


    # =========================
    # STEP 6: GRAD-CAM
    # =========================

    gradcam_image, gradcam_class = generate_gradcam(
        model,
        image,
        device
    )


    # Convert Grad-CAM image to PNG bytes

    buffer = io.BytesIO()

    gradcam_image.save(
        buffer,
        format="PNG"
    )


    # Convert image to Base64

    gradcam_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")


    # =========================
    # FINAL RESULT
    # =========================

    return {

        "success": True,

        "stage": "complete",

        "fundus": True,

        "fundus_confidence":
            round(
                fundus_confidence,
                1
            ),

        "quality": "good",

        "quality_details":
            quality_details,

        "dr_grade":
            grade,

        "dr_class":
            CLASS_NAMES[grade],

        "confidence":
            round(
                confidence,
                1
            ),

        "referable_status":
            referable_status,

        "referable_probability":
            round(
                referable_probability * 100,
                1
            ),

        "recommendation":
            recommendation,

        "gradcam_class":
            CLASS_NAMES[gradcam_class],

        "gradcam_image":
            gradcam_base64
    }