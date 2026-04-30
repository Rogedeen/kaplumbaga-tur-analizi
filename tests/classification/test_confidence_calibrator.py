import pytest
from src.classification.config import ClassificationConfig
from src.classification.confidence_calibrator import ConfidenceCalibrator

def test_confidence_calibrator():
    config = ClassificationConfig(
        HIGH_CONFIDENCE_THRESHOLD=0.80,
        LOW_CONFIDENCE_THRESHOLD=0.50
    )
    calibrator = ConfidenceCalibrator(config)
    
    # High confidence (>= 0.80)
    assert calibrator.is_confident(0.85) is True
    assert calibrator.is_confident(0.80) is True
    assert calibrator.is_confident(0.79) is False
    
    # Low confidence (0.50 <= x < 0.80)
    assert calibrator.is_low_confidence(0.70) is True
    assert calibrator.is_low_confidence(0.50) is True
    assert calibrator.is_low_confidence(0.49) is False
    assert calibrator.is_low_confidence(0.85) is False
    
    # Uncertain (< 0.50)
    assert calibrator.is_uncertain(0.40) is True
    assert calibrator.is_uncertain(0.50) is False
    assert calibrator.is_uncertain(0.85) is False
