import pytest
import numpy as np
from src.feature_extraction.resnet_extractor import ResNetExtractor
from src.feature_extraction.config import FeatureExtractionConfig
from src.feature_extraction.interfaces import FeatureVector
from src.feature_extraction.exceptions import ExtractionError

@pytest.fixture
def extractor():
    config = FeatureExtractionConfig(pretrained=False) # Hızlı test için pretrained indiremeyebilir
    return ResNetExtractor(config)

def test_extract_valid_image(extractor):
    # Dummy image: 224x224 RGB
    dummy_image = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
    
    result = extractor.extract(dummy_image, source_image_id="test_image_1")
    
    assert isinstance(result, FeatureVector)
    assert result.source_image_id == "test_image_1"
    assert result.model_name == "resnet18_metric_learning"
    assert result.embedding.shape == (512,)
    assert isinstance(result.extraction_timestamp, str)

def test_extract_invalid_input_type(extractor):
    with pytest.raises(ExtractionError):
        extractor.extract(None, "test")

def test_extract_deterministic_output(extractor):
    # Aynı girdiyle iki kez çalıştırıldığında aynı sonucu vermelidir
    dummy_image = np.ones((224, 224, 3), dtype=np.uint8) * 128
    
    result1 = extractor.extract(dummy_image, "img1")
    result2 = extractor.extract(dummy_image, "img2")
    
    np.testing.assert_array_almost_equal(result1.embedding, result2.embedding)
