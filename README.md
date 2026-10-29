# DR-Screening — Diabetic Retinopathy Screening Using AI

DR-Screening is a deep learning project that analyzes retinal images to identify signs of diabetic retinopathy (DR). It uses a ResNet18 model to predict the severity of DR and Grad-CAM to visualize the image regions that influenced the prediction.

The project includes image quality checks, patient registration, screening results, and screening history.

**Disclaimer:** This project is for educational purposes only. It is not a clinically validated diagnostic system and does not replace a doctor's advice.

## Features

- **Image Validation:** Checks whether the uploaded image is suitable for analysis.
- **Image Quality Check:** Checks image sharpness, brightness, and contrast.
- **DR Classification:** Classifies retinal images into five severity grades using ResNet18.
- **Referable DR Assessment:** Estimates the probability of referable DR.
- **Grad-CAM:** Generates a heatmap to visualize the regions influencing the prediction.
- **Patient Management:** Supports patient registration and screening history.
- **Web Interface:** Allows users to upload images and view results.
- **Backend and Database:** Uses Spring Boot, FastAPI, and PostgreSQL to manage the application.

## Technology Stack

| Component | Technologies |
|---|---|
| AI Model | PyTorch, Torchvision, ResNet18 |
| AI API | FastAPI, Uvicorn |
| Image Processing | OpenCV, Pillow, NumPy |
| Frontend | HTML, CSS, JavaScript |
| Backend | Java, Spring Boot |
| Database | PostgreSQL |
| Model Hosting | Hugging Face Hub |
| Tools | Git, VS Code |

## How It Works

1. The user uploads a retinal image.
2. The system checks the image quality.
3. ResNet18 predicts the DR severity grade.
4. The system calculates the referable-DR probability.
5. Grad-CAM generates a heatmap for visualization.
6. The results are displayed on the website.

## DR Severity Grades

| Grade | Classification |
|---|---|
| 0 | No DR |
| 1 | Mild DR |
| 2 | Moderate DR |
| 3 | Severe DR |
| 4 | Proliferative DR |

In this prototype, Grades 2, 3, and 4 are considered referable. Their predicted probabilities are added together, and the result is compared with a threshold of `0.46`.

## Dataset and Model

- **Dataset:** APTOS 2019 Blindness Detection
- **Model:** ResNet18
- **Number of Classes:** 5
- **Dataset Size:** 3,662 images
- **Training/Validation Split:** 80/20
- **Model File:** `best_model.pth`

The project also includes a basic image validator trained using retinal images and CIFAR-10 images as negative examples. It needs further testing with more realistic images.

## Model Evaluation

The following results were reported for the project's validation split. Keep them only if they match your actual evaluation output.

| Metric | Result |
|---|---:|
| Accuracy | 92.63% |
| Sensitivity | 90.60% |
| Specificity | 94.02% |
| Precision | 91.22% |
| F1-score | 90.91% |

These results do not guarantee the same performance on real-world retinal images.

## Project Structure

```text
DR-Screening/
├── frontend/
│   ├── css/style.css
│   ├── js/script.js
│   ├── doctor.html
│   ├── history.html
│   ├── login.html
│   ├── patient.html
│   ├── screening.html
│   └── screening-details.html
├── ai_api.py
├── gradcam.py
├── model.py
├── quality_check.py
├── requirements.txt
├── memory_assistant.py
└── best_model.pth
```

The Spring Boot backend is maintained separately in the `DR-Backend` project.

## Installation and Setup

### Requirements

- Python 3.11
- Java 21
- Maven 3.9 or compatible
- PostgreSQL 16 or compatible
- Git

### 1. Clone the Repository

```powershell
git clone https://github.com/IshirAgarwal16/DR-Screening.git
cd DR-Screening
```

### 2. Install Python Dependencies

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Run the AI Service

```powershell
python -m uvicorn ai_api:app --reload --host 127.0.0.1 --port 8000
```

Open `http://localhost:8000/docs` to test the API.

### 4. Configure PostgreSQL

Create a database named `dr_screening` and configure the database credentials in the Spring Boot backend.

Example database URL:

```text
jdbc:postgresql://localhost:5432/dr_screening
```

### 5. Run the Spring Boot Backend

Navigate to the `DR-Backend` project and run:

```powershell
mvn spring-boot:run
```

The configured backend port is `8084`. Ensure that the backend connects to the AI service at `http://localhost:8000/analyze`.

### 6. Run the Frontend

Start a local static server for the `frontend` directory and open the appropriate HTML page in your browser. Ensure the API URLs are configured correctly.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Check AI service status |
| POST | `/analyze` | Analyze a retinal image |

Visit `http://localhost:8000/docs` for API details.

## Additional Feature: Memory Assistant

The project also contains an experimental `memory_assistant.py` service that uses Hindsight for memory storage and retrieval and Groq to generate responses.

It provides `/health` and `/chat` endpoints. This is a separate local prototype, and its integration with the main application has not been confirmed.

Keep API keys and passwords in environment variables. Use synthetic data when testing the assistant.

## Limitations and Future Improvements

- Test the model on independent datasets.
- Improve image validation.
- Evaluate the model on more diverse retinal images.
- Improve API security and error handling.
- Further evaluate the Grad-CAM visualizations.

This project is a prototype and requires further testing and clinical validation before any real-world medical use.

## Acknowledgements

This project uses the APTOS 2019 Blindness Detection dataset for diabetic retinopathy classification research. Please follow the dataset's original usage and attribution terms.
