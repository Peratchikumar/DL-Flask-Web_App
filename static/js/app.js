/* ============================================================
   VEHICLE DAMAGE AI
   YOLO26 + Flask Frontend
   ============================================================ */


/* ============================================================
   DOM ELEMENTS
   ============================================================ */

const fileInput =
    document.getElementById("fileInput");

const browseButton =
    document.getElementById("browseButton");

const dropZone =
    document.getElementById("dropZone");

const previewContainer =
    document.getElementById("previewContainer");

const imagePreview =
    document.getElementById("imagePreview");

const fileName =
    document.getElementById("fileName");

const removeButton =
    document.getElementById("removeButton");

const analyzeButton =
    document.getElementById("analyzeButton");

const errorMessage =
    document.getElementById("errorMessage");

const loadingOverlay =
    document.getElementById("loadingOverlay");

const resultsEmpty =
    document.getElementById("resultsEmpty");

const resultContent =
    document.getElementById("resultContent");

const detectionCount =
    document.getElementById("detectionCount");

const detectionList =
    document.getElementById("detectionList");

const resultFilename =
    document.getElementById("resultFilename");

const resultStatus =
    document.getElementById("resultStatus");


/* ============================================================
   CONFIGURATION
   ============================================================ */

const API_ENDPOINT = "/api/predict";

const MAX_FILE_SIZE =
    16 * 1024 * 1024; // 16 MB

const ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
];


/* ============================================================
   APPLICATION STATE
   ============================================================ */

let selectedFile = null;


/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    initializeApplication
);


function initializeApplication() {

    if (!fileInput || !browseButton || !dropZone) {
        console.error(
            "Required frontend elements are missing."
        );

        return;
    }

    setupFileSelection();

    setupDragAndDrop();

    setupRemoveButton();

    setupAnalyzeButton();

    setupKeyboardAccessibility();

}


/* ============================================================
   FILE SELECTION
   ============================================================ */

function setupFileSelection() {

    browseButton.addEventListener(
        "click",
        () => {
            fileInput.click();
        }
    );


    fileInput.addEventListener(
        "change",
        (event) => {

            const file =
                event.target.files[0];

            if (file) {
                handleFile(file);
            }

        }
    );

}


/* ============================================================
   DRAG AND DROP
   ============================================================ */

function setupDragAndDrop() {

    const dragEvents = [
        "dragenter",
        "dragover"
    ];


    dragEvents.forEach(
        (eventName) => {

            dropZone.addEventListener(
                eventName,
                handleDragEnter
            );

        }
    );


    const leaveEvents = [
        "dragleave",
        "drop"
    ];


    leaveEvents.forEach(
        (eventName) => {

            dropZone.addEventListener(
                eventName,
                handleDragLeave
            );

        }
    );


    dropZone.addEventListener(
        "drop",
        handleFileDrop
    );

}


function handleDragEnter(event) {

    event.preventDefault();

    event.stopPropagation();

    dropZone.classList.add(
        "dragover"
    );

}


function handleDragLeave(event) {

    event.preventDefault();

    event.stopPropagation();

    dropZone.classList.remove(
        "dragover"
    );

}


function handleFileDrop(event) {

    event.preventDefault();

    event.stopPropagation();

    dropZone.classList.remove(
        "dragover"
    );


    const files =
        event.dataTransfer.files;


    if (!files || files.length === 0) {
        return;
    }


    handleFile(files[0]);

}


/* ============================================================
   FILE VALIDATION
   ============================================================ */

function validateFile(file) {

    if (!file) {

        return {
            valid: false,
            message: "Please select an image."
        };

    }


    if (!ALLOWED_TYPES.includes(file.type)) {

        return {
            valid: false,
            message:
                "Unsupported file type. Please upload a JPG, PNG, or WEBP image."
        };

    }


    if (file.size > MAX_FILE_SIZE) {

        return {
            valid: false,
            message:
                "File is too large. The maximum allowed size is 16 MB."
        };

    }


    return {
        valid: true,
        message: ""
    };

}


/* ============================================================
   HANDLE SELECTED FILE
   ============================================================ */

function handleFile(file) {

    clearError();


    const validation =
        validateFile(file);


    if (!validation.valid) {

        showError(
            validation.message
        );

        return;
    }


    selectedFile = file;

    showImagePreview(file);

}


/* ============================================================
   IMAGE PREVIEW
   ============================================================ */

function showImagePreview(file) {

    const reader =
        new FileReader();


    reader.onload = function(event) {

        imagePreview.src =
            event.target.result;

        imagePreview.alt =
            `Preview of ${file.name}`;

        fileName.textContent =
            file.name;


        dropZone.style.display =
            "none";


        previewContainer.classList.add(
            "active"
        );


        analyzeButton.disabled =
            false;

    };


    reader.onerror = function() {

        showError(
            "Unable to preview the selected image."
        );

    };


    reader.readAsDataURL(file);

}


/* ============================================================
   REMOVE SELECTED FILE
   ============================================================ */

function setupRemoveButton() {

    removeButton.addEventListener(
        "click",
        removeSelectedFile
    );

}


function removeSelectedFile() {

    selectedFile = null;

    fileInput.value = "";

    imagePreview.src = "";

    imagePreview.alt =
        "Vehicle preview";


    previewContainer.classList.remove(
        "active"
    );


    dropZone.style.display =
        "flex";


    analyzeButton.disabled =
        true;


    clearError();


    resetResults();

}


/* ============================================================
   ANALYZE BUTTON
   ============================================================ */

function setupAnalyzeButton() {

    analyzeButton.addEventListener(
        "click",
        analyzeVehicle
    );

}


async function analyzeVehicle() {

    if (!selectedFile) {

        showError(
            "Please select a vehicle image first."
        );

        return;
    }


    clearError();

    setLoading(true);


    const formData =
        new FormData();


    formData.append(
        "file",
        selectedFile
    );


    try {

        const response =
            await fetch(
                API_ENDPOINT,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await parseResponse(response);


        if (!response.ok) {

            throw new Error(
                data.message ||
                data.error ||
                "Vehicle damage prediction failed."
            );

        }


        displayResults(data);

    }

    catch (error) {

        console.error(
            "Vehicle damage detection error:",
            error
        );


        showError(
            error.message ||
            "Unable to process the image. Please try again."
        );

    }

    finally {

        setLoading(false);

    }

}


/* ============================================================
   PARSE API RESPONSE
   ============================================================ */

async function parseResponse(response) {

    const contentType =
        response.headers.get(
            "content-type"
        );


    if (
        contentType &&
        contentType.includes(
            "application/json"
        )
    ) {

        return await response.json();

    }


    const text =
        await response.text();


    return {
        success: false,
        message:
            text ||
            "The server returned an unexpected response."
    };

}


/* ============================================================
   DISPLAY DETECTION RESULTS
   ============================================================ */

function displayResults(data) {

    resultsEmpty.style.display =
        "none";


    resultContent.classList.add(
        "active"
    );


    const detections =
        Array.isArray(data.detections)
            ? data.detections
            : [];


    detectionCount.textContent =
        detections.length;


    resultFilename.textContent =
        data.filename ||
        "Vehicle analysis";


    detectionList.innerHTML =
        "";


    if (detections.length === 0) {

        displayNoDamage();

        return;
    }


    resultStatus.textContent =
        "Damage Found";


    detections.forEach(
        (detection) => {

            createDetectionItem(
                detection
            );

        }
    );

}


/* ============================================================
   DISPLAY NO DAMAGE
   ============================================================ */

function displayNoDamage() {

    resultStatus.textContent =
        "Clear";


    detectionList.innerHTML = `
        <div class="no-damage">
            ✓ No visible vehicle damage
            detected by the AI model.
        </div>
    `;

}


/* ============================================================
   CREATE DETECTION ITEM
   ============================================================ */

function createDetectionItem(
    detection
) {

    const className =
        formatClassName(
            detection.class_name ||
            "Unknown damage"
        );


    const confidence =
        getConfidencePercentage(
            detection
        );


    const item =
        document.createElement(
            "div"
        );


    item.className =
        "detection-item";


    const top =
        document.createElement(
            "div"
        );


    top.className =
        "detection-top";


    const name =
        document.createElement(
            "span"
        );


    name.className =
        "damage-name";


    name.textContent =
        className;


    const confidenceText =
        document.createElement(
            "span"
        );


    confidenceText.className =
        "confidence";


    confidenceText.textContent =
        `${confidence.toFixed(1)}%`;


    top.appendChild(name);

    top.appendChild(
        confidenceText
    );


    const bar =
        document.createElement(
            "div"
        );


    bar.className =
        "confidence-bar";


    const fill =
        document.createElement(
            "div"
        );


    fill.className =
        "confidence-fill";


    fill.style.width =
        `${Math.min(
            Math.max(confidence, 0),
            100
        )}%`;


    bar.appendChild(fill);


    item.appendChild(top);

    item.appendChild(bar);


    detectionList.appendChild(
        item
    );

}


/* ============================================================
   CONFIDENCE CALCULATION
   ============================================================ */

function getConfidencePercentage(
    detection
) {

    if (
        detection.confidence_percent !==
        undefined &&
        detection.confidence_percent !==
        null
    ) {

        return clamp(
            Number(
                detection.confidence_percent
            ),
            0,
            100
        );

    }


    const confidence =
        Number(
            detection.confidence || 0
        );


    return clamp(
        confidence * 100,
        0,
        100
    );

}


/* ============================================================
   FORMAT DAMAGE CLASS NAME
   ============================================================ */

function formatClassName(name) {

    return String(name)
        .replaceAll("-", " ")
        .replaceAll("_", " ")
        .replace(/\s+/g, " ")
        .trim()
        .replace(
            /\b\w/g,
            character =>
                character.toUpperCase()
        );

}


/* ============================================================
   CLAMP VALUE
   ============================================================ */

function clamp(
    value,
    minimum,
    maximum
) {

    return Math.min(
        Math.max(
            value,
            minimum
        ),
        maximum
    );

}


/* ============================================================
   LOADING STATE
   ============================================================ */

function setLoading(
    isLoading
) {

    if (isLoading) {

        loadingOverlay.classList.add(
            "active"
        );


        analyzeButton.disabled =
            true;


        analyzeButton.textContent =
            "Analyzing...";

    }

    else {

        loadingOverlay.classList.remove(
            "active"
        );


        analyzeButton.disabled =
            !selectedFile;


        analyzeButton.textContent =
            "🔍 Analyze Vehicle Damage";

    }

}


/* ============================================================
   ERROR HANDLING
   ============================================================ */

function showError(
    message
) {

    errorMessage.textContent =
        message;


    errorMessage.classList.add(
        "active"
    );

}


function clearError() {

    errorMessage.textContent =
        "";


    errorMessage.classList.remove(
        "active"
    );

}


/* ============================================================
   RESET RESULTS
   ============================================================ */

function resetResults() {

    resultsEmpty.style.display =
        "flex";


    resultContent.classList.remove(
        "active"
    );


    detectionCount.textContent =
        "0";


    resultStatus.textContent =
        "Ready";


    resultFilename.textContent =
        "Analysis result";


    detectionList.innerHTML =
        "";

}


/* ============================================================
   KEYBOARD ACCESSIBILITY
   ============================================================ */

function setupKeyboardAccessibility() {

    dropZone.setAttribute(
        "tabindex",
        "0"
    );


    dropZone.setAttribute(
        "role",
        "button"
    );


    dropZone.setAttribute(
        "aria-label",
        "Upload vehicle image"
    );


    dropZone.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" ||
                event.key === " "
            ) {

                event.preventDefault();

                fileInput.click();

            }

        }
    );

}


/* ============================================================
   PREVENT UNWANTED DROP BEHAVIOR
   ============================================================ */

document.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

    }
);


document.addEventListener(
    "drop",
    (event) => {

        if (
            !dropZone.contains(
                event.target
            )
        ) {

            event.preventDefault();

        }

    }
);