from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class ImageProcessingConfig:
    min_width: int = 100
    min_height: int = 100
    max_size: int = 1024
    confidence_threshold: float = 0.3
    padding_percent: float = 0.05
    target_size: Tuple[int, int] = (224, 224)
    imagenet_mean: Tuple[float, float, float] = (0.485, 0.456, 0.406)
    imagenet_std: Tuple[float, float, float] = (0.229, 0.224, 0.225)
    default_model_path: str = "yolov8s-seg.pt"
