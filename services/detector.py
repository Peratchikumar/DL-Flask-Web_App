"""
Vehicle Damage Detection Service
Single YOLO26 model inference.
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
    """Loads and runs the single vehicle-damage YOLO26 model."""

    def __init__(self) -> None:
        self.model_path = Path(MODEL_PATH)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}"
            )

        # Load ONE model only
        self.model = YOLO(str(self.model_path))

    def predict(
        self,
        source: Any,
        save: bool = False,
        project: str | None = None,
        name: str | None = None,
    ):
        """
        Run vehicle-damage detection.

        Parameters
        ----------
        source:
            Image/video path or supported inference source.

        save:
            Whether to save the annotated prediction.

        project:
            Output directory.

        name:
            Output run name.

        Returns
        -------
        YOLO prediction results.
        """

        kwargs = {
            "source": source,
            "imgsz": IMAGE_SIZE,
            "conf": CONFIDENCE_THRESHOLD,
            "iou": IOU_THRESHOLD,
            "save": save,
            "verbose": False,
        }

        if project:
            kwargs["project"] = project

        if name:
            kwargs["name"] = name

        return self.model.predict(**kwargs)


# ============================================================
# SINGLE DETECTOR INSTANCE
# ============================================================

detector = VehicleDamageDetector()


def detect(
    source: Any,
    save: bool = False,
    project: str | None = None,
    name: str | None = None,
):
    """
    Convenience function for vehicle-damage detection.
    """

    return detector.predict(
        source=source,
        save=save,
        project=project,
        name=name,
    )