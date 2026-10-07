const BACKEND_URL = "http://localhost:8084";

/* =========================
   LOGIN
========================= */

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
}

function handleLogin(event) {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const roleInput = document.querySelector('input[name="role"]:checked');

    if (!emailInput || !passwordInput || !roleInput) {
        alert("Please fill in all login details.");
        return;
    }

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const role = roleInput.value;

    if (!email || !password) {
        alert("Please enter your email and password.");
        return;
    }

    localStorage.setItem("userEmail", email);
    localStorage.setItem("userRole", role);

    if (role === "Healthcare Worker") {
        window.location.href = "patient.html";
    } else if (role === "Doctor") {
        window.location.href = "doctor.html";
    } else {
        alert("Please select a valid role.");
    }
}


/* =========================
   PATIENT REGISTRATION
========================= */

const patientForm = document.getElementById("patientForm");

if (patientForm) {
    patientForm.addEventListener("submit", registerPatient);
}

async function registerPatient(event) {
    event.preventDefault();

    const patientIdInput = document.getElementById("patientId");
    const nameInput = document.getElementById("patientName");
    const ageInput = document.getElementById("patientAge");
    const genderInput = document.getElementById("patientGender");

    if (!patientIdInput || !nameInput || !ageInput || !genderInput) {
        return;
    }

    const patientId = Number(patientIdInput.value);
    const name = nameInput.value.trim();
    const age = Number(ageInput.value);
    const gender = genderInput.value;

    if (!patientId || patientId < 1) {
        showPatientMessage("Please enter a valid Patient ID.", "error");
        return;
    }

    if (!name) {
        showPatientMessage("Please enter patient's name.", "error");
        return;
    }

    if (!age || age < 1 || age > 120) {
        showPatientMessage("Please enter a valid age.", "error");
        return;
    }

    if (!gender) {
        showPatientMessage("Please select patient's gender.", "error");
        return;
    }

    showPatientMessage("Registering patient...", "loading");

    const patientData = {
        id: patientId,
        name: name,
        age: age,
        gender: gender
    };

    try {
        const response = await fetch(
            `${BACKEND_URL}/api/patients`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(patientData)
            }
        );

        if (response.status === 409) {
            showPatientMessage(
                "This Patient ID already exists. Please enter a different ID.",
                "error"
            );
            return;
        }

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend error:", errorText);

            showPatientMessage(
                "Patient registration failed.",
                "error"
            );
            return;
        }

        const patient = await response.json();

        localStorage.setItem("patientId", patient.id);
        localStorage.setItem("patientName", patient.name);
        localStorage.setItem("patientAge", patient.age);
        localStorage.setItem("patientGender", patient.gender);

        showPatientMessage(
            "Patient registered successfully!",
            "success"
        );

        setTimeout(() => {
            window.location.href = "screening.html";
        }, 1000);

    } catch (error) {
        console.error("Registration error:", error);

        showPatientMessage(
            "Unable to connect to the backend. Make sure Spring Boot is running on port 8084.",
            "error"
        );
    }
}


/* =========================
   PATIENT MESSAGE
========================= */

function showPatientMessage(message, type) {
    const element = document.getElementById("patientMessage");

    if (!element) {
        return;
    }

    element.innerText = message;

    const messageColors = {
        success: "#16a34a",
        error: "#dc2626",
        loading: "#2563eb"
    };

    element.style.color = messageColors[type] || "#2563eb";
}


/* =========================
   HOME PAGE
========================= */

const startScreeningButton =
    document.querySelector(".primary-btn");

if (startScreeningButton) {
    startScreeningButton.addEventListener("click", () => {
        window.location.href = "login.html";
    });
}

const learnMoreButton =
    document.querySelector(".secondary-btn");

if (learnMoreButton) {
    learnMoreButton.addEventListener("click", () => {
        const href = learnMoreButton.getAttribute("href");

        if (href && href !== "#" && href.includes("#")) {
            return;
        }
    });
}


/* =========================
   LOGOUT
========================= */

const logoutLinks =
    document.querySelectorAll('a[href="login.html"]');

logoutLinks.forEach((link) => {
    const isLogout =
        link.textContent.trim().toLowerCase().includes("logout");

    if (!isLogout) {
        return;
    }

    link.addEventListener("click", clearUserData);
});

function clearUserData() {
    const keys = [
        "userEmail",
        "userRole",
        "patientId",
        "patientName",
        "patientAge",
        "patientGender"
    ];

    keys.forEach((key) => {
        localStorage.removeItem(key);
    });
}


/* =========================
   PATIENT INFORMATION
========================= */

function loadPatientInformation() {
    const elements = {
        name: document.getElementById("displayPatientName"),
        age: document.getElementById("displayPatientAge"),
        gender: document.getElementById("displayPatientGender")
    };

    const patient = {
        name: localStorage.getItem("patientName"),
        age: localStorage.getItem("patientAge"),
        gender: localStorage.getItem("patientGender")
    };

    if (elements.name && patient.name) {
        elements.name.innerText = patient.name;
    }

    if (elements.age && patient.age) {
        elements.age.innerText = patient.age;
    }

    if (elements.gender && patient.gender) {
        elements.gender.innerText = patient.gender;
    }
}

loadPatientInformation();


/* =========================
   SCREENING PAGE ELEMENTS
========================= */

const fundusImage = document.getElementById("fundusImage");
const analyzeButton = document.getElementById("analyzeButton");
const uploadArea = document.getElementById("uploadArea");
const imagePreview = document.getElementById("imagePreview");
const imagePreviewContainer =
    document.getElementById("imagePreviewContainer");
const removeImage = document.getElementById("removeImage");
const loadingMessage = document.getElementById("loadingMessage");
const screeningMessage =
    document.getElementById("screeningMessage");


/* =========================
   SCREENING PATIENT
========================= */

const screeningPatientName =
    document.getElementById("screeningPatientName");

if (screeningPatientName) {
    const patientName =
        localStorage.getItem("patientName");

    if (patientName) {
        screeningPatientName.innerText = patientName;
    }
}


/* =========================
   IMAGE SELECTION
========================= */

if (fundusImage) {
    fundusImage.addEventListener("change", handleImageSelection);
}

function handleImageSelection() {
    const file = fundusImage.files[0];

    if (!file) {
        return;
    }

    if (!file.type.startsWith("image/")) {
        showScreeningMessage(
            "Please select a valid image file.",
            "error"
        );

        fundusImage.value = "";
        return;
    }

    const reader = new FileReader();

    reader.onload = (event) => {
        if (imagePreview) {
            imagePreview.src = event.target.result;
        }

        if (imagePreviewContainer) {
            imagePreviewContainer.style.display = "block";
        }

        if (uploadArea) {
            uploadArea.style.display = "none";
        }

        if (analyzeButton) {
            analyzeButton.disabled = false;
        }

        showScreeningMessage(
            "Image selected. Ready for analysis.",
            "success"
        );
    };

    reader.readAsDataURL(file);
}


/* =========================
   REMOVE IMAGE
========================= */

if (removeImage) {
    removeImage.addEventListener("click", resetImageSelection);
}

function resetImageSelection() {
    if (fundusImage) {
        fundusImage.value = "";
    }

    if (imagePreview) {
        imagePreview.src = "";
    }

    if (imagePreviewContainer) {
        imagePreviewContainer.style.display = "none";
    }

    if (uploadArea) {
        uploadArea.style.display = "flex";
    }

    if (analyzeButton) {
        analyzeButton.disabled = true;
    }

    if (screeningMessage) {
        screeningMessage.innerText = "";
    }
}


/* =========================
   IMAGE ANALYSIS
========================= */

if (analyzeButton) {
    analyzeButton.addEventListener("click", analyzeFundusImage);
}

async function analyzeFundusImage() {
    const file = fundusImage?.files[0];

    if (!file) {
        showScreeningMessage(
            "Please select a fundus image first.",
            "error"
        );
        return;
    }

    const patientId =
        localStorage.getItem("patientId");

    if (!patientId) {
        showScreeningMessage(
            "Patient information not found. Please register the patient again.",
            "error"
        );
        return;
    }

    const formData = new FormData();

    formData.append("file", file);
    formData.append("patientId", patientId);

    setAnalysisLoading(true);

    try {
        const response = await fetch(
            `${BACKEND_URL}/api/ai/analyze`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("AI analysis request failed.");
        }

        const result = await response.json();

        console.log("AI Result:", result);

        setAnalysisLoading(false);

        if (!result.success) {
            handleFailedAnalysis(result);

            if (analyzeButton) {
                analyzeButton.disabled = false;
            }

            return;
        }

        displayScreeningResult(result, file);

    } catch (error) {
        console.error("AI analysis error:", error);

        setAnalysisLoading(false);

        if (analyzeButton) {
            analyzeButton.disabled = false;
        }

        showScreeningMessage(
            "Unable to connect to the backend. Make sure Spring Boot is running on port 8084.",
            "error"
        );
    }
}


/* =========================
   LOADING STATE
========================= */

function setAnalysisLoading(isLoading) {
    if (analyzeButton) {
        analyzeButton.disabled = isLoading;
    }

    if (loadingMessage) {
        loadingMessage.style.display =
            isLoading ? "block" : "none";
    }

    if (screeningMessage && isLoading) {
        screeningMessage.innerText = "";
    }
}


/* =========================
   DISPLAY SCREENING RESULT
========================= */

function displayScreeningResult(result, file) {
    const resultSection =
        document.getElementById("resultSection");

    const drClass =
        document.getElementById("drClass");

    const drGrade =
        document.getElementById("drGrade");

    const confidence =
        document.getElementById("confidence");

    const referableStatus =
        document.getElementById("referableStatus");

    const referableProbability =
        document.getElementById("referableProbability");

    const recommendation =
        document.getElementById("recommendation");

    const originalResultImage =
        document.getElementById("originalResultImage");

    const gradcamImage =
        document.getElementById("gradcamImage");

    const sharpness =
        document.getElementById("sharpness");

    const brightness =
        document.getElementById("brightness");

    const contrast =
        document.getElementById("contrast");


    if (drClass) {
        drClass.innerText =
            result.dr_class || "Unknown";
    }

    if (drGrade) {
        drGrade.innerText =
            `Grade ${result.dr_grade}`;
    }

    if (confidence) {
        confidence.innerText =
            `${result.confidence}%`;
    }

    if (referableStatus) {
        referableStatus.innerText =
            result.referable_status;
    }

    if (referableProbability) {
        referableProbability.innerText =
            `Probability: ${result.referable_probability}%`;
    }

    if (recommendation) {
        recommendation.innerText =
            result.recommendation;
    }


    if (originalResultImage) {
        const reader = new FileReader();

        reader.onload = (event) => {
            originalResultImage.src =
                event.target.result;
        };

        reader.readAsDataURL(file);
    }


    if (gradcamImage && result.gradcam_image) {
        gradcamImage.src =
            `data:image/png;base64,${result.gradcam_image}`;
    }


    if (result.quality_details) {
        if (sharpness) {
            sharpness.innerText =
                result.quality_details.sharpness;
        }

        if (brightness) {
            brightness.innerText =
                result.quality_details.brightness;
        }

        if (contrast) {
            contrast.innerText =
                result.quality_details.contrast;
        }
    }


    if (resultSection) {
        resultSection.style.display = "block";

        resultSection.scrollIntoView({
            behavior: "smooth"
        });
    }

    showScreeningMessage(
        "Screening completed successfully.",
        "success"
    );
}


/* =========================
   FAILED ANALYSIS
========================= */

function handleFailedAnalysis(result) {
    let message =
        result.message ||
        "Image could not be analyzed.";

    if (result.stage === "fundus_validation") {
        message =
            "The uploaded image does not appear to be a fundus image. Please upload a retinal fundus photograph.";
    } else if (result.stage === "quality_check") {
        message =
            "Fundus image quality is poor. Please capture another clearer image.";
    }

    showScreeningMessage(message, "error");
}


/* =========================
   SCREENING MESSAGE
========================= */

function showScreeningMessage(message, type) {
    if (!screeningMessage) {
        return;
    }

    screeningMessage.innerText = message;

    const colors = {
        success: "#16a34a",
        error: "#dc2626",
        loading: "#2563eb"
    };

    screeningMessage.style.color =
        colors[type] || colors.loading;
}


/* =========================
   NEW SCREENING
========================= */

const newScreeningButton =
    document.getElementById("newScreeningButton");

if (newScreeningButton) {
    newScreeningButton.addEventListener(
        "click",
        startNewScreening
    );
}

function startNewScreening() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    if (fundusImage) {
        fundusImage.value = "";
    }

    if (imagePreview) {
        imagePreview.src = "";
    }

    if (imagePreviewContainer) {
        imagePreviewContainer.style.display = "none";
    }

    if (uploadArea) {
        uploadArea.style.display = "flex";
    }

    if (analyzeButton) {
        analyzeButton.disabled = true;
    }

    const resultSection =
        document.getElementById("resultSection");

    if (resultSection) {
        resultSection.style.display = "none";
    }

    if (screeningMessage) {
        screeningMessage.innerText = "";
    }

    if (loadingMessage) {
        loadingMessage.style.display = "none";
    }
}


/* =========================
   FRONTEND STATUS
========================= */

console.log("DR Screening frontend loaded successfully.");
console.log("Backend:", BACKEND_URL);