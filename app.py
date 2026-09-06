"""
Explainable AI for Diabetic Retinopathy Screening in Rural India

Streamlit Dashboard

Run with:
streamlit run app.py
"""

from datetime import date

import streamlit as st
import torch
from PIL import Image
from torchvision import transforms

from model import load_model, CLASS_NAMES
from gradcam import generate_gradcam


# ---------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="DR Screening - Clinical Decision Support",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

DR_GRADES = {
    0: {
        "label": "No DR",
        "risk": "Low",
        "color": "#2e7d32",
    },
    1: {
        "label": "Mild",
        "risk": "Low-Moderate",
        "color": "#9e9d24",
    },
    2: {
        "label": "Moderate",
        "risk": "Moderate",
        "color": "#f9a825",
    },
    3: {
        "label": "Severe",
        "risk": "High",
        "color": "#ef6c00",
    },
    4: {
        "label": "Proliferative DR",
        "risk": "Very High",
        "color": "#c62828",
    },
}


RECOMMENDATIONS = {
    0: (
        "No diabetic retinopathy was predicted by the AI model. "
        "Routine screening and clinical follow-up are recommended."
    ),
    1: (
        "The AI model predicted mild diabetic retinopathy. "
        "Clinical evaluation and appropriate follow-up are recommended."
    ),
    2: (
        "The AI model predicted moderate diabetic retinopathy. "
        "Referral to an ophthalmologist for further evaluation is recommended."
    ),
    3: (
        "The AI model predicted severe diabetic retinopathy. "
        "Prompt ophthalmology referral is recommended."
    ),
    4: (
        "The AI model predicted proliferative diabetic retinopathy. "
        "Urgent ophthalmology evaluation is recommended."
    ),
}


EXPLANATION_TEXT = {
    0: (
        "The model classified this image as No DR. "
        "The Grad-CAM heatmap shows the retinal regions that contributed "
        "most strongly to this prediction."
    ),
    1: (
        "The model classified this image as Mild DR. "
        "The Grad-CAM heatmap shows the retinal regions that contributed "
        "most strongly to this prediction."
    ),
    2: (
        "The model classified this image as Moderate DR. "
        "The Grad-CAM heatmap shows the retinal regions that contributed "
        "most strongly to this prediction."
    ),
    3: (
        "The model classified this image as Severe DR. "
        "The Grad-CAM heatmap shows the retinal regions that contributed "
        "most strongly to this prediction."
    ),
    4: (
        "The model classified this image as Proliferative DR. "
        "The Grad-CAM heatmap shows the retinal regions that contributed "
        "most strongly to this prediction."
    ),
}


# ---------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------

@st.cache_resource
def get_ai_model():
    model, device = load_model()
    return model, device


# ---------------------------------------------------------------------
# AI inference
# ---------------------------------------------------------------------

def run_real_analysis(image):

    model, device = get_ai_model()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    image = image.convert("RGB")

    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0).to(device)

    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1,
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1,
        )

    grade = prediction.item()

    confidence = round(
        confidence.item() * 100,
        1,
    )

    return grade, confidence


# ---------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "gradcam_image" not in st.session_state:
    st.session_state.gradcam_image = None


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------

with st.sidebar:

    st.markdown("## 🩺 Patient Details")
    st.markdown("---")

    patient_id = st.text_input(
        "Patient ID",
        placeholder="e.g. PHC-2026-00142",
    )

    patient_age = st.number_input(
        "Patient Age",
        min_value=0,
        max_value=120,
        value=50,
        step=1,
    )

    screening_date = st.date_input(
        "Screening Date",
        value=date.today(),
    )

    st.markdown("---")

    st.markdown("### 📤 Upload Fundus Image")

    uploaded_file = st.file_uploader(
        "Upload a retinal fundus image",
        type=["png", "jpg", "jpeg"],
        help="Supported formats: PNG, JPG, JPEG",
    )

    st.markdown("---")

    st.info(
        "**AI MODEL ACTIVE**\n\n"
        "This dashboard uses the trained DR grading model "
        "loaded from `best_model.pth`."
    )


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

st.title(
    "👁️ Explainable AI for Diabetic Retinopathy Screening"
)

st.markdown(
    "##### Clinical Decision-Support for Rural Healthcare Screening  "
    ""
)

st.markdown("---")


# ---------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------

col_left, col_right = st.columns(
    [1, 1.2],
    gap="large",
)


# ---------------------------------------------------------------------
# Left column
# ---------------------------------------------------------------------

with col_left:

    st.subheader("Fundus Image")

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        st.session_state.uploaded_image = image

        st.image(
            image,
            caption="Uploaded fundus image",
            use_container_width=True,
        )

    else:

        st.markdown(
            """
            <div style="
                border: 2px dashed #b0b0b0;
                border-radius: 10px;
                padding: 60px 20px;
                text-align: center;
                color: #888888;
                background-color: #fafafa;">

                No image uploaded yet.<br>

                Use the sidebar to upload a fundus image
                (PNG/JPG/JPEG).

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    analyze_clicked = st.button(
        "🔍 Analyze Image",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None),
    )

    if uploaded_file is None:

        st.caption(
            "Upload a fundus image to enable analysis."
        )


    # -----------------------------------------------------------------
    # Analysis
    # -----------------------------------------------------------------

    if analyze_clicked:

        with st.spinner(
            "Running AI model and generating Grad-CAM..."
        ):

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            # AI prediction
            grade, confidence = run_real_analysis(
                image
            )

            # Load model
            model, device = get_ai_model()

            # Generate Grad-CAM
            gradcam_image, _ = generate_gradcam(
                model,
                image,
                device,
            )

            # Save results
            st.session_state.analysis_result = {
                "grade": grade,
                "confidence": confidence,
                "patient_id": patient_id,
                "patient_age": patient_age,
                "screening_date": screening_date,
            }

            st.session_state.gradcam_image = (
                gradcam_image
            )


# ---------------------------------------------------------------------
# Right column - Screening Result
# ---------------------------------------------------------------------

with col_right:

    st.subheader("Screening Result")

    result = st.session_state.analysis_result

    if result is None:

        st.markdown(
            """
            <div style="
                border-radius: 10px;
                padding: 40px 20px;
                text-align: center;
                color: #888888;
                background-color: #fafafa;">

                Results will appear here after analysis.

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        grade = result["grade"]

        grade_info = DR_GRADES[grade]


                # -------------------------------------------------------------
        # DR Grade Box
        # -------------------------------------------------------------

        if grade == 0:

            st.success(
                f"### Grade {grade}: {grade_info['label']}"
            )

        elif grade == 1:

            st.warning(
                f"### Grade {grade}: {grade_info['label']}"
            )

        elif grade == 2:

            st.warning(
                f"### Grade {grade}: {grade_info['label']}"
            )

        elif grade == 3:

            st.error(
                f"### Grade {grade}: {grade_info['label']}"
            )

        else:

            st.error(
                f"### Grade {grade}: {grade_info['label']}"
            )

        # -------------------------------------------------------------
        # Metrics
        # -------------------------------------------------------------

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        metric_col1.metric(
            "DR Grade",
            f"{grade} - {grade_info['label']}",
        )

        metric_col2.metric(
            "Model Confidence",
            f"{result['confidence']}%",
        )

        metric_col3.metric(
            "Risk Level",
            grade_info["risk"],
        )


        # -------------------------------------------------------------
        # Risk Assessment
        # -------------------------------------------------------------

        st.markdown("#### 🚦 Risk Assessment")

        if grade == 0:

            st.success(
                "🟢 **LOW RISK**\n\n"
                "Routine screening and clinical follow-up recommended."
            )

        elif grade == 1:

            st.warning(
                "🟡 **LOW-MODERATE RISK**\n\n"
                "Clinical evaluation and appropriate follow-up recommended."
            )

        elif grade == 2:

            st.warning(
                "🟡 **MODERATE RISK**\n\n"
                "Ophthalmologist follow-up recommended."
            )

        elif grade == 3:

            st.error(
                "🟠 **HIGH RISK**\n\n"
                "Prompt ophthalmology referral recommended."
            )

        else:

            st.error(
                "🔴 **VERY HIGH RISK**\n\n"
                "Urgent ophthalmology evaluation recommended."
            )


        # -------------------------------------------------------------
        # Recommendation
        # -------------------------------------------------------------

        st.markdown("#### 📋 Recommendation")

        if grade == 0:

            st.success(
                RECOMMENDATIONS[grade]
            )

        elif grade in [1, 2]:

            st.warning(
                RECOMMENDATIONS[grade]
            )

        else:

            st.error(
                RECOMMENDATIONS[grade]
            )


# ---------------------------------------------------------------------
# AI Explanation + Grad-CAM
# ---------------------------------------------------------------------

if st.session_state.analysis_result is not None:

    st.markdown("---")

    st.subheader("🧠 AI Explanation")

    exp_col1, exp_col2 = st.columns(
        [1, 1],
        gap="large",
    )

    grade = st.session_state.analysis_result["grade"]


    # Text explanation
    with exp_col1:

        st.markdown(
            "**Model Reasoning**"
        )

        st.write(
            EXPLANATION_TEXT[grade]
        )

        st.caption(
            "Grad-CAM indicates image regions that influenced "
            "the model prediction. It is not a definitive "
            "lesion detector or medical diagnosis."
        )


    # Grad-CAM
    with exp_col2:

        st.markdown(
            "**🔥 Grad-CAM Heatmap**"
        )

        if st.session_state.gradcam_image is not None:

            st.image(
                st.session_state.gradcam_image,
                caption=(
                    "Regions influencing the AI prediction"
                ),
                use_container_width=True,
            )

        else:

            st.warning(
                "Grad-CAM could not be generated."
            )


# ---------------------------------------------------------------------
# Screening Report
# ---------------------------------------------------------------------

if st.session_state.analysis_result is not None:

    st.markdown("---")

    st.subheader("📄 Screening Report")

    result = st.session_state.analysis_result

    grade = result["grade"]

    grade_info = DR_GRADES[grade]


    report_col1, report_col2 = st.columns(2)


    with report_col1:

        st.markdown(
            f"""
            **Patient ID:** {result['patient_id'] or "Not provided"}

            **Patient Age:** {result['patient_age']}

            **Screening Date:** {
                result['screening_date'].strftime('%d %B %Y')
            }
            """
        )


    with report_col2:

        st.markdown(
            f"""
            **DR Grade:** {grade} - {grade_info['label']}

            **Model Confidence:** {result['confidence']}%

            **Risk Level:** {grade_info['risk']}
            """
        )


    st.markdown("**Recommendation:**")

    st.write(
        RECOMMENDATIONS[grade]
    )


    # -------------------------------------------------------------
    # Report text
    # -------------------------------------------------------------

    report_text = (

        "DIABETIC RETINOPATHY SCREENING REPORT\n"

        + "=" * 45

        + "\n"

        + f"Patient ID: "
        + f"{result['patient_id'] or 'Not provided'}\n"

        + f"Patient Age: "
        + f"{result['patient_age']}\n"

        + f"Screening Date: "
        + f"{result['screening_date'].strftime('%d %B %Y')}\n\n"

        + f"DR Grade: "
        + f"{grade} - {grade_info['label']}\n"

        + f"Model Confidence: "
        + f"{result['confidence']}%\n"

        + f"Risk Level: "
        + f"{grade_info['risk']}\n\n"

        + "Recommendation:\n"

        + RECOMMENDATIONS[grade]

        + "\n\n"

        + "AI Explanation:\n"

        + EXPLANATION_TEXT[grade]

        + "\n\n"

        + "=" * 45

        + "\n"

        + "DISCLAIMER: This is a screening and "

        + "clinical decision-support prototype. "

        + "The output is generated by an AI model and "

        + "does not constitute a definitive medical diagnosis. "

        + "All findings must be reviewed by a qualified "

        + "ophthalmologist or medical professional.\n"
    )


    st.download_button(
        label="⬇️ Download Report (Text)",

        data=report_text,

        file_name=(
            f"DR_Screening_Report_"
            f"{result['patient_id'] or 'patient'}.txt"
        ),

        mime="text/plain",

        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------

st.markdown("---")

st.error(
    "**Disclaimer:** This application is a screening and "
    "clinical decision-support prototype developed for the "
    "Smart India Hackathon. It is not a definitive medical "
    "diagnostic system. AI predictions and Grad-CAM "
    "visualizations should not be used alone for actual "
    "patient care. All screening results must be reviewed "
    "and confirmed by a qualified ophthalmologist or medical "
    "professional.",
    icon="⚕️",
)

st.caption(
    "Explainable AI for Diabetic Retinopathy Screening in Rural India | "
    "Smart India Hackathon Prototype"
)