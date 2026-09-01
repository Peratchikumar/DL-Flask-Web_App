/* ============================================================
   DL_VEHICLE_DAMAGE_DETECTION
   Frontend JavaScript
   ============================================================ */

"use strict";


/* ============================================================
   APPLICATION INITIALIZATION
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    initializeUpload();
    initializeNavigation();
    initializeImageErrorHandling();

});


/* ============================================================
   CONFIGURATION
   ============================================================ */

const CONFIG = {

    maxFileSize:
        50 * 1024 * 1024, // 50 MB

    allowedTypes: [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp"
    ],

    allowedExtensions: [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp"
    ]

};


/* ============================================================
   DOM HELPERS
   ============================================================ */

function getElement(id) {

    return document.getElementById(id);

}


/* ============================================================
   UPLOAD INITIALIZATION
   ============================================================ */

function initializeUpload() {

    const fileInput =
        getElement("fileInput");

    const uploadZone =
        getElement("uploadZone");

    const browseButton =
        getElement("browseButton");

    const removeButton =
        getElement("removeButton");

    const predictionForm =
        getElement("predictionForm");


    /*
     * If this page does not contain the upload interface,
     * simply stop without generating errors.
     */

    if (
        !fileInput ||
        !uploadZone
    ) {
        return;
    }


    /* --------------------------------------------------------
       File input
    -------------------------------------------------------- */

    fileInput.addEventListener(
        "change",
        handleFileInputChange
    );


    /* --------------------------------------------------------
       Browse button
    -------------------------------------------------------- */

    if (browseButton) {

        browseButton.addEventListener(
            "click",
            (event) => {

                event.preventDefault();
                event.stopPropagation();

                openFilePicker(fileInput);

            }
        );

    }


    /* --------------------------------------------------------
       Upload zone click
    -------------------------------------------------------- */

    uploadZone.addEventListener(
        "click",
        (event) => {

            /*
             * Do not trigger the file picker twice when
             * clicking the Browse button.
             */

            if (
                browseButton &&
                (
                    event.target === browseButton ||
                    browseButton.contains(event.target)
                )
            ) {
                return;
            }

            openFilePicker(fileInput);

        }
    );


    /* --------------------------------------------------------
       Keyboard accessibility
    -------------------------------------------------------- */

    uploadZone.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" ||
                event.key === " "
            ) {

                event.preventDefault();

                openFilePicker(fileInput);

            }

        }
    );


    /* --------------------------------------------------------
       Drag and drop
    -------------------------------------------------------- */

    initializeDragAndDrop(
        uploadZone,
        fileInput
    );


    /* --------------------------------------------------------
       Remove button
    -------------------------------------------------------- */

    if (removeButton) {

        removeButton.addEventListener(
            "click",
            (event) => {

                event.preventDefault();

                resetUpload();

            }
        );

    }


    /* --------------------------------------------------------
       Form submission
    -------------------------------------------------------- */

    if (predictionForm) {

        predictionForm.addEventListener(
            "submit",
            handleFormSubmit
        );

    }

}


/* ============================================================
   OPEN FILE PICKER
   ============================================================ */

function openFilePicker(fileInput) {

    if (!fileInput) {
        return;
    }

    fileInput.click();

}


/* ============================================================
   FILE INPUT CHANGE
   ============================================================ */

function handleFileInputChange(event) {

    const file =
        event.target.files &&
        event.target.files[0];

    if (!file) {
        return;
    }

    processSelectedFile(file);

}


/* ============================================================
   PROCESS SELECTED FILE
   ============================================================ */

function processSelectedFile(file) {

    clearError();


    const validation =
        validateFile(file);


    if (!validation.valid) {

        showError(
            validation.message
        );

        resetUpload(false);

        return;

    }


    displayImagePreview(file);

}


/* ============================================================
   FILE VALIDATION
   ============================================================ */

function validateFile(file) {

    if (!file) {

        return {
            valid: false,
            message:
                "Please select a vehicle image."
        };

    }


    /* --------------------------------------------------------
       File type
    -------------------------------------------------------- */

    const typeIsAllowed =
        CONFIG.allowedTypes.includes(
            file.type
        );


    const extension =
        getFileExtension(
            file.name
        );


    const extensionIsAllowed =
        CONFIG.allowedExtensions.includes(
            extension
        );


    if (
        !typeIsAllowed &&
        !extensionIsAllowed
    ) {

        return {
            valid: false,
            message:
                "Unsupported file type. Please upload JPG, JPEG, PNG, WEBP or BMP."
        };

    }


    /* --------------------------------------------------------
       File size
    -------------------------------------------------------- */

    if (
        file.size >
        CONFIG.maxFileSize
    ) {

        return {
            valid: false,
            message:
                "The selected image is too large. Maximum file size is 50 MB."
        };

    }


    return {
        valid: true,
        message: ""
    };

}


/* ============================================================
   GET FILE EXTENSION
   ============================================================ */

function getFileExtension(filename) {

    if (
        typeof filename !== "string"
    ) {
        return "";
    }


    const lastDot =
        filename.lastIndexOf(".");


    if (lastDot === -1) {
        return "";
    }


    return filename
        .slice(lastDot)
        .toLowerCase();

}


/* ============================================================
   IMAGE PREVIEW
   ============================================================ */

function displayImagePreview(file) {

    const previewContainer =
        getElement("previewContainer");

    const imagePreview =
        getElement("imagePreview");

    const detectButton =
        getElement("detectButton");


    if (
        !previewContainer ||
        !imagePreview
    ) {
        return;
    }


    /*
     * Revoke an older object URL before creating
     * a new one.
     */

    cleanupPreviewUrl();


    window.vehicleDamagePreviewUrl =
        URL.createObjectURL(file);


    imagePreview.src =
        window.vehicleDamagePreviewUrl;


    imagePreview.alt =
        `Selected vehicle image: ${file.name}`;


    previewContainer.classList.add(
        "visible"
    );


    if (detectButton) {

        detectButton.disabled =
            false;

    }


    updateSelectedFileInformation(
        file
    );


    clearError();

}


/* ============================================================
   SELECTED FILE INFORMATION
   ============================================================ */

function updateSelectedFileInformation(file) {

    const previewLabel =
        document.querySelector(
            ".preview-label"
        );


    if (!previewLabel || !file) {
        return;
    }


    previewLabel.textContent =
        `Selected Image: ${file.name}`;

}


/* ============================================================
   IMAGE PREVIEW LOAD ERROR
   ============================================================ */

function initializeImageErrorHandling() {

    const imagePreview =
        getElement("imagePreview");


    if (!imagePreview) {
        return;
    }


    imagePreview.addEventListener(
        "error",
        () => {

            showError(
                "The selected image could not be previewed. Please choose another image."
            );

            resetUpload();

        }
    );

}


/* ============================================================
   RESET UPLOAD
   ============================================================ */

function resetUpload(
    clearFileInput = true
) {

    const fileInput =
        getElement("fileInput");

    const previewContainer =
        getElement("previewContainer");

    const imagePreview =
        getElement("imagePreview");

    const detectButton =
        getElement("detectButton");

    const previewLabel =
        document.querySelector(
            ".preview-label"
        );


    cleanupPreviewUrl();


    if (
        clearFileInput &&
        fileInput
    ) {

        fileInput.value = "";

    }


    if (imagePreview) {

        imagePreview.removeAttribute(
            "src"
        );

        imagePreview.alt =
            "Selected vehicle image preview";

    }


    if (previewContainer) {

        previewContainer.classList.remove(
            "visible"
        );

    }


    if (previewLabel) {

        previewLabel.textContent =
            "Selected Image";

    }


    if (detectButton) {

        detectButton.disabled =
            true;

        detectButton.classList.remove(
            "loading"
        );

    }


    const buttonText =
        getElement("buttonText");


    if (buttonText) {

        buttonText.textContent =
            "Detect Vehicle Damage";

    }


    clearError();

}


/* ============================================================
   CLEANUP OBJECT URL
   ============================================================ */

function cleanupPreviewUrl() {

    if (
        window.vehicleDamagePreviewUrl
    ) {

        URL.revokeObjectURL(
            window.vehicleDamagePreviewUrl
        );

        window.vehicleDamagePreviewUrl =
            null;

    }

}


/* ============================================================
   ERROR MESSAGE
   ============================================================ */

function showError(message) {

    const errorMessage =
        getElement("errorMessage");


    if (!errorMessage) {
        return;
    }


    errorMessage.textContent =
        message;


    errorMessage.classList.add(
        "visible"
    );

}


function clearError() {

    const errorMessage =
        getElement("errorMessage");


    if (!errorMessage) {
        return;
    }


    errorMessage.textContent =
        "";


    errorMessage.classList.remove(
        "visible"
    );

}


/* ============================================================
   DRAG AND DROP
   ============================================================ */

function initializeDragAndDrop(
    uploadZone,
    fileInput
) {

    const dragEvents = [
        "dragenter",
        "dragover"
    ];


    dragEvents.forEach(
        (eventName) => {

            uploadZone.addEventListener(
                eventName,
                handleDragOver
            );

        }
    );


    uploadZone.addEventListener(
        "dragleave",
        handleDragLeave
    );


    uploadZone.addEventListener(
        "drop",
        (event) => {

            handleDrop(
                event,
                fileInput,
                uploadZone
            );

        }
    );

}


/* ============================================================
   DRAG OVER
   ============================================================ */

function handleDragOver(event) {

    event.preventDefault();

    event.stopPropagation();


    const uploadZone =
        event.currentTarget;


    if (
        uploadZone
    ) {

        uploadZone.classList.add(
            "dragover"
        );

    }


    /*
     * Tell the browser that dropping is allowed.
     */

    if (
        event.dataTransfer
    ) {

        event.dataTransfer.dropEffect =
            "copy";

    }

}


/* ============================================================
   DRAG LEAVE
   ============================================================ */

function handleDragLeave(event) {

    event.preventDefault();

    event.stopPropagation();


    const uploadZone =
        event.currentTarget;


    /*
     * Only remove the state when the pointer
     * actually leaves the upload zone.
     */

    if (
        event.relatedTarget &&
        uploadZone.contains(
            event.relatedTarget
        )
    ) {
        return;
    }


    uploadZone.classList.remove(
        "dragover"
    );

}


/* ============================================================
   DROP
   ============================================================ */

function handleDrop(
    event,
    fileInput,
    uploadZone
) {

    event.preventDefault();

    event.stopPropagation();


    uploadZone.classList.remove(
        "dragover"
    );


    const files =
        event.dataTransfer &&
        event.dataTransfer.files;


    if (
        !files ||
        !files.length
    ) {

        showError(
            "No file was dropped. Please choose an image."
        );

        return;

    }


    const file =
        files[0];


    processDroppedFile(
        file,
        fileInput
    );

}


/* ============================================================
   PROCESS DROPPED FILE
   ============================================================ */

function processDroppedFile(
    file,
    fileInput
) {

    const validation =
        validateFile(file);


    if (!validation.valid) {

        showError(
            validation.message
        );

        return;

    }


    /*
     * Assign the dropped file to the actual
     * form input when the browser supports DataTransfer.
     */

    try {

        if (
            typeof DataTransfer !==
            "undefined"
        ) {

            const dataTransfer =
                new DataTransfer();


            dataTransfer.items.add(
                file
            );


            fileInput.files =
                dataTransfer.files;

        }

    } catch (error) {

        /*
         * The preview can still work even if
         * assigning the dropped file is unsupported.
         */

    }


    displayImagePreview(
        file
    );

}


/* ============================================================
   FORM SUBMISSION
   ============================================================ */

function handleFormSubmit(event) {

    const form =
        event.currentTarget;


    const fileInput =
        getElement("fileInput");


    if (
        !fileInput
    ) {
        return;
    }


    const file =
        fileInput.files &&
        fileInput.files[0];


    const validation =
        validateFile(file);


    if (!validation.valid) {

        event.preventDefault();


        showError(
            validation.message
        );


        return;

    }


    /*
     * Prevent accidental double submissions.
     */

    setLoadingState(
        true
    );


    /*
     * Allow the normal HTML form submission
     * to continue to Flask.
     */

}


/* ============================================================
   LOADING STATE
   ============================================================ */

function setLoadingState(
    isLoading
) {

    const detectButton =
        getElement("detectButton");

    const buttonText =
        getElement("buttonText");


    if (!detectButton) {
        return;
    }


    if (isLoading) {

        detectButton.disabled =
            true;


        detectButton.classList.add(
            "loading"
        );


        if (buttonText) {

            buttonText.textContent =
                "Analyzing Vehicle...";

        }

    } else {

        detectButton.classList.remove(
            "loading"
        );


        if (buttonText) {

            buttonText.textContent =
                "Detect Vehicle Damage";

        }

    }

}


/* ============================================================
   NAVIGATION
   ============================================================ */

function initializeNavigation() {

    const navigationLinks =
        document.querySelectorAll(
            'a[href^="#"]'
        );


    if (!navigationLinks.length) {
        return;
    }


    navigationLinks.forEach(
        (link) => {

            link.addEventListener(
                "click",
                handleNavigationClick
            );

        }
    );

}


/* ============================================================
   SMOOTH NAVIGATION
   ============================================================ */

function handleNavigationClick(event) {

    const link =
        event.currentTarget;


    const targetId =
        link.getAttribute(
            "href"
        );


    if (
        !targetId ||
        targetId === "#"
    ) {
        return;
    }


    const target =
        document.querySelector(
            targetId
        );


    if (!target) {
        return;
    }


    event.preventDefault();


    target.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });


    /*
     * Update the URL hash without causing
     * another jump.
     */

    if (
        window.history &&
        window.history.pushState
    ) {

        window.history.pushState(
            null,
            "",
            targetId
        );

    }

}


/* ============================================================
   BEFORE PAGE UNLOAD
   ============================================================ */

window.addEventListener(
    "beforeunload",
    () => {

        cleanupPreviewUrl();

    }
);


/* ============================================================
   EXPOSE ONLY NECESSARY FUNCTIONS
   ============================================================ */

window.VehicleDamageDetection = {

    resetUpload,

    showError,

    clearError,

    setLoadingState

};