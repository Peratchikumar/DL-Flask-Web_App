"""
YOLO26 Vehicle Damage Detection Service.

This module:
    - Loads one trained YOLO26 .pt model
    - Performs image inference
    - Extracts detected classes
    - Extracts confidence scores
    - Extracts bounding boxes
    - Returns JSON-friendly prediction results
"""

from pathlib import Path
from typing import Any

from ultralytics import YOLO

from config.settings import (
    MODEL_PATH,
    IMAGE_SIZE,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
)


class VehicleDamageDetector:
    """
    Vehicle damage detector using a trained YOLO26 .pt model.
    """

    def __init__(
        self,
        model_path: Path = MODEL_PATH,
        image_size: int = IMAGE_SIZE,
        confidence_threshold: float = CONFIDENCE_THRESHOLD,
        iou_threshold: float = IOU_THRESHOLD,
    ) -> None:

        self.model_path = Path(model_path)
        self.image_size = image_size
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold

        self.model = self._load_model()

    # ========================================================
    # MODEL LOADING
    # ========================================================

    def _load_model(self) -> YOLO:
        """
        Load the trained YOLO26 .pt model.

        Returns:
            Loaded YOLO model.

        Raises:
            FileNotFoundError:
                If the model file does not exist.

            RuntimeError:
                If the model cannot be loaded.
        """

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"YOLO26 model not found: {self.model_path}"
            )

        # Make sure we are using the PyTorch model
        if self.model_path.suffix.lower() != ".pt":
            raise ValueError(
                "This detector is configured for a "
                "PyTorch .pt model only."
            )

        try:

            model = YOLO(
                str(self.model_path)
            )

            print("=" * 60)
            print("YOLO26 VEHICLE DAMAGE DETECTOR")
            print("=" * 60)
            print(
                f"Model Path: {self.model_path}"
            )
            print(
                f"Image Size: {self.image_size}"
            )
            print(
                "Confidence Threshold: "
                f"{self.confidence_threshold}"
            )
            print(
                f"IoU Threshold: {self.iou_threshold}"
            )
            print("=" * 60)
            print("MODEL LOADED SUCCESSFULLY")
            print("=" * 60)

            return model

        except Exception as exc:

            raise RuntimeError(
                f"Failed to load YOLO26 model: {exc}"
            ) from exc

    # ========================================================
    # IMAGE PREDICTION
    # ========================================================

    def predict(
        self,
        image_path: str | Path,
    ) -> dict[str, Any]:
        """
        Run vehicle damage detection on an image.

        Args:
            image_path:
                Path to the input vehicle image.

        Returns:
            Dictionary containing detection results.
        """

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Input image not found: {image_path}"
            )

        if not image_path.is_file():
            raise ValueError(
                f"Input path is not a file: {image_path}"
            )

        try:

            results = self.model.predict(
                source=str(image_path),
                imgsz=self.image_size,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False,
            )

            if not results:

                return self._empty_result(
                    image_path
                )

            return self._process_results(
                results[0],
                image_path,
            )

        except Exception as exc:

            raise RuntimeError(
                f"Vehicle damage prediction failed: {exc}"
            ) from exc

    # ========================================================
    # PROCESS YOLO RESULTS
    # ========================================================

    def _process_results(
        self,
        result: Any,
        image_path: Path,
    ) -> dict[str, Any]:
        """
        Convert raw YOLO results into a
        JSON-friendly dictionary.
        """

        detections: list[dict[str, Any]] = []

        boxes = result.boxes

        if boxes is not None:

            for index in range(len(boxes)):

                class_id = int(
                    boxes.cls[index].item()
                )

                confidence = float(
                    boxes.conf[index].item()
                )

                coordinates = (
                    boxes.xyxy[index]
                    .cpu()
                    .numpy()
                    .tolist()
                )

                x1, y1, x2, y2 = coordinates

                class_name = (
                    self._get_class_name(
                        class_id
                    )
                )

                detection = {
                    "class_id": class_id,

                    "class_name": class_name,

                    "confidence": round(
                        confidence,
                        4,
                    ),

                    "confidence_percent": round(
                        confidence * 100,
                        2,
                    ),

                    "bounding_box": {
                        "x1": round(
                            float(x1),
                            2,
                        ),

                        "y1": round(
                            float(y1),
                            2,
                        ),

                        "x2": round(
                            float(x2),
                            2,
                        ),

                        "y2": round(
                            float(y2),
                            2,
                        ),
                    },
                }

                detections.append(
                    detection
                )

        return {
            "success": True,

            "filename": image_path.name,

            "detection_count": len(
                detections
            ),

            "detections": detections,
        }

    # ========================================================
    # GET CLASS NAME
    # ========================================================

    def _get_class_name(
        self,
        class_id: int,
    ) -> str:
        """
        Get the class name associated
        with a YOLO class ID.
        """

        names = self.model.names

        if isinstance(names, dict):

            return str(
                names.get(
                    class_id,
                    f"class_{class_id}",
                )
            )

        if isinstance(names, list):

            if 0 <= class_id < len(names):

                return str(
                    names[class_id]
                )

        return f"class_{class_id}"

    # ========================================================
    # EMPTY RESULT
    # ========================================================

    @staticmethod
    def _empty_result(
        image_path: Path,
    ) -> dict[str, Any]:
        """
        Return a valid result when
        no predictions are available.
        """

        return {
            "success": True,

            "filename": image_path.name,

            "detection_count": 0,

            "detections": [],
        }

    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    def get_model_info(
        self,
    ) -> dict[str, Any]:
        """
        Return information about the
        loaded YOLO26 model.
        """

        return {
            "model_name": "YOLO26",

            "model_type": "PyTorch (.pt)",

            "model_path": str(
                self.model_path
            ),

            "image_size": self.image_size,

            "confidence_threshold": (
                self.confidence_threshold
            ),

            "iou_threshold": (
                self.iou_threshold
            ),

            "class_count": len(
                self.model.names
            ),

            "classes": self.model.names,
        }


# ============================================================
# SINGLE DETECTOR INSTANCE
# ============================================================

# The model is loaded once when Flask imports
# this module. All requests reuse the same model.

detector = VehicleDamageDetector()