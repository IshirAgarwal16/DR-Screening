import requests
import base64


# =========================
# API URL
# =========================

API_URL = "http://127.0.0.1:8000/analyze"


# =========================
# IMAGE PATH
# =========================

IMAGE_PATH = "retina_test3.png"


# =========================
# SEND IMAGE TO API
# =========================

with open(IMAGE_PATH, "rb") as image_file:

    response = requests.post(
        API_URL,
        files={
            "file": (
                IMAGE_PATH,
                image_file,
                "image/png"
            )
        }
    )


# =========================
# RESPONSE STATUS
# =========================

print("Status Code:", response.status_code)

print("\nRAW API RESPONSE:")
print(response.text)


# =========================
# STOP IF ERROR
# =========================

if response.status_code != 200:

    print("\nAPI Error!")
    exit()


# =========================
# CONVERT JSON
# =========================

result = response.json()


# =========================
# PRINT ALL RESPONSE KEYS
# =========================

print("\nResponse Keys:")
print(result.keys())


# =========================
# CHECK SUCCESS
# =========================

if result.get("success") != True:

    print("\nAnalysis was not successful.")

    print(
        "Stage:",
        result.get("stage")
    )

    print(
        "Message:",
        result.get("message")
    )

    exit()


# =========================
# PRINT RESULT
# =========================

print("\nDR Result")
print("-------------------------")

print(
    "DR Class:",
    result.get("dr_class")
)

print(
    "Confidence:",
    result.get("confidence")
)

print(
    "Referable Status:",
    result.get("referable_status")
)

print(
    "Referable Probability:",
    result.get("referable_probability")
)

print(
    "Grad-CAM Class:",
    result.get("gradcam_class")
)


# =========================
# SAVE GRAD-CAM
# =========================

gradcam_base64 = result.get(
    "gradcam_image"
)


if gradcam_base64:

    image_data = base64.b64decode(
        gradcam_base64
    )

    with open(
        "gradcam_result.png",
        "wb"
    ) as output_file:

        output_file.write(
            image_data
        )

    print(
        "\nGrad-CAM saved successfully!"
    )

    print(
        "File: gradcam_result.png"
    )

else:

    print(
        "\nGrad-CAM image not found!"
    )