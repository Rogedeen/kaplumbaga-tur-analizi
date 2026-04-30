from abc import ABC, abstractmethod
import numpy as np
from typing import Optional
from dataclasses import dataclass

@dataclass
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

@dataclass
class DetectionResult:
    success: bool
    bbox: Optional[BoundingBox]
    confidence: float
    cropped_image: Optional[np.ndarray]
    error_message: Optional[str]

class IImagePreprocessor(ABC):
    @abstractmethod
    def validate(self, image: np.ndarray) -> bool:
        pass

    @abstractmethod
    def resize_for_detection(self, image: np.ndarray) -> np.ndarray:
        pass

    @abstractmethod
    def normalize_for_model(self, image: np.ndarray) -> np.ndarray:
        pass

class IFaceDetector(ABC):
    @abstractmethod
    def detect(self, image: np.ndarray) -> tuple[Optional[BoundingBox], float]:
        """Returns the bounding box and confidence score."""
        pass
