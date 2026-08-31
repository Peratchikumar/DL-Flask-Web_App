"""
File Utility Functions

Vehicle Damage Detection
YOLO26 + Flask
"""

from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from config.settings import (
    UPLOAD_FOLDER,
    OUTPUT_FOLDER,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
)


# ============================================================
# FILE EXTENSION
# ============================================================

def get_file_extension(filename: str) -> str:
    """
    Get the lowercase extension of a file.

    Example:
        vehicle.jpg -> jpg
    """

    if not filename or "." not in filename:
        return ""

    return filename.rsplit(
        ".",
        1
    )[1].lower()


# ============================================================
# IMAGE VALIDATION
# ============================================================

def is_allowed_image(filename: str) -> bool:
    """
    Check whether the file is an allowed image type.
    """

    extension = get_file_extension(
        filename
    )

    return extension in ALLOWED_IMAGE_EXTENSIONS


# ============================================================
# VIDEO VALIDATION
# ============================================================

def is_allowed_video(filename: str) -> bool:
    """
    Check whether the file is an allowed video type.
    """

    extension = get_file_extension(
        filename
    )

    return extension in ALLOWED_VIDEO_EXTENSIONS


# ============================================================
# SECURE FILENAME
# ============================================================

def create_secure_filename(
    filename: str
) -> str:
    """
    Convert an uploaded filename into a safe filename.
    """

    safe_filename = secure_filename(
        filename
    )

    if not safe_filename:
        raise ValueError(
            "Invalid filename."
        )

    return safe_filename


# ============================================================
# UNIQUE FILENAME
# ============================================================

def create_unique_filename(
    filename: str
) -> str:
    """
    Create a unique and secure filename.

    Example:
        car.jpg

    becomes:
        a8f31c29_car.jpg
    """

    safe_filename = create_secure_filename(
        filename
    )

    unique_id = uuid4().hex[:8]

    return f"{unique_id}_{safe_filename}"


# ============================================================
# SAVE UPLOADED FILE
# ============================================================

def save_uploaded_file(
    uploaded_file: FileStorage
) -> Path:
    """
    Save an uploaded file to the uploads directory.

    Returns:
        Path of the saved file.
    """

    if uploaded_file is None:
        raise ValueError(
            "No uploaded file was provided."
        )

    if not uploaded_file.filename:
        raise ValueError(
            "Uploaded file has no filename."
        )

    filename = create_unique_filename(
        uploaded_file.filename
    )

    upload_directory = Path(
        UPLOAD_FOLDER
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = (
        upload_directory / filename
    )

    uploaded_file.save(
        str(file_path)
    )

    return file_path


# ============================================================
# DELETE FILE
# ============================================================

def delete_file(
    file_path: str | Path
) -> bool:
    """
    Safely delete a file.

    Returns:
        True if deleted.
        False if the file does not exist.
    """

    path = Path(file_path)

    try:

        if path.exists() and path.is_file():

            path.unlink()

            return True

        return False

    except OSError as error:

        print(
            f"Warning: Could not delete "
            f"{path}: {error}"
        )

        return False


# ============================================================
# CHECK FILE EXISTS
# ============================================================

def file_exists(
    file_path: str | Path
) -> bool:
    """
    Check whether a file exists.
    """

    path = Path(file_path)

    return (
        path.exists()
        and path.is_file()
    )


# ============================================================
# CREATE OUTPUT PATH
# ============================================================

def create_output_path(
    filename: str,
    suffix: str = "_result"
) -> Path:
    """
    Create a path for an output file.

    Example:
        car.jpg

    becomes:
        outputs/car_result.jpg
    """

    safe_filename = create_secure_filename(
        filename
    )

    original_path = Path(
        safe_filename
    )

    output_filename = (
        f"{original_path.stem}"
        f"{suffix}"
        f"{original_path.suffix}"
    )

    output_directory = Path(
        OUTPUT_FOLDER
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return (
        output_directory /
        output_filename
    )


# ============================================================
# GET FILE SIZE
# ============================================================

def get_file_size(
    file_path: str | Path
) -> int:
    """
    Get file size in bytes.
    """

    path = Path(file_path)

    if not path.exists():
        return 0

    return path.stat().st_size


# ============================================================
# FORMAT FILE SIZE
# ============================================================

def format_file_size(
    size_bytes: int
) -> str:
    """
    Convert bytes into a readable file size.

    Examples:
        1024 -> 1.00 KB
        1048576 -> 1.00 MB
    """

    if size_bytes < 0:
        return "0 B"

    size = float(size_bytes)

    units = [
        "B",
        "KB",
        "MB",
        "GB",
    ]

    for unit in units:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"