from dataclasses import dataclass

@dataclass
class ImageProcessingConfig:
    min_width: int = 100
    min_height: int = 100
    max_size: int = 1024
    confidence_threshold: float = 0.5
    padding_percent: float = 0.2
    target_size: tuple[int, int] = (224, 224)
    imagenet_mean: tuple[float, float, float] = (0.485, 0.456, 0.406)
    imagenet_std: tuple[float, float, float] = (0.229, 0.224, 0.225)
