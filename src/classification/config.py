from dataclasses import dataclass

@dataclass
class ClassificationConfig:
    """Sınıflandırma ajanı için yapılandırma ayarları."""
    HIGH_CONFIDENCE_THRESHOLD: float = 0.80
    LOW_CONFIDENCE_THRESHOLD: float = 0.50
    MODEL_PATH: str = "models/classification_head.pt"
    INPUT_DIM: int = 512
    NUM_CLASSES: int = 5

