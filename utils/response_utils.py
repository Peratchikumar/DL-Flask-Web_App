"""
Response utilities for the Vehicle Damage Detection API.

This module provides reusable functions for creating
consistent JSON responses across the Flask application.
"""

from typing import Any

from flask import jsonify


# ============================================================
# SUCCESS RESPONSE
# ============================================================

def success_response(
    data: dict[str, Any] | None = None,
    message: str = "Request completed successfully.",
    status_code: int = 200,
):
    """
    Create a standardized successful JSON response.

    Args:
        data:
            Response data.
        message:
            Success message.
        status_code:
            HTTP status code.

    Returns:
        Flask JSON response.
    """

    response_data: dict[str, Any] = {
        "success": True,
        "message": message,
    }

    if data:
        response_data.update(data)

    return jsonify(response_data), status_code


# ============================================================
# ERROR RESPONSE
# ============================================================

def error_response(
    error: str,
    message: str | None = None,
    status_code: int = 400,
    details: Any | None = None,
):
    """
    Create a standardized error JSON response.

    Args:
        error:
            Short description of the error.
        message:
            Detailed message for the client.
        status_code:
            HTTP error status code.
        details:
            Optional additional error information.

    Returns:
        Flask JSON response.
    """

    response_data: dict[str, Any] = {
        "success": False,
        "error": error,
    }

    if message:
        response_data["message"] = message

    if details is not None:
        response_data["details"] = details

    return jsonify(response_data), status_code


# ============================================================
# VALIDATION ERROR
# ============================================================

def validation_error(
    message: str,
    details: Any | None = None,
):
    """
    Create a validation error response.

    HTTP status:
        400 Bad Request
    """

    return error_response(
        error="Validation Error",
        message=message,
        status_code=400,
        details=details,
    )


# ============================================================
# NOT FOUND RESPONSE
# ============================================================

def not_found_response(
    message: str = "The requested resource was not found.",
):
    """
    Create a 404 Not Found response.
    """

    return error_response(
        error="Not Found",
        message=message,
        status_code=404,
    )


# ============================================================
# INTERNAL SERVER ERROR
# ============================================================

def server_error_response(
    message: str = "An unexpected server error occurred.",
    details: Any | None = None,
):
    """
    Create a 500 Internal Server Error response.
    """

    return error_response(
        error="Internal Server Error",
        message=message,
        status_code=500,
        details=details,
    )


# ============================================================
# PREDICTION SUCCESS RESPONSE
# ============================================================

def prediction_response(
    filename: str,
    detections: list[dict[str, Any]],
):
    """
    Create a standardized vehicle damage prediction response.

    Args:
        filename:
            Name of the processed image.

        detections:
            List of YOLO26 detection results.

    Returns:
        Flask JSON response.
    """

    return success_response(
        data={
            "filename": filename,
            "detection_count": len(detections),
            "detections": detections,
        },
        message="Vehicle damage detection completed successfully.",
        status_code=200,
    )


# ============================================================
# NO DAMAGE DETECTED RESPONSE
# ============================================================

def no_detection_response(
    filename: str,
):
    """
    Create a response when no vehicle damage is detected.
    """

    return success_response(
        data={
            "filename": filename,
            "detection_count": 0,
            "detections": [],
        },
        message="No vehicle damage was detected.",
        status_code=200,
    )