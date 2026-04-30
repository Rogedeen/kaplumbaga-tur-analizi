from dataclasses import dataclass

@dataclass
class ImageProcessingConfig:
    min_width: int = 100
    min_height: int = 100
    max_size: int = 1024
    confidence_threshold: float = 0.5
    padding_percent: float = 0.2
    target_size: tuple[int, int] = (224, 224)
