import pytest
import numpy as np
from src.classification.config import ClassificationConfig
from src.classification.confidence_calibrator import ConfidenceCalibrator
from src.classification.species_registry import SpeciesRegistry
from src.classification.similarity_classifier import SimilarityClassifier
from src.feature_extraction.interfaces import FeatureVector

def test_similarity_classifier():
    config = ClassificationConfig(INPUT_DIM=512, NUM_CLASSES=5, HIGH_CONFIDENCE_THRESHOLD=0.80, LOW_CONFIDENCE_THRESHOLD=0.50)
    calibrator = ConfidenceCalibrator(config)
    registry = SpeciesRegistry()
    classifier = SimilarityClassifier(config, calibrator, registry)
    
    # Referanslardan biriyle tam eşleşen (perfect match) bir vektör gönderelim
    # Seed 42 olduğu için referanslar sabit
    perfect_match_vec = classifier.reference_vectors[0]
    
    fv = FeatureVector(
        embedding=perfect_match_vec,
        model_name="mock_model",
        extraction_timestamp="2026-05-01T10:00:00Z",
        source_image_id="img_123"
    )
    
    result = classifier.classify(fv)
    
    assert result.source_image_id == "img_123"
    assert len(result.top_predictions) == 3
    
    # Tam eşleşme olduğu için en az 0.99 beklenir (float precision sebebiyle)
    assert result.confidence >= 0.99
    assert result.is_confident is True
    assert result.predicted_species == registry.get_species_info(0)["species"]

def test_similarity_classifier_uncertain():
    config = ClassificationConfig(INPUT_DIM=512, NUM_CLASSES=5, HIGH_CONFIDENCE_THRESHOLD=0.99, LOW_CONFIDENCE_THRESHOLD=0.99)
    calibrator = ConfidenceCalibrator(config)
    registry = SpeciesRegistry()
    classifier = SimilarityClassifier(config, calibrator, registry)
    
    # Tamamen alakasız/rastgele bir vektör (veya ortogonal) gönderelim
    # Çok düşük bir ihtimal de olsa rastgele benzerlik yüksek çıkabilir, ama
    # threshold 0.99 olduğu için belirsiz çıkacaktır.
    fv = FeatureVector(
        embedding=np.zeros(512), # Sıfır vektörü hata verdirmeli ve exception flowa düşmeli
        model_name="mock_model",
        extraction_timestamp="2026-05-01T10:00:00Z",
        source_image_id="img_123"
    )
    
    result = classifier.classify(fv)
    
    assert result.predicted_species is None
    assert result.is_confident is False
    assert result.confidence == 0.0
