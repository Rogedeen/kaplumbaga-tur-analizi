import pytest
import numpy as np
from src.classification.config import ClassificationConfig
from src.classification.confidence_calibrator import ConfidenceCalibrator
from src.classification.species_registry import SpeciesRegistry
from src.classification.softmax_classifier import SoftmaxClassifier
from src.feature_extraction.interfaces import FeatureVector

def test_softmax_classifier():
    config = ClassificationConfig(INPUT_DIM=512, NUM_CLASSES=5, HIGH_CONFIDENCE_THRESHOLD=0.80, LOW_CONFIDENCE_THRESHOLD=0.50)
    calibrator = ConfidenceCalibrator(config)
    registry = SpeciesRegistry()
    classifier = SoftmaxClassifier(config, calibrator, registry)
    
    # Mock FeatureVector
    fv = FeatureVector(
        embedding=np.random.rand(512),
        model_name="mock_model",
        extraction_timestamp="2026-04-30T10:00:00Z",
        source_image_id="img_123"
    )
    
    result = classifier.classify(fv)
    
    assert result.source_image_id == "img_123"
    assert len(result.top_predictions) <= 3
    
    # Eşik altı tahminde "güvenli" olarak işaretlenemiyor (unit test ile kanıtlı)
    if result.confidence < 0.80:
        assert result.is_confident is False
        
    if result.confidence < 0.50:
        assert result.predicted_species is None

def test_softmax_classifier_uncertain():
    config = ClassificationConfig(INPUT_DIM=512, NUM_CLASSES=5, HIGH_CONFIDENCE_THRESHOLD=0.99, LOW_CONFIDENCE_THRESHOLD=0.99)
    calibrator = ConfidenceCalibrator(config)
    registry = SpeciesRegistry()
    classifier = SoftmaxClassifier(config, calibrator, registry)
    
    # Mock FeatureVector
    fv = FeatureVector(
        embedding=np.random.rand(512),
        model_name="mock_model",
        extraction_timestamp="2026-04-30T10:00:00Z",
        source_image_id="img_123"
    )
    
    result = classifier.classify(fv)
    
    assert result.predicted_species is None
    assert result.is_confident is False
