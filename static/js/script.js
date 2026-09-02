/* ============================================================
   VEHICLE DAMAGE AI
   Premium Automotive AI Inspection Interface
   Frontend Interaction Controller
   ============================================================ */

"use strict";


/* ============================================================
   01. DOM REFERENCES
   ============================================================ */

const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("vehicle_image");
const uploadArea = document.getElementById("upload-area");
const selectedFile = document.getElementById("selected-file");
const fileLabel = document.getElementById("file-label");

const submitButton = document.getElementById("submit-button");
const submitButtonText = document.getElementById("submit-button-text");
const buttonSpinner = document.getElementById("button-spinner");

const loadingOverlay = document.getElementById("loading-overlay");
const newAnalysisButton = document.getElementById("new-analysis");

const resultsSection = document.getElementById("results");
const resultImage = document.getElementById("result-image");


/* ============================================================
   02. APPLICATION CONFIGURATION
   ============================================================ */

const CONFIG = {
    maxFileSize: 10 * 1024 * 1024,

    allowedExtensions: [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ],

    allowedMimeTypes: [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]
};


/* ============================================================
   03. INITIALIZATION
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    initializeUpload();
    initializeForm();
    initializeNewAnalysis();
    initializeNavigation();
    initializeResultImage();
    initializeAccessibility();

});


/* ============================================================
   04. UPLOAD INITIALIZATION
   ============================================================ */

function initializeUpload() {

    if (!fileInput || !uploadArea) {
        return;
    }


    /*
     * Clicking the upload zone opens
     * the native file picker.
     */

    uploadArea.addEventListener("click", (event) => {

        if (event.target === fileInput) {
            return;
        }

        fileInput.click();

    });


    /*
     * Keyboard support.
     * Enter and Space activate the file picker.
     */

    uploadArea.addEventListener("keydown", (event) => {

        if (
            event.key === "Enter" ||
            event.key === " "
        ) {

            event.preventDefault();

            fileInput.click();

        }

    });


    /*
     * Standard file selection.
     */

    fileInput.addEventListener("change", () => {

        const file = fileInput.files?.[0];

        if (!file) {

            resetFileSelection();

            return;
        }

        processSelectedFile(file);

    });


    /*
     * Drag events.
     */

    uploadArea.addEventListener(
        "dragenter",
        handleDragEnter
    );

    uploadArea.addEventListener(
        "dragover",
        handleDragOver
    );

    uploadArea.addEventListener(
        "dragleave",
        handleDragLeave
    );

    uploadArea.addEventListener(
        "drop",
        handleDrop
    );

}


/* ============================================================
   05. FILE VALIDATION
   ============================================================ */

function validateFile(file) {

    if (!file) {

        return {
            valid: false,
            message: "Please select an image."
        };

    }


    /*
     * Validate file size.
     */

    if (file.size > CONFIG.maxFileSize) {

        return {
            valid: false,
            message: "Image size must be 10 MB or smaller."
        };

    }


    /*
     * Validate extension.
     */

    const fileName = file.name.toLowerCase();

    const hasValidExtension =
        CONFIG.allowedExtensions.some(
            extension => fileName.endsWith(extension)
        );


    /*
     * Validate MIME type where available.
     */

    const hasValidMimeType =
        !file.type ||
        CONFIG.allowedMimeTypes.includes(file.type);


    if (!hasValidExtension || !hasValidMimeType) {

        return {
            valid: false,
            message:
                "Unsupported image format. Please use JPG, JPEG, PNG or WEBP."
        };

    }


    return {
        valid: true,
        message: ""
    };

}


/* ============================================================
   06. PROCESS SELECTED FILE
   ============================================================ */

function processSelectedFile(file) {

    const validation = validateFile(file);


    if (!validation.valid) {

        showUploadError(validation.message);

        resetFileInput();

        return;

    }


    clearUploadError();

    updateSelectedFile(file);

    enableSubmitButton();

}


/* ============================================================
   07. UPDATE SELECTED FILE UI
   ============================================================ */

function updateSelectedFile(file) {

    if (!fileLabel || !selectedFile) {
        return;
    }


    fileLabel.textContent = formatFileName(
        file.name,
        48
    );


    selectedFile.classList.add("has-file");


    /*
     * Show file information through a title
     * without making the UI visually crowded.
     */

    selectedFile.setAttribute(
        "title",
        `${file.name} — ${formatFileSize(file.size)}`
    );

}


/* ============================================================
   08. FILE NAME FORMATTING
   ============================================================ */

function formatFileName(fileName, maxLength) {

    if (fileName.length <= maxLength) {
        return fileName;
    }


    const extensionIndex =
        fileName.lastIndexOf(".");


    if (extensionIndex === -1) {

        return (
            fileName.substring(
                0,
                maxLength - 3
            ) +
            "..."
        );

    }


    const extension =
        fileName.substring(extensionIndex);

    const availableLength =
        maxLength -
        extension.length -
        3;


    return (
        fileName.substring(
            0,
            Math.max(availableLength, 1)
        ) +
        "..." +
        extension
    );

}


/* ============================================================
   09. FILE SIZE FORMATTING
   ============================================================ */

function formatFileSize(bytes) {

    if (!Number.isFinite(bytes) || bytes <= 0) {
        return "0 KB";
    }


    const units = [
        "B",
        "KB",
        "MB",
        "GB"
    ];


    const index = Math.min(
        Math.floor(
            Math.log(bytes) /
            Math.log(1024)
        ),
        units.length - 1
    );


    const value =
        bytes /
        Math.pow(1024, index);


    return `${value.toFixed(index === 0 ? 0 : 1)} ${units[index]}`;

}


/* ============================================================
   10. RESET FILE SELECTION
   ============================================================ */

function resetFileSelection() {

    if (fileLabel) {
        fileLabel.textContent = "No image selected";
    }


    if (selectedFile) {

        selectedFile.classList.remove(
            "has-file"
        );

        selectedFile.removeAttribute(
            "title"
        );

    }


    disableSubmitButton();

}


/* ============================================================
   11. RESET FILE INPUT
   ============================================================ */

function resetFileInput() {

    if (!fileInput) {
        return;
    }

    fileInput.value = "";

}


/* ============================================================
   12. SUBMIT BUTTON STATE
   ============================================================ */

function enableSubmitButton() {

    if (!submitButton) {
        return;
    }

    submitButton.disabled = false;

}


function disableSubmitButton() {

    if (!submitButton) {
        return;
    }

    submitButton.disabled = true;

}


/* ============================================================
   13. DRAG & DROP
   ============================================================ */

function handleDragEnter(event) {

    event.preventDefault();
    event.stopPropagation();

    uploadArea?.classList.add("drag-over");

}


function handleDragOver(event) {

    event.preventDefault();
    event.stopPropagation();

    if (event.dataTransfer) {
        event.dataTransfer.dropEffect = "copy";
    }

    uploadArea?.classList.add("drag-over");

}


function handleDragLeave(event) {

    event.preventDefault();
    event.stopPropagation();


    /*
     * Only remove the state when leaving
     * the upload zone itself.
     */

    if (
        event.relatedTarget &&
        uploadArea?.contains(event.relatedTarget)
    ) {

        return;

    }


    uploadArea?.classList.remove("drag-over");

}


function handleDrop(event) {

    event.preventDefault();
    event.stopPropagation();

    uploadArea?.classList.remove("drag-over");


    const files =
        event.dataTransfer?.files;


    if (!files || files.length === 0) {
        return;
    }


    const file = files[0];


    /*
     * Put the dropped file into the native
     * input when browser security permits.
     */

    try {

        const dataTransfer =
            new DataTransfer();

        dataTransfer.items.add(file);

        fileInput.files =
            dataTransfer.files;

    } catch (error) {

        /*
         * Some environments do not permit
         * programmatic assignment.
         * The selected file can still be processed.
         */

        console.debug(
            "Unable to synchronize dropped file with input.",
            error
        );

    }


    processSelectedFile(file);

}


/* ============================================================
   14. FORM SUBMISSION
   ============================================================ */

function initializeForm() {

    if (!uploadForm) {
        return;
    }


    uploadForm.addEventListener(
        "submit",
        handleFormSubmit
    );

}


function handleFormSubmit(event) {

    /*
     * Allow the browser to perform the normal
     * Flask multipart POST.
     *
     * We only enhance the experience here.
     */

    if (!fileInput?.files?.length) {

        event.preventDefault();

        showUploadError(
            "Please select a vehicle image before starting the inspection."
        );

        return;

    }


    const file =
        fileInput.files[0];


    const validation =
        validateFile(file);


    if (!validation.valid) {

        event.preventDefault();

        showUploadError(
            validation.message
        );

        return;

    }


    clearUploadError();

    setLoadingState(true);

}


/* ============================================================
   15. LOADING STATE
   ============================================================ */

function setLoadingState(isLoading) {

    if (submitButton) {

        submitButton.classList.toggle(
            "is-loading",
            isLoading
        );

        submitButton.disabled = isLoading;

    }


    if (submitButtonText) {

        submitButtonText.textContent =
            isLoading
                ? "Analyzing..."
                : "Analyze Vehicle";

    }


    if (loadingOverlay) {

        loadingOverlay.classList.toggle(
            "active",
            isLoading
        );

        loadingOverlay.setAttribute(
            "aria-hidden",
            String(!isLoading)
        );

    }


    document.body.classList.toggle(
        "inspection-loading",
        isLoading
    );

}


/* ============================================================
   16. UPLOAD ERROR
   ============================================================ */

function showUploadError(message) {

    clearUploadError();


    if (!uploadArea) {
        return;
    }


    const error = document.createElement("div");

    error.className =
        "client-upload-error";


    error.setAttribute(
        "role",
        "alert"
    );


    error.textContent =
        message;


    error.style.cssText = `
        position: absolute;
        left: 20px;
        right: 20px;
        bottom: 16px;
        z-index: 10;
        padding: 9px 12px;
        border: 1px solid rgba(255, 102, 120, 0.25);
        border-radius: 8px;
        background: rgba(255, 102, 120, 0.08);
        color: #ffb4be;
        font-size: 9px;
        font-weight: 600;
        text-align: center;
    `;


    uploadArea.appendChild(error);


    uploadArea.classList.add(
        "upload-error"
    );

}


function clearUploadError() {

    if (!uploadArea) {
        return;
    }


    const existingError =
        uploadArea.querySelector(
            ".client-upload-error"
        );


    if (existingError) {
        existingError.remove();
    }


    uploadArea.classList.remove(
        "upload-error"
    );

}


/* ============================================================
   17. NEW ANALYSIS
   ============================================================ */

function initializeNewAnalysis() {

    if (!newAnalysisButton) {
        return;
    }


    newAnalysisButton.addEventListener(
        "click",
        startNewAnalysis
    );

}


function startNewAnalysis() {

    /*
     * Clear current form state.
     */

    resetFileInput();
    resetFileSelection();
    clearUploadError();


    /*
     * Scroll back to inspection workspace.
     */

    const inspectionSection =
        document.getElementById(
            "inspection"
        );


    if (inspectionSection) {

        inspectionSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }


    /*
     * Focus the upload area after
     * the scroll begins.
     */

    window.setTimeout(() => {

        uploadArea?.focus({
            preventScroll: true
        });

    }, 450);

}


/* ============================================================
   18. RESULT IMAGE
   ============================================================ */

function initializeResultImage() {

    if (!resultImage) {
        return;
    }


    resultImage.addEventListener(
        "error",
        handleResultImageError
    );

}


function handleResultImageError() {

    const container =
        resultImage.closest(
            ".image-frame"
        );


    if (!container) {
        return;
    }


    resultImage.style.display =
        "none";


    const message =
        document.createElement("div");


    message.className =
        "result-image-error";


    message.textContent =
        "Unable to display the annotated image.";


    message.style.cssText = `
        padding: 30px;
        color: #a8b2c1;
        font-size: 11px;
        text-align: center;
    `;


    container.appendChild(message);

}


/* ============================================================
   19. NAVIGATION
   ============================================================ */

function initializeNavigation() {

    const navigationLinks =
        document.querySelectorAll(
            ".nav-link"
        );


    if (!navigationLinks.length) {
        return;
    }


    navigationLinks.forEach(link => {

        link.addEventListener(
            "click",
            () => {

                navigationLinks.forEach(
                    item =>
                        item.classList.remove(
                            "active"
                        )
                );


                link.classList.add(
                    "active"
                );

            }
        );

    });


    /*
     * Keep navigation state synchronized
     * with visible sections.
     */

    initializeNavigationObserver();

}


function initializeNavigationObserver() {

    const sections =
        document.querySelectorAll(
            "#inspection, #workflow, #technology"
        );


    if (
        !sections.length ||
        !("IntersectionObserver" in window)
    ) {

        return;

    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) {
                        return;
                    }


                    const sectionId =
                        entry.target.id;


                    const activeLink =
                        document.querySelector(
                            `.nav-link[href="#${sectionId}"]`
                        );


                    if (!activeLink) {
                        return;
                    }


                    document
                        .querySelectorAll(
                            ".nav-link"
                        )
                        .forEach(link => {

                            link.classList.remove(
                                "active"
                            );

                        });


                    activeLink.classList.add(
                        "active"
                    );

                });

            },
            {
                root: null,
                rootMargin: "-25% 0px -60% 0px",
                threshold: 0
            }
        );


    sections.forEach(
        section =>
            observer.observe(section)
    );

}


/* ============================================================
   20. ACCESSIBILITY
   ============================================================ */

function initializeAccessibility() {

    /*
     * Ensure the upload area remains keyboard accessible.
     */

    if (uploadArea) {

        uploadArea.setAttribute(
            "aria-keyshortcuts",
            "Enter Space"
        );

    }


    /*
     * Give the loading screen a proper
     * live status while active.
     */

    if (loadingOverlay) {

        loadingOverlay.setAttribute(
            "aria-live",
            "polite"
        );

    }

}


/* ============================================================
   21. PAGE SHOW / BROWSER BACK-FORWARD CACHE
   ============================================================ */

window.addEventListener(
    "pageshow",
    () => {

        setLoadingState(false);

        if (
            uploadArea &&
            uploadArea.classList.contains(
                "drag-over"
            )
        ) {

            uploadArea.classList.remove(
                "drag-over"
            );

        }

    }
);


/* ============================================================
   22. ESCAPE KEY
   ============================================================ */

document.addEventListener(
    "keydown",
    event => {

        if (event.key !== "Escape") {
            return;
        }


        /*
         * Remove drag state if Escape is pressed.
         */

        uploadArea?.classList.remove(
            "drag-over"
        );

    }
);


/* ============================================================
   23. GLOBAL DRAG PROTECTION
   ============================================================ */

window.addEventListener(
    "dragover",
    event => {

        event.preventDefault();

    }
);


window.addEventListener(
    "drop",
    event => {

        /*
         * Only allow drops inside the
         * designated upload zone.
         */

        if (
            uploadArea &&
            uploadArea.contains(event.target)
        ) {

            return;

        }


        event.preventDefault();

    }
);


/* ============================================================
   24. PREVENT ACCIDENTAL DOUBLE SUBMISSION
   ============================================================ */

if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        event => {

            if (
                uploadForm.dataset.submitted === "true"
            ) {

                event.preventDefault();

                return;

            }


            /*
             * Mark as submitted only after
             * validation has passed.
             */

            if (
                fileInput?.files?.length &&
                validateFile(
                    fileInput.files[0]
                ).valid
            ) {

                uploadForm.dataset.submitted =
                    "true";

            }

        },
        true
    );

}


/* ============================================================
   END OF VEHICLE DAMAGE AI SCRIPT
   ============================================================ */