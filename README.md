# DR-Screening — Explainable AI for Diabetic Retinopathy

DR-Screening is an AI-assisted diabetic retinopathy (DR) screening prototype that analyzes retinal fundus images using deep learning. It combines fundus image validation, image quality assessment, severity classification, referable-DR assessment, and Grad-CAM visualization in a screening workflow.

The project explores how explainable AI could support retinal screening workflows, including settings where access to eye-care specialists may be limited.

> **Disclaimer:** This project is intended for educational and research purposes. It is not a clinically validated diagnostic system and must not replace professional medical evaluation.

## Features

- **Fundus Image Validation:** Checks whether an uploaded image is suitable for the retinal analysis pipeline.
- **Image Quality Assessment:** Evaluates sharpness, brightness, and contrast before classification.
- **DR Severity Classification:** Uses a ResNet18 model to classify retinal images into five severity grades.
- **Referable DR Assessment:** Calculates referable-DR probability from the predicted probabilities of Grades 2, 3, and 4.
- **Grad-CAM Visualization:** Generates a heatmap to help inspect image regions that influenced the model prediction.
- **Patient Registration:** Provides an interface for entering patient information.
- **Screening Workflow:** Supports image upload, analysis, and presentation of screening results.
- **Screening History:** Provides pages for reviewing previous screening records and individual screening details.
- **REST API:** Exposes image analysis through FastAPI.
- **Backend Integration:** Uses Spring Boot to manage application workflows and communicate with the AI service.
- **Database Integration:** Uses PostgreSQL to store patient and screening records.

## Technology Stack

| Component | Technologies |
|---|---|
| AI model | PyTorch, Torchvision, ResNet18 |
| AI API | FastAPI, Uvicorn |
| Image processing | OpenCV, Pillow, NumPy |
| Model hosting | Hugging Face Hub |
| Frontend | HTML, CSS, JavaScript |
| Backend | Java, Spring Boot |
| Database | PostgreSQL |
| Development tools | Git, VS Code |

## System Architecture

The application consists of three main services:

1. **Frontend:** Provides the user interface for patient registration, image upload, and screening results.
2. **Spring Boot Backend:** Manages application workflows, communicates with the AI service, and interacts with PostgreSQL.
3. **FastAPI AI Service:** Validates retinal images, performs quality checks, runs the DR classifier, and generates Grad-CAM visualizations.

PostgreSQL stores the application's patient and screening records.

## Repository Structure

The following tree represents the main AI repository files and frontend structure:

```text
DR-Screening/
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   ├── doctor.html
│   ├── history.html
│   ├── login.html
│   ├── patient.html
│   ├── screening-details.html
│   └── screening.html
│
├── ai_api.py
├── gradcam.py
├── model.py
├── quality_check.py
├── requirements.txt
└── best_model.pth
```

The Spring Boot backend is maintained separately in the `DR-Backend` project.

The trained model checkpoint may be stored locally or obtained from the configured model-hosting source, depending on the implementation.

## How the System Works

```text
Retinal Image Upload
        |
        v
Fundus Image Validation
        |
        v
Image Quality Assessment
        |
        v
ResNet18 DR Classification
        |
        v
Referable DR Probability
        |
        v
Threshold-Based Assessment
        |
        v
Grad-CAM Generation
        |
        v
Screening Result
```

The pipeline checks the input image before running the severity classifier. Images that fail the configured validation or quality checks are rejected rather than being passed through the complete analysis process.

## DR Severity Classification

The model predicts one of five diabetic retinopathy grades.

| Grade | Classification |
|---|---|
| 0 | No DR |
| 1 | Mild DR |
| 2 | Moderate DR |
| 3 | Severe DR |
| 4 | Proliferative DR |

### Referable DR Assessment

For this prototype, Grades 0–1 are classified as non-referable and Grades 2–4 as referable.

The referable probability is calculated by adding the predicted probabilities for Grades 2, 3, and 4:

```python
referable_probability = (
    P(Grade 2) +
    P(Grade 3) +
    P(Grade 4)
)
```

The configured decision threshold is `0.46`. The final assessment depends on the implementation's threshold logic and model outputs.

## Dataset and Model

The severity classifier was trained using the APTOS 2019 Blindness Detection dataset.

- **Architecture:** ResNet18
- **Number of classes:** 5
- **Dataset size:** 3,662 images
- **Training/validation split:** 80/20
- **Model checkpoint:** `best_model.pth`

The project also includes a separate fundus validator. Its current prototype training setup uses retinal images as positive examples and CIFAR-10 images as negative examples. More challenging real-world negative images are needed for stronger evaluation.

### Model Evaluation

The reported results on the APTOS validation split at a referable-DR threshold of `0.46` are:

| Metric | Reported Result |
|---|---:|
| Accuracy | 92.63% |
| Sensitivity | 90.60% |
| Specificity | 94.02% |
| Precision | 91.22% |
| F1-score | 90.91% |

These figures are reported project results and should be retained only if supported by the corresponding evaluation output. They describe performance on the project's dataset split and do not establish clinical validity or guarantee performance on images collected in real-world healthcare settings.

## Grad-CAM Explainability

Grad-CAM generates a visual heatmap associated with the model's prediction. It helps inspect which image regions influenced the classification.

The heatmap is an interpretability aid, not proof that a particular retinal lesion exists. Its output should be considered alongside the model prediction and the limitations of the prototype.

## Requirements

For local development:

- Python 3.11
- Java 21
- Maven 3.9 or a compatible version
- PostgreSQL 16 or a compatible version
- Git
- Python dependencies listed in `requirements.txt`

The frontend uses HTML, CSS, and JavaScript and can be served locally using a suitable static file server.

**The current development setup does not require Docker.**

## Local Setup

### 1. Clone the AI Repository

```powershell
git clone https://github.com/IshirAgarwal16/DR-Screening.git
cd DR-Screening
```

### 2. Create a Python Virtual Environment

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Alternatively, run the Python executable directly without activating the environment.

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

Ensure that the installed PyTorch and Torchvision versions are compatible with the model and your Python environment.

### 4. Start the AI Service

From the AI repository directory:

```powershell
python -m uvicorn ai_api:app --reload --host 127.0.0.1 --port 8000
```

The service should be accessible at:

- **API base URL:** `http://localhost:8000`
- **Interactive API documentation:** `http://localhost:8000/docs`
- **Health check:** `http://localhost:8000/health`

Keep this terminal open while using the application.

### 5. Set Up PostgreSQL

Ensure PostgreSQL is installed and running.

Create or use the `dr_screening` database and configure the Spring Boot application's database connection.

Example local database URL:

```text
jdbc:postgresql://localhost:5432/dr_screening
```

Configure the database username and password through environment variables or a local, uncommitted configuration file. Do not commit credentials to GitHub.

### 6. Start the Spring Boot Backend

The backend is maintained separately in the `DR-Backend` project.

Open another PowerShell terminal and navigate to the backend directory:

```powershell
cd C:\Ishircode\DR-Backend\drbackend
mvn spring-boot:run
```

The backend is configured to use port `8084`. Confirm the startup logs before testing the application.

Ensure that the backend's AI service URL points to the local FastAPI service:

```text
http://localhost:8000/analyze
```

This address applies when both services run directly on the same machine. The actual configuration must match the backend implementation.

### 7. Start the Frontend

The frontend consists of HTML, CSS, and JavaScript files in the `frontend` directory.

Serve the frontend locally using a static file server and open the appropriate page in your browser. Verify that its API requests point to the running Spring Boot backend.

If the frontend and backend use different origins, configure appropriate Cross-Origin Resource Sharing (CORS) settings in the backend.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | AI service health check |
| POST | `/analyze` | Analyze an uploaded retinal image |

The `/analyze` endpoint returns the analysis response, including the classification, quality assessment, referable-DR information, and Grad-CAM output supported by the implementation.

Refer to the interactive API documentation at `http://localhost:8000/docs` for the actual request format and response schema.

## Service Ports

| Service | Port |
|---|---:|
| Spring Boot backend | 8084 |
| FastAPI AI service | 8000 |
| PostgreSQL | 5432 |

These are the configured local development ports. If a port is changed, update the relevant service configuration and API URLs accordingly.

## Security and Data Handling

- Keep database passwords, API keys, and other secrets out of Git commits.
- Use environment variables or local configuration files excluded from version control.
- Exclude virtual environments, caches, and unnecessary generated files from the repository.
- Do not publish patient-identifiable information or real patient images in a public repository.
- Apply appropriate authentication, authorization, and data-protection measures before handling real patient information.

## Limitations and Intended Use

DR-Screening is an educational and research prototype, not a clinically validated diagnostic system.

- Dataset-based metrics do not guarantee real-world performance.
- Image-quality thresholds are heuristic and require further evaluation.
- The fundus validator needs testing against more realistic non-fundus images.
- Grad-CAM highlights regions that influenced a prediction; it does not prove the presence of disease.
- The model may be affected by differences in cameras, image quality, populations, and acquisition conditions.
- Predictions must not replace examination by a qualified eye-care professional.

Clinical validation, external testing, privacy safeguards, security controls, and appropriate regulatory review are necessary before real-world clinical deployment.

## Future Improvements

- Evaluate performance on an independent external dataset.
- Improve fundus validation using challenging non-fundus images.
- Assess calibration and threshold selection for referable DR.
- Strengthen API authentication, input validation, and error handling.
- Improve explainability evaluation and user-facing result presentation.
- Conduct usability and workflow testing with qualified eye-care professionals.

## Acknowledgements

This project uses the APTOS 2019 Blindness Detection dataset for diabetic retinopathy classification research. Refer to the dataset's original source and terms for attribution and usage requirements.
