# DR-Screening — Explainable AI for Diabetic Retinopathy

DR-Screening is an AI-assisted diabetic retinopathy screening prototype that analyzes retinal fundus images using deep learning. It combines image validation, quality assessment, severity classification, referable-DR assessment, and Grad-CAM visualization in a screening workflow.

The project explores how explainable AI could support retinal screening workflows, including settings where access to eye-care specialists may be limited.

## Features

- **Fundus Image Validation:** Checks whether an uploaded image is suitable for the retinal analysis pipeline.
- **Image Quality Assessment:** Evaluates sharpness, brightness, and contrast before classification.
- **DR Severity Classification:** Uses a ResNet18 model to classify retinal images into five severity grades.
- **Referable DR Assessment:** Calculates referable-DR probability from the predicted probabilities of Grades 2, 3, and 4.
- **Grad-CAM Visualization:** Generates a heatmap highlighting image regions that influenced the model prediction.
- **Patient Registration:** Provides a web interface for entering patient information.
- **Screening Workflow:** Supports image upload, analysis, and presentation of screening results.
- **Screening History:** Includes pages for reviewing previous screening records and individual screening details.
- **REST API:** Exposes image analysis through FastAPI.
- **Docker Support:** Includes a Dockerfile for containerizing the AI service.

## Technology Stack

| Component | Technologies |
|---|---|
| AI model | PyTorch, Torchvision, ResNet18 |
| API | FastAPI, Uvicorn |
| Image processing | OpenCV, Pillow, NumPy |
| Model hosting | Hugging Face Hub |
| Frontend | HTML, CSS, JavaScript |
| Backend | Java, Spring Boot |
| Database | PostgreSQL |
| Containerization | Docker |

## Repository Structure

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
├── Dockerfile
└── best_model.pth
```

The tree highlights the principal files used by the screening interface and AI service. The trained checkpoint may be hosted separately if it is too large to include in the Git repository.

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

### Referable DR

For this prototype, Grades 0–1 are classified as non-referable and Grades 2–4 as referable.

The referable probability is calculated by adding the predicted probabilities for Grades 2, 3, and 4:

```python
referable_probability = (
    P(Grade 2) +
    P(Grade 3) +
    P(Grade 4)
)
```

The current configured decision threshold is `0.46`.

## Dataset and Model

The severity classifier was trained using the APTOS 2019 Blindness Detection dataset.

- **Architecture:** ResNet18
- **Number of classes:** 5
- **Dataset size:** 3,662 images
- **Training/validation split:** 80/20
- **Model checkpoint:** `best_model.pth`

The project also includes a separate fundus validator. Its current prototype training setup uses retinal images as positive examples and CIFAR-10 images as negative examples. More challenging real-world negative images are needed for a stronger evaluation.

### Model Evaluation

On the APTOS validation split, the referable-DR classifier achieved the following results at a threshold of `0.46`:

| Metric | Result |
|---|---:|
| Accuracy | 92.63% |
| Sensitivity | 90.60% |
| Specificity | 94.02% |
| Precision | 91.22% |
| F1-score | 90.91% |

These results describe performance on the project's dataset split. They do not establish clinical validity or guarantee performance on images collected in real-world healthcare settings.

## Grad-CAM Explainability

Grad-CAM is used to generate a visual heatmap associated with the model's prediction. It helps inspect which image regions influenced the classification.

The heatmap is an interpretability aid, not proof that a particular retinal lesion exists. Its output should be considered alongside the model prediction and other limitations of the prototype.

## Requirements

For local development:

- Python 3.11
- Git
- Dependencies listed in `requirements.txt`

For containerized execution:

- Docker Desktop

## Local Setup

### 1. Open the project directory

```powershell
cd C:\Ishircode\DR-Screening
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can temporarily allow activation scripts in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start FastAPI

```powershell
uvicorn ai_api:app --reload
```

The AI service should be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

To run the API so that it is accessible through Docker networking, use:

```powershell
uvicorn ai_api:app --host 0.0.0.0 --port 8000
```

Keep the terminal running while using the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Service health check |
| POST | `/analyze` | Analyze an uploaded retinal image |

The `/analyze` endpoint processes the image and returns the analysis response, including relevant classification, quality, referable-DR, and Grad-CAM information.

Refer to the interactive API documentation at `/docs` for the exact request format and response schema.

## Run with Docker

Build the AI service image from the repository root:

```powershell
docker build -t dr-screening-ai .
```

Start the container:

```powershell
docker run --name dr-screening-container -p 8000:8000 dr-screening-ai
```

Test the health endpoint:

```powershell
curl.exe http://localhost:8000/health
```

If the container fails during startup, inspect its logs:

```powershell
docker logs dr-screening-container
```

The model checkpoint or model-hosting configuration must be accessible to the application at runtime.

## Integration with the Backend

The complete prototype uses separate services:

| Service | Port |
|---|---:|
| Spring Boot backend | 8084 |
| FastAPI AI service | 8000 |
| PostgreSQL database | 5432 |

The Spring Boot backend manages patient records, communicates with the AI service, and stores screening results in PostgreSQL.

When Spring Boot runs inside Docker and FastAPI runs directly on the Windows host, configure the backend's AI endpoint as:

```text
http://host.docker.internal:8000/analyze
```

When both services run inside Docker, they should share a Docker network. In that setup, use the AI container or Compose service name instead of `localhost` or `127.0.0.1`.

## Security and Data Handling

- Keep database passwords and API keys out of Git commits.
- Exclude virtual environments, local environment files, and unnecessary generated files from the repository.
- Avoid publishing patient-identifiable information or real patient images in public repositories.
- Use appropriate access controls and data-protection measures before handling real patient information.

## Limitations and Intended Use

DR-Screening is a development and educational prototype, not a clinically validated diagnostic system.

- Dataset-based metrics do not guarantee real-world performance.
- Image-quality thresholds are heuristic and require further evaluation.
- The fundus validator needs testing against more realistic non-fundus images.
- Grad-CAM highlights regions that influenced a prediction; it does not prove the presence of disease.
- Predictions must not replace examination by a qualified eye-care professional.

Clinical validation, external testing, privacy safeguards, and appropriate regulatory review are necessary before real-world clinical deployment.