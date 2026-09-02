/* =========================================================
   DRIVEINSPECT
   Premium AI Vehicle Damage Detection
   script.js
   ========================================================= */

"use strict";


/* =========================================================
   1. CONFIGURATION
   ========================================================= */

const MAX_FILE_SIZE = 100 * 1024 * 1024;

const ALLOWED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp"
];

const ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/bmp"
];


/* =========================================================
   2. DOM ELEMENTS
   ========================================================= */

const uploadZone =
    document.getElementById("uploadZone");

const browseButton =
    document.getElementById("browseButton");

const fileInput =
    document.getElementById("fileInput");

const selectedFile =
    document.getElementById("selectedFile");

const selectedImage =
    document.getElementById("selectedImage");

const fileName =
    document.getElementById("fileName");

const fileSize =
    document.getElementById("fileSize");

const removeFile =
    document.getElementById("removeFile");

const detectButton =
    document.getElementById("detectButton");

const detectButtonText =
    document.getElementById("detectButtonText");

const buttonLoader =
    document.getElementById("buttonLoader");

const progressSection =
    document.getElementById("progressSection");

const progressText =
    document.getElementById("progressText");

const progressPercent =
    document.getElementById("progressPercent");

const progressBar =
    document.getElementById("progressBar");

const errorMessage =
    document.getElementById("errorMessage");

const errorText =
    document.getElementById("errorText");

const closeError =
    document.getElementById("closeError");

const resultsSection =
    document.getElementById("resultsSection");

const resultMessage =
    document.getElementById("resultMessage");

const resultImage =
    document.getElementById("resultImage");

const mediaPlaceholder =
    document.getElementById("mediaPlaceholder");

const totalDetections =
    document.getElementById("totalDetections");

const averageConfidence =
    document.getElementById("averageConfidence");

const damageTypeCount =
    document.getElementById("damageTypeCount");

const damageList =
    document.getElementById("damageList");

const detectionList =
    document.getElementById("detectionList");

const detectionCountLabel =
    document.getElementById("detectionCountLabel");

const openResultButton =
    document.getElementById("openResultButton");

const newDetectionButton =
    document.getElementById("newDetectionButton");


/* =========================================================
   3. APPLICATION STATE
   ========================================================= */

let selectedFileObject = null;

let selectedImageURL = null;

let currentResultURL = null;

let isProcessing = false;


/* =========================================================
   4. INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeUpload();

        initializeButtons();

        initializeDragAndDrop();

        initializeKeyboardSupport();

    }
);


/* =========================================================
   5. UPLOAD INITIALIZATION
   ========================================================= */

function initializeUpload() {

    if (browseButton) {

        browseButton.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

                openFilePicker();

            }
        );

    }


    if (fileInput) {

        fileInput.addEventListener(
            "change",
            handleFileSelection
        );

    }

}


/* =========================================================
   6. BUTTON INITIALIZATION
   ========================================================= */

function initializeButtons() {

    if (removeFile) {

        removeFile.addEventListener(
            "click",
            (event) => {

                event.stopPropagation();

                resetSelectedFile();

            }
        );

    }


    if (detectButton) {

        detectButton.addEventListener(
            "click",
            detectVehicleDamage
        );

    }


    if (closeError) {

        closeError.addEventListener(
            "click",
            hideError
        );

    }


    if (openResultButton) {

        openResultButton.addEventListener(
            "click",
            openResult
        );

    }


    if (newDetectionButton) {

        newDetectionButton.addEventListener(
            "click",
            startNewInspection
        );

    }

}


/* =========================================================
   7. OPEN FILE PICKER
   ========================================================= */

function openFilePicker() {

    if (!fileInput || isProcessing) {
        return;
    }

    fileInput.click();

}


/* =========================================================
   8. DRAG AND DROP
   ========================================================= */

function initializeDragAndDrop() {

    if (!uploadZone) {
        return;
    }


    uploadZone.addEventListener(
        "dragenter",
        handleDragEnter
    );


    uploadZone.addEventListener(
        "dragover",
        handleDragOver
    );


    uploadZone.addEventListener(
        "dragleave",
        handleDragLeave
    );


    uploadZone.addEventListener(
        "drop",
        handleDrop
    );


    uploadZone.addEventListener(
        "click",
        (event) => {

            if (
                event.target.closest(
                    ".browse-link"
                )
            ) {
                return;
            }


            if (!isProcessing) {
                openFilePicker();
            }

        }
    );

}


/* =========================================================
   9. DRAG ENTER
   ========================================================= */

function handleDragEnter(event) {

    event.preventDefault();

    event.stopPropagation();

    if (isProcessing) {
        return;
    }

    uploadZone.classList.add(
        "drag-over"
    );

}


/* =========================================================
   10. DRAG OVER
   ========================================================= */

function handleDragOver(event) {

    event.preventDefault();

    event.stopPropagation();

    if (isProcessing) {
        return;
    }

    event.dataTransfer.dropEffect =
        "copy";

    uploadZone.classList.add(
        "drag-over"
    );

}


/* =========================================================
   11. DRAG LEAVE
   ========================================================= */

function handleDragLeave(event) {

    event.preventDefault();

    event.stopPropagation();

    if (
        !uploadZone.contains(
            event.relatedTarget
        )
    ) {

        uploadZone.classList.remove(
            "drag-over"
        );

    }

}


/* =========================================================
   12. DROP
   ========================================================= */

function handleDrop(event) {

    event.preventDefault();

    event.stopPropagation();

    uploadZone.classList.remove(
        "drag-over"
    );


    if (isProcessing) {
        return;
    }


    const files =
        event.dataTransfer.files;


    if (!files || files.length === 0) {

        showError(
            "No image was dropped."
        );

        return;

    }


    handleSelectedFile(
        files[0]
    );

}


/* =========================================================
   13. FILE INPUT CHANGE
   ========================================================= */

function handleFileSelection(event) {

    const files =
        event.target.files;


    if (!files || files.length === 0) {
        return;
    }


    handleSelectedFile(
        files[0]
    );

}


/* =========================================================
   14. HANDLE SELECTED FILE
   ========================================================= */

function handleSelectedFile(file) {

    hideError();


    if (isProcessing) {
        return;
    }


    /* -----------------------------------------------------
       CHECK FILE
    ----------------------------------------------------- */

    if (!file) {

        showError(
            "Please select an image."
        );

        return;

    }


    /* -----------------------------------------------------
       CHECK FILE TYPE
    ----------------------------------------------------- */

    const extension =
        getFileExtension(
            file.name
        );


    const validExtension =
        ALLOWED_EXTENSIONS.includes(
            extension
        );


    const validMime =
        ALLOWED_MIME_TYPES.includes(
            file.type
        );


    if (
        !validExtension &&
        !validMime
    ) {

        showError(
            "Unsupported image format. Please use JPG, JPEG, PNG, WEBP, or BMP."
        );

        resetFileInput();

        return;

    }


    /* -----------------------------------------------------
       CHECK FILE SIZE
    ----------------------------------------------------- */

    if (file.size > MAX_FILE_SIZE) {

        showError(
            "Image is too large. Maximum file size is 100 MB."
        );

        resetFileInput();

        return;

    }


    /* -----------------------------------------------------
       CHECK EMPTY FILE
    ----------------------------------------------------- */

    if (file.size === 0) {

        showError(
            "The selected image is empty."
        );

        resetFileInput();

        return;

    }


    /* -----------------------------------------------------
       STORE FILE
    ----------------------------------------------------- */

    selectedFileObject = file;


    /* -----------------------------------------------------
       CREATE PREVIEW
    ----------------------------------------------------- */

    createImagePreview(file);


    /* -----------------------------------------------------
       UPDATE UI
    ----------------------------------------------------- */

    if (selectedFile) {

        selectedFile.hidden = false;

    }


    if (uploadZone) {

        uploadZone.style.display =
            "none";

    }


    if (detectButton) {

        detectButton.disabled = false;

    }


    /* -----------------------------------------------------
       HIDE OLD RESULTS
    ----------------------------------------------------- */

    hideResults();

}


/* =========================================================
   15. CREATE IMAGE PREVIEW
   ========================================================= */

function createImagePreview(file) {

    if (!selectedImage) {
        return;
    }


    if (selectedImageURL) {

        URL.revokeObjectURL(
            selectedImageURL
        );

    }


    selectedImageURL =
        URL.createObjectURL(file);


    selectedImage.src =
        selectedImageURL;


    selectedImage.alt =
        file.name;


    if (fileName) {

        fileName.textContent =
            file.name;

    }


    if (fileSize) {

        fileSize.textContent =
            formatFileSize(
                file.size
            );

    }

}


/* =========================================================
   16. RESET SELECTED FILE
   ========================================================= */

function resetSelectedFile() {

    selectedFileObject = null;


    if (selectedImageURL) {

        URL.revokeObjectURL(
            selectedImageURL
        );

        selectedImageURL = null;

    }


    if (selectedImage) {

        selectedImage.removeAttribute(
            "src"
        );

    }


    if (fileName) {

        fileName.textContent =
            "No image selected";

    }


    if (fileSize) {

        fileSize.textContent =
            "0 MB";

    }


    if (selectedFile) {

        selectedFile.hidden = true;

    }


    if (uploadZone) {

        uploadZone.style.display =
            "";

    }


    if (detectButton) {

        detectButton.disabled = true;

    }


    resetFileInput();

}


/* =========================================================
   17. RESET FILE INPUT
   ========================================================= */

function resetFileInput() {

    if (fileInput) {

        fileInput.value = "";

    }

}


/* =========================================================
   18. DETECT VEHICLE DAMAGE
   ========================================================= */

async function detectVehicleDamage() {

    if (
        !selectedFileObject ||
        isProcessing
    ) {

        return;

    }


    hideError();

    hideResults();

    isProcessing = true;


    setProcessingState(
        true
    );


    simulateProgress();


    const formData =
        new FormData();


    formData.append(
        "file",
        selectedFileObject
    );


    try {

        const response =
            await fetch(
                "/predict",
                {
                    method: "POST",
                    body: formData
                }
            );


        let data = null;


        try {

            data =
                await response.json();

        } catch (jsonError) {

            throw new Error(
                "The server returned an invalid response."
            );

        }


        if (
            !response.ok ||
            !data ||
            data.success !== true
        ) {

            throw new Error(
                data?.error ||
                data?.message ||
                "Vehicle damage detection failed."
            );

        }


        /* -------------------------------------------------
           COMPLETE PROGRESS
        ------------------------------------------------- */

        setProgress(
            100,
            "Detection completed successfully."
        );


        await delay(
            350
        );


        /* -------------------------------------------------
           RENDER RESULTS
        ------------------------------------------------- */

        renderResults(
            data
        );


    } catch (error) {

        console.error(
            "Detection error:",
            error
        );


        stopProgress();


        showError(
            error.message ||
            "Unable to process the image. Please try again."
        );


    } finally {

        isProcessing = false;

        setProcessingState(
            false
        );

    }

}


/* =========================================================
   19. PROCESSING STATE
   ========================================================= */

function setProcessingState(
    processing
) {

    isProcessing =
        processing;


    if (detectButton) {

        detectButton.disabled =
            processing ||
            !selectedFileObject;

    }


    if (detectButtonText) {

        detectButtonText.textContent =
            processing
                ? "Analyzing vehicle..."
                : "Analyze Vehicle";

    }


    if (buttonLoader) {

        buttonLoader.hidden =
            !processing;

    }


    if (processing) {

        if (uploadZone) {

            uploadZone.style.pointerEvents =
                "none";

            uploadZone.style.opacity =
                "0.65";

        }

    } else {

        if (uploadZone) {

            uploadZone.style.pointerEvents =
                "";

            uploadZone.style.opacity =
                "";

        }

    }

}


/* =========================================================
   20. PROGRESS SIMULATION
   ========================================================= */

let progressTimer = null;

let simulatedProgress = 0;


function simulateProgress() {

    stopProgressTimer();


    simulatedProgress = 5;


    setProgress(
        simulatedProgress,
        "Preparing vehicle image..."
    );


    progressTimer =
        setInterval(
            () => {

                if (!isProcessing) {
                    return;
                }


                if (
                    simulatedProgress < 25
                ) {

                    simulatedProgress +=
                        Math.random() * 4 + 2;

                    setProgress(
                        simulatedProgress,
                        "Uploading image..."
                    );

                } else if (
                    simulatedProgress < 55
                ) {

                    simulatedProgress +=
                        Math.random() * 3 + 1;

                    setProgress(
                        simulatedProgress,
                        "Running YOLO26 detection..."
                    );

                } else if (
                    simulatedProgress < 78
                ) {

                    simulatedProgress +=
                        Math.random() * 2 + 0.7;

                    setProgress(
                        simulatedProgress,
                        "Analyzing visible damage..."
                    );

                } else if (
                    simulatedProgress < 92
                ) {

                    simulatedProgress +=
                        Math.random() * 1.2 + 0.3;

                    setProgress(
                        simulatedProgress,
                        "Preparing inspection report..."
                    );

                }


            },
            450
        );

}


/* =========================================================
   21. STOP PROGRESS TIMER
   ========================================================= */

function stopProgressTimer() {

    if (progressTimer) {

        clearInterval(
            progressTimer
        );

        progressTimer = null;

    }

}


/* =========================================================
   22. SET PROGRESS
   ========================================================= */

function setProgress(
    percentage,
    message
) {

    const safePercentage =
        Math.min(
            100,
            Math.max(
                0,
                percentage
            )
        );


    if (progressSection) {

        progressSection.hidden =
            false;

    }


    if (progressText) {

        progressText.textContent =
            message;

    }


    if (progressPercent) {

        progressPercent.textContent =
            `${Math.round(safePercentage)}%`;

    }


    if (progressBar) {

        progressBar.style.width =
            `${safePercentage}%`;

    }

}


/* =========================================================
   23. STOP PROGRESS
   ========================================================= */

function stopProgress() {

    stopProgressTimer();

    setProgress(
        0,
        "Preparing vehicle image..."
    );


    if (progressSection) {

        progressSection.hidden =
            true;

    }

}


/* =========================================================
   24. RENDER RESULTS
   ========================================================= */

function renderResults(data) {

    stopProgressTimer();


    currentResultURL =
        data.result_url ||
        null;


    /* -----------------------------------------------------
       RESULT MESSAGE
    ----------------------------------------------------- */

    if (resultMessage) {

        resultMessage.textContent =
            data.message ||
            "AI analysis completed successfully.";

    }


    /* -----------------------------------------------------
       RESULT IMAGE
    ----------------------------------------------------- */

    if (
        resultImage &&
        currentResultURL
    ) {

        resultImage.src =
            currentResultURL;

        resultImage.hidden =
            false;

    } else if (resultImage) {

        resultImage.removeAttribute(
            "src"
        );

        resultImage.hidden =
            true;

    }


    if (mediaPlaceholder) {

        mediaPlaceholder.hidden =
            Boolean(
                currentResultURL
            );

    }


    /* -----------------------------------------------------
       TOTAL DETECTIONS
    ----------------------------------------------------- */

    const total =
        Number(
            data.total_detections || 0
        );


    if (totalDetections) {

        totalDetections.textContent =
            total;

    }


    /* -----------------------------------------------------
       AVERAGE CONFIDENCE
    ----------------------------------------------------- */

    const average =
        Number(
            data.average_confidence || 0
        );


    if (averageConfidence) {

        averageConfidence.textContent =
            `${formatConfidence(average)}%`;

    }


    /* -----------------------------------------------------
       DAMAGE COUNTS
    ----------------------------------------------------- */

    const damageCounts =
        data.damage_counts || {};


    const damageTypes =
        Object.keys(
            damageCounts
        );


    if (damageTypeCount) {

        damageTypeCount.textContent =
            damageTypes.length;

    }


    renderDamageCounts(
        damageCounts
    );


    /* -----------------------------------------------------
       DETECTIONS
    ----------------------------------------------------- */

    const detections =
        Array.isArray(
            data.detections
        )
            ? data.detections
            : [];


    renderDetections(
        detections
    );


    if (detectionCountLabel) {

        detectionCountLabel.textContent =
            `${detections.length} ${
                detections.length === 1
                    ? "detection"
                    : "detections"
            }`;

    }


    /* -----------------------------------------------------
       SHOW RESULTS
    ----------------------------------------------------- */

    if (progressSection) {

        progressSection.hidden =
            true;

    }


    if (resultsSection) {

        resultsSection.hidden =
            false;

    }


    /* -----------------------------------------------------
       SCROLL TO RESULTS
    ----------------------------------------------------- */

    setTimeout(
        () => {

            resultsSection?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        },
        150
    );

}


/* =========================================================
   25. RENDER DAMAGE COUNTS
   ========================================================= */

function renderDamageCounts(
    damageCounts
) {

    if (!damageList) {
        return;
    }


    damageList.innerHTML = "";


    const entries =
        Object.entries(
            damageCounts || {}
        );


    if (entries.length === 0) {

        damageList.innerHTML = `

            <div class="damage-item">

                <span class="damage-dot"></span>

                <span class="damage-name">
                    No visible damage detected
                </span>

                <span class="damage-count-number">
                    0
                </span>

            </div>

        `;

        return;

    }


    entries.sort(
        (a, b) =>
            Number(b[1]) -
            Number(a[1])
    );


    entries.forEach(
        ([name, count]) => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "damage-item";


            item.innerHTML = `

                <span class="damage-dot"></span>

                <span
                    class="damage-name"
                    title="${escapeHtml(name)}"
                >
                    ${escapeHtml(name)}
                </span>

                <span class="damage-count-number">
                    ${Number(count)}
                </span>

            `;


            damageList.appendChild(
                item
            );

        }
    );

}


/* =========================================================
   26. RENDER DETECTIONS
   ========================================================= */

function renderDetections(
    detections
) {

    if (!detectionList) {
        return;
    }


    detectionList.innerHTML = "";


    if (
        !detections ||
        detections.length === 0
    ) {

        detectionList.innerHTML = `

            <div class="detection-row">

                <div class="detection-class">
                    No detections found
                </div>

                <div class="confidence">

                    <div class="confidence-bar">

                        <div
                            class="confidence-fill"
                            style="width: 0%"
                        ></div>

                    </div>

                    <span class="confidence-value">
                        0%
                    </span>

                </div>

            </div>

        `;

        return;

    }


    detections.forEach(
        (detection) => {

            const name =
                detection.class ||
                "Unknown damage";


            const confidence =
                normalizeConfidence(
                    detection.confidence
                );


            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "detection-row";


            row.innerHTML = `

                <div
                    class="detection-class"
                    title="${escapeHtml(name)}"
                >
                    ${escapeHtml(name)}
                </div>


                <div class="confidence">

                    <div class="confidence-bar">

                        <div
                            class="confidence-fill"
                            style="width: ${confidence}%"
                        ></div>

                    </div>


                    <span class="confidence-value">
                        ${formatConfidence(confidence)}%
                    </span>

                </div>


                <div
                    class="confidence-value"
                    aria-hidden="true"
                >
                    ${confidence >= 80
                        ? "HIGH"
                        : confidence >= 50
                            ? "MID"
                            : "LOW"}
                </div>

            `;


            detectionList.appendChild(
                row
            );

        }
    );

}


/* =========================================================
   27. NORMALIZE CONFIDENCE
   ========================================================= */

function normalizeConfidence(
    value
) {

    let confidence =
        Number(value);


    if (!Number.isFinite(confidence)) {

        confidence = 0;

    }


    /*
     Backend returns confidence
     as a percentage.

     This also safely handles
     decimal values between 0 and 1.
    */

    if (
        confidence > 0 &&
        confidence <= 1
    ) {

        confidence *= 100;

    }


    confidence =
        Math.min(
            100,
            Math.max(
                0,
                confidence
            )
        );


    return Number(
        confidence.toFixed(2)
    );

}


/* =========================================================
   28. FORMAT CONFIDENCE
   ========================================================= */

function formatConfidence(
    value
) {

    const confidence =
        Number(value);


    if (
        !Number.isFinite(
            confidence
        )
    ) {

        return "0";

    }


    return confidence
        .toFixed(1)
        .replace(
            /\.0$/,
            ""
        );

}


/* =========================================================
   29. OPEN RESULT
   ========================================================= */

function openResult() {

    if (!currentResultURL) {

        showError(
            "No detection result is available."
        );

        return;

    }


    window.open(
        currentResultURL,
        "_blank",
        "noopener,noreferrer"
    );

}


/* =========================================================
   30. NEW INSPECTION
   ========================================================= */

function startNewInspection() {

    stopProgressTimer();


    currentResultURL =
        null;


    hideResults();

    hideError();

    stopProgress();


    resetSelectedFile();


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

}


/* =========================================================
   31. HIDE RESULTS
   ========================================================= */

function hideResults() {

    if (resultsSection) {

        resultsSection.hidden =
            true;

    }


    if (resultImage) {

        resultImage.removeAttribute(
            "src"
        );

    }


    if (mediaPlaceholder) {

        mediaPlaceholder.hidden =
            true;

    }


    if (damageList) {

        damageList.innerHTML =
            "";

    }


    if (detectionList) {

        detectionList.innerHTML =
            "";

    }

}


/* =========================================================
   32. SHOW ERROR
   ========================================================= */

function showError(
    message
) {

    if (!errorMessage) {
        return;
    }


    if (errorText) {

        errorText.textContent =
            message;

    }


    errorMessage.hidden =
        false;


    setTimeout(
        () => {

            errorMessage.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        },
        50
    );

}


/* =========================================================
   33. HIDE ERROR
   ========================================================= */

function hideError() {

    if (errorMessage) {

        errorMessage.hidden =
            true;

    }

}


/* =========================================================
   34. GET FILE EXTENSION
   ========================================================= */

function getFileExtension(
    filename
) {

    if (
        !filename ||
        !filename.includes(".")
    ) {

        return "";

    }


    return filename
        .split(".")
        .pop()
        .toLowerCase();

}


/* =========================================================
   35. FORMAT FILE SIZE
   ========================================================= */

function formatFileSize(
    bytes
) {

    if (
        !Number.isFinite(bytes) ||
        bytes <= 0
    ) {

        return "0 MB";

    }


    const megabytes =
        bytes /
        (1024 * 1024);


    if (megabytes < 1) {

        const kilobytes =
            bytes / 1024;


        return `${kilobytes.toFixed(1)} KB`;

    }


    return `${megabytes.toFixed(2)} MB`;

}


/* =========================================================
   36. ESCAPE HTML
   ========================================================= */

function escapeHtml(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}


/* =========================================================
   37. DELAY HELPER
   ========================================================= */

function delay(
    milliseconds
) {

    return new Promise(
        (resolve) => {

            setTimeout(
                resolve,
                milliseconds
            );

        }
    );

}


/* =========================================================
   38. KEYBOARD ACCESSIBILITY
   ========================================================= */

function initializeKeyboardSupport() {

    if (!uploadZone) {
        return;
    }


    uploadZone.addEventListener(
        "keydown",
        (event) => {

            if (isProcessing) {
                return;
            }


            if (
                event.key === "Enter" ||
                event.key === " "
            ) {

                event.preventDefault();

                openFilePicker();

            }

        }
    );

}


/* =========================================================
   39. GLOBAL DRAG PREVENTION
   ========================================================= */

document.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

    }
);


document.addEventListener(
    "drop",
    (event) => {

        /*
         Prevent accidentally opening an image
         in the browser when dropped outside
         the upload area.
        */

        if (
            uploadZone &&
            !uploadZone.contains(
                event.target
            )
        ) {

            event.preventDefault();

        }

    }
);


/* =========================================================
   40. IMAGE LOAD ERROR
   ========================================================= */

if (resultImage) {

    resultImage.addEventListener(
        "error",
        () => {

            resultImage.hidden =
                true;


            if (mediaPlaceholder) {

                mediaPlaceholder.textContent =
                    "Unable to load the detection result.";

                mediaPlaceholder.hidden =
                    false;

            }

        }
    );

}


/* =========================================================
   41. IMAGE LOAD SUCCESS
   ========================================================= */

if (resultImage) {

    resultImage.addEventListener(
        "load",
        () => {

            resultImage.hidden =
                false;


            if (mediaPlaceholder) {

                mediaPlaceholder.hidden =
                    true;

            }

        }
    );

}


/* =========================================================
   42. CLEANUP
   ========================================================= */

window.addEventListener(
    "beforeunload",
    () => {

        stopProgressTimer();


        if (selectedImageURL) {

            URL.revokeObjectURL(
                selectedImageURL
            );

        }

    }
);