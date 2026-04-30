from .config import ClassificationConfig

class ConfidenceCalibrator:
    def __init__(self, config: ClassificationConfig):
        self.config = config

    def is_confident(self, confidence: float) -> bool:
        """Güven skorunun yüksek güven sınırını geçip geçmediğini kontrol eder."""
        return confidence >= self.config.HIGH_CONFIDENCE_THRESHOLD

    def is_low_confidence(self, confidence: float) -> bool:
        """Güven skorunun düşük güven sınırını geçip geçmediğini kontrol eder."""
        return confidence >= self.config.LOW_CONFIDENCE_THRESHOLD and confidence < self.config.HIGH_CONFIDENCE_THRESHOLD

    def is_uncertain(self, confidence: float) -> bool:
        """Güven skorunun çok düşük olduğunu (belirsiz) kontrol eder."""
        return confidence < self.config.LOW_CONFIDENCE_THRESHOLD
