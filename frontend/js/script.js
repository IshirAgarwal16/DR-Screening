/* =========================================================
   DR SCREENING - FRONTEND JAVASCRIPT
   ========================================================= */


/* =========================================================
   BACKEND CONFIGURATION
   ========================================================= */

const BACKEND_URL = "http://localhost:8084";


/* =========================================================
   LOGIN PAGE
   ========================================================= */

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const emailElement =
            document.getElementById("email");

        const passwordElement =
            document.getElementById("password");

        const roleElement =
            document.querySelector(
                'input[name="role"]:checked'
            );


        if (!emailElement || !passwordElement || !roleElement) {

            alert("Please fill in all login details.");

            return;
        }


        const email =
            emailElement.value.trim();

        const password =
            passwordElement.value.trim();

        const role =
            roleElement.value;


        if (email === "" || password === "") {

            alert("Please enter your email and password.");

            return;
        }


        /*
         * TEMPORARY FRONTEND LOGIN
         *
         * Authentication will be connected to the
         * Spring Boot backend later.
         */

        localStorage.setItem(
            "userEmail",
            email
        );

        localStorage.setItem(
            "userRole",
            role
        );


        /*
         * Healthcare Worker
         */

        if (role === "Healthcare Worker") {

            window.location.href =
                "patient.html";

        }


        /*
         * Doctor
         */

        else if (role === "Doctor") {

            window.location.href =
                "doctor.html";

        }

        else {

            alert("Please select a valid role.");

        }

    });

}


/* =========================================================
   PATIENT REGISTRATION
   ========================================================= */

const patientForm =
    document.getElementById("patientForm");


if (patientForm) {

    patientForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            /* ---------------------------------------------
               GET FORM VALUES
               --------------------------------------------- */

            const nameElement =
                document.getElementById("patientName");

            const ageElement =
                document.getElementById("patientAge");

            const genderElement =
                document.getElementById("patientGender");

            const messageElement =
                document.getElementById("patientMessage");


            if (
                !nameElement ||
                !ageElement ||
                !genderElement
            ) {

                return;

            }


            const name =
                nameElement.value.trim();

            const age =
                Number(ageElement.value);

            const gender =
                genderElement.value;


            /* ---------------------------------------------
               VALIDATION
               --------------------------------------------- */

            if (name === "") {

                showPatientMessage(
                    "Please enter patient's name.",
                    "error"
                );

                return;

            }


            if (
                !age ||
                age < 1 ||
                age > 120
            ) {

                showPatientMessage(
                    "Please enter a valid age.",
                    "error"
                );

                return;

            }


            if (gender === "") {

                showPatientMessage(
                    "Please select patient's gender.",
                    "error"
                );

                return;

            }


            /* ---------------------------------------------
               SHOW LOADING MESSAGE
               --------------------------------------------- */

            showPatientMessage(
                "Registering patient...",
                "loading"
            );


            /* ---------------------------------------------
               CREATE PATIENT OBJECT
               --------------------------------------------- */

            const patientData = {

                name: name,

                age: age,

                gender: gender

            };


            try {

                /* -----------------------------------------
                   SEND DATA TO SPRING BOOT
                   ----------------------------------------- */

                const response =
                    await fetch(
                        BACKEND_URL + "/api/patients",
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify(
                                    patientData
                                )

                        }
                    );


                /* -----------------------------------------
                   CHECK RESPONSE
                   ----------------------------------------- */

                if (!response.ok) {

                    throw new Error(
                        "Patient registration failed."
                    );

                }


                /* -----------------------------------------
                   GET SAVED PATIENT
                   ----------------------------------------- */

                const patient =
                    await response.json();


                console.log(
                    "Patient registered:",
                    patient
                );


                /* -----------------------------------------
                   SAVE PATIENT INFORMATION
                   ----------------------------------------- */

                localStorage.setItem(
                    "patientId",
                    patient.id
                );

                localStorage.setItem(
                    "patientName",
                    patient.name
                );

                localStorage.setItem(
                    "patientAge",
                    patient.age
                );

                localStorage.setItem(
                    "patientGender",
                    patient.gender
                );


                /* -----------------------------------------
                   SUCCESS MESSAGE
                   ----------------------------------------- */

                showPatientMessage(
                    "Patient registered successfully!",
                    "success"
                );


                /* -----------------------------------------
                   REDIRECT TO SCREENING
                   ----------------------------------------- */

                setTimeout(
                    function () {

                        window.location.href =
                            "screening.html";

                    },
                    1000
                );


            }

            catch (error) {

                console.error(
                    "Registration error:",
                    error
                );


                showPatientMessage(
                    "Unable to connect to the backend. Make sure Spring Boot is running on port 8084.",
                    "error"
                );

            }

        }
    );

}


/* =========================================================
   PATIENT MESSAGE FUNCTION
   ========================================================= */

function showPatientMessage(
    message,
    type
) {

    const messageElement =
        document.getElementById(
            "patientMessage"
        );


    if (!messageElement) {

        return;

    }


    messageElement.innerText =
        message;


    if (type === "success") {

        messageElement.style.color =
            "#16a34a";

    }

    else if (type === "error") {

        messageElement.style.color =
            "#dc2626";

    }

    else if (type === "loading") {

        messageElement.style.color =
            "#2563eb";

    }

}


/* =========================================================
   HOME PAGE - START SCREENING BUTTON
   ========================================================= */

const startScreeningButton =
    document.querySelector(
        ".primary-btn"
    );


if (startScreeningButton) {

    startScreeningButton.addEventListener(
        "click",
        function () {

            /*
             * For now, send the user to login.
             */

            window.location.href =
                "login.html";

        }
    );

}


/* =========================================================
   HOME PAGE - LEARN MORE
   ========================================================= */

const learnMoreButton =
    document.querySelector(
        ".secondary-btn"
    );


if (learnMoreButton) {

    learnMoreButton.addEventListener(
        "click",
        function (event) {

            /*
             * If the button already has an anchor,
             * allow normal HTML behaviour.
             */

            const href =
                learnMoreButton.getAttribute(
                    "href"
                );


            if (
                href &&
                href !== "#" &&
                href.includes("#")
            ) {

                return;

            }

        }
    );

}


/* =========================================================
   LOGOUT
   ========================================================= */

const logoutLinks =
    document.querySelectorAll(
        'a[href="login.html"]'
    );


logoutLinks.forEach(
    function (link) {

        /*
         * Only clear login information when the
         * link is explicitly being used as logout.
         */

        if (
            link.textContent
                .trim()
                .toLowerCase()
                .includes("logout")
        ) {

            link.addEventListener(
                "click",
                function () {

                    localStorage.removeItem(
                        "userEmail"
                    );

                    localStorage.removeItem(
                        "userRole"
                    );

                    localStorage.removeItem(
                        "patientId"
                    );

                    localStorage.removeItem(
                        "patientName"
                    );

                    localStorage.removeItem(
                        "patientAge"
                    );

                    localStorage.removeItem(
                        "patientGender"
                    );

                }
            );

        }

    }
);


/* =========================================================
   DISPLAY REGISTERED PATIENT INFORMATION
   ========================================================= */

function loadPatientInformation() {

    const patientNameElement =
        document.getElementById(
            "displayPatientName"
        );

    const patientAgeElement =
        document.getElementById(
            "displayPatientAge"
        );

    const patientGenderElement =
        document.getElementById(
            "displayPatientGender"
        );


    const patientName =
        localStorage.getItem(
            "patientName"
        );

    const patientAge =
        localStorage.getItem(
            "patientAge"
        );

    const patientGender =
        localStorage.getItem(
            "patientGender"
        );


    if (
        patientNameElement &&
        patientName
    ) {

        patientNameElement.innerText =
            patientName;

    }


    if (
        patientAgeElement &&
        patientAge
    ) {

        patientAgeElement.innerText =
            patientAge;

    }


    if (
        patientGenderElement &&
        patientGender
    ) {

        patientGenderElement.innerText =
            patientGender;

    }

}


/* =========================================================
   RUN PATIENT INFORMATION FUNCTION
   ========================================================= */

loadPatientInformation();


/* =========================================================
   CONSOLE MESSAGE
   ========================================================= */

console.log(
    "DR Screening frontend loaded successfully."
);

console.log(
    "Backend:",
    BACKEND_URL
);

/* =========================================================
   SCREENING PAGE
   ========================================================= */

const fundusImage =
    document.getElementById("fundusImage");

const analyzeButton =
    document.getElementById("analyzeButton");

const uploadArea =
    document.getElementById("uploadArea");

const imagePreview =
    document.getElementById("imagePreview");

const imagePreviewContainer =
    document.getElementById(
        "imagePreviewContainer"
    );

const removeImage =
    document.getElementById("removeImage");

const loadingMessage =
    document.getElementById("loadingMessage");

const screeningMessage =
    document.getElementById(
        "screeningMessage"
    );


/* =========================================================
   LOAD PATIENT INFORMATION
   ========================================================= */

const screeningPatientName =
    document.getElementById(
        "screeningPatientName"
    );


if (screeningPatientName) {

    const patientName =
        localStorage.getItem(
            "patientName"
        );

    if (patientName) {

        screeningPatientName.innerText =
            patientName;

    }

}


/* =========================================================
   IMAGE SELECTION
   ========================================================= */

if (fundusImage) {

    fundusImage.addEventListener(
        "change",
        function () {

            const file =
                fundusImage.files[0];


            if (!file) {

                return;

            }


            /* Check file type */

            if (!file.type.startsWith("image/")) {

                showScreeningMessage(
                    "Please select a valid image file.",
                    "error"
                );

                fundusImage.value = "";

                return;

            }


            /* Create preview */

            const reader =
                new FileReader();


            reader.onload =
                function (event) {

                    imagePreview.src =
                        event.target.result;

                    imagePreviewContainer.style.display =
                        "block";

                    uploadArea.style.display =
                        "none";

                    analyzeButton.disabled =
                        false;

                    showScreeningMessage(
                        "Image selected. Ready for analysis.",
                        "success"
                    );

                };


            reader.readAsDataURL(file);

        }
    );

}


/* =========================================================
   REMOVE IMAGE
   ========================================================= */

if (removeImage) {

    removeImage.addEventListener(
        "click",
        function () {

            fundusImage.value = "";

            imagePreview.src = "";

            imagePreviewContainer.style.display =
                "none";

            uploadArea.style.display =
                "flex";

            analyzeButton.disabled =
                true;

            screeningMessage.innerText =
                "";

        }
    );

}


/* =========================================================
   ANALYZE IMAGE
   ========================================================= */

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        async function () {

            const file =
                fundusImage.files[0];


            if (!file) {

                showScreeningMessage(
                    "Please select a fundus image first.",
                    "error"
                );

                return;

            }


            const patientId =
                localStorage.getItem(
                    "patientId"
                );


            if (!patientId) {

                showScreeningMessage(
                    "Patient information not found. Please register the patient again.",
                    "error"
                );

                return;

            }


            /* ---------------------------------------------
               CREATE FORM DATA
               --------------------------------------------- */

            const formData =
                new FormData();


            formData.append(
                "file",
                file
            );

            formData.append(
                "patientId",
                patientId
            );


            /* ---------------------------------------------
               SHOW LOADING
               --------------------------------------------- */

            analyzeButton.disabled =
                true;

            loadingMessage.style.display =
                "block";

            screeningMessage.innerText =
                "";


            try {

                /* -----------------------------------------
                   SEND TO SPRING BOOT
                   ----------------------------------------- */

                const response =
                    await fetch(
                        BACKEND_URL +
                        "/api/ai/analyze",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                /* -----------------------------------------
                   CHECK RESPONSE
                   ----------------------------------------- */

                if (!response.ok) {

                    throw new Error(
                        "AI analysis request failed."
                    );

                }


                const result =
                    await response.json();


                console.log(
                    "AI Result:",
                    result
                );


                /* -----------------------------------------
                   HIDE LOADING
                   ----------------------------------------- */

                loadingMessage.style.display =
                    "none";


                /* -----------------------------------------
                   HANDLE RESULT
                   ----------------------------------------- */

                if (!result.success) {

                    handleFailedAnalysis(
                        result
                    );

                    analyzeButton.disabled =
                        false;

                    return;

                }


                /* -----------------------------------------
                   DISPLAY RESULT
                   ----------------------------------------- */

                displayScreeningResult(
                    result,
                    file
                );


            }

            catch (error) {

                console.error(
                    "AI analysis error:",
                    error
                );


                loadingMessage.style.display =
                    "none";


                analyzeButton.disabled =
                    false;


                showScreeningMessage(
                    "Unable to connect to the backend. Make sure Spring Boot is running on port 8084.",
                    "error"
                );

            }

        }
    );

}


/* =========================================================
   DISPLAY SCREENING RESULT
   ========================================================= */

function displayScreeningResult(
    result,
    file
) {

    const resultSection =
        document.getElementById(
            "resultSection"
        );


    const drClass =
        document.getElementById(
            "drClass"
        );

    const drGrade =
        document.getElementById(
            "drGrade"
        );

    const confidence =
        document.getElementById(
            "confidence"
        );

    const referableStatus =
        document.getElementById(
            "referableStatus"
        );

    const referableProbability =
        document.getElementById(
            "referableProbability"
        );

    const recommendation =
        document.getElementById(
            "recommendation"
        );

    const originalResultImage =
        document.getElementById(
            "originalResultImage"
        );

    const gradcamImage =
        document.getElementById(
            "gradcamImage"
        );

    const sharpness =
        document.getElementById(
            "sharpness"
        );

    const brightness =
        document.getElementById(
            "brightness"
        );

    const contrast =
        document.getElementById(
            "contrast"
        );


    /* ---------------------------------------------
       DR RESULT
       --------------------------------------------- */

    drClass.innerText =
        result.dr_class || "Unknown";


    drGrade.innerText =
        "Grade " +
        result.dr_grade;


    /* ---------------------------------------------
       CONFIDENCE
       --------------------------------------------- */

    confidence.innerText =
        result.confidence + "%";


    /* ---------------------------------------------
       REFERABLE STATUS
       --------------------------------------------- */

    referableStatus.innerText =
        result.referable_status;


    referableProbability.innerText =
        "Probability: " +
        result.referable_probability +
        "%";


    /* ---------------------------------------------
       RECOMMENDATION
       --------------------------------------------- */

    recommendation.innerText =
        result.recommendation;


    /* ---------------------------------------------
       ORIGINAL IMAGE
       --------------------------------------------- */

    const reader =
        new FileReader();


    reader.onload =
        function (event) {

            originalResultImage.src =
                event.target.result;

        };


    reader.readAsDataURL(file);


    /* ---------------------------------------------
       GRAD-CAM
       --------------------------------------------- */

    if (result.gradcam_image) {

        gradcamImage.src =
            "data:image/png;base64," +
            result.gradcam_image;

    }


    /* ---------------------------------------------
       QUALITY DETAILS
       --------------------------------------------- */

    if (result.quality_details) {

        sharpness.innerText =
            result.quality_details.sharpness;

        brightness.innerText =
            result.quality_details.brightness;

        contrast.innerText =
            result.quality_details.contrast;

    }


    /* ---------------------------------------------
       SHOW RESULT
       --------------------------------------------- */

    resultSection.style.display =
        "block";


    resultSection.scrollIntoView({
        behavior: "smooth"
    });


    showScreeningMessage(
        "Screening completed successfully.",
        "success"
    );

}


/* =========================================================
   FAILED ANALYSIS
   ========================================================= */

function handleFailedAnalysis(
    result
) {

    let message =
        result.message ||
        "Image could not be analyzed.";


    if (
        result.stage ===
        "fundus_validation"
    ) {

        message =
            "The uploaded image does not appear to be a fundus image. Please upload a retinal fundus photograph.";

    }


    else if (
        result.stage ===
        "quality_check"
    ) {

        message =
            "Fundus image quality is poor. Please capture another clearer image.";

    }


    showScreeningMessage(
        message,
        "error"
    );

}


/* =========================================================
   SCREENING MESSAGE
   ========================================================= */

function showScreeningMessage(
    message,
    type
) {

    if (!screeningMessage) {

        return;

    }


    screeningMessage.innerText =
        message;


    if (type === "success") {

        screeningMessage.style.color =
            "#16a34a";

    }

    else if (type === "error") {

        screeningMessage.style.color =
            "#dc2626";

    }

    else {

        screeningMessage.style.color =
            "#2563eb";

    }

}


/* =========================================================
   NEW SCREENING
   ========================================================= */

const newScreeningButton =
    document.getElementById(
        "newScreeningButton"
    );


if (newScreeningButton) {

    newScreeningButton.addEventListener(
        "click",
        function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });


            if (fundusImage) {

                fundusImage.value =
                    "";

            }


            if (imagePreview) {

                imagePreview.src =
                    "";

            }


            if (imagePreviewContainer) {

                imagePreviewContainer.style.display =
                    "none";

            }


            if (uploadArea) {

                uploadArea.style.display =
                    "flex";

            }


            if (analyzeButton) {

                analyzeButton.disabled =
                    true;

            }


            const resultSection =
                document.getElementById(
                    "resultSection"
                );


            if (resultSection) {

                resultSection.style.display =
                    "none";

            }

        }
    );

}

