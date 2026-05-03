import pytest
import numpy as np
from src.image_processing.config import ImageProcessingConfig
from src.image_processing.preprocessor import DefaultImagePreprocessor
from src.image_processing.exceptions import InvalidImageError

@pytest.fixture
def preprocessor():
    config = ImageProcessingConfig(min_width=50, min_height=50, max_size=200, target_size=(224, 224))
    return DefaultImagePreprocessor(config)

def test_validate_valid_image(preprocessor):
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    assert preprocessor.validate(image) == True

def test_validate_invalid_type(preprocessor):
    with pytest.raises(InvalidImageError):
        preprocessor.validate(None)

def test_validate_invalid_resolution(preprocessor):
    image = np.zeros((40, 40, 3), dtype=np.uint8)
    with pytest.raises(InvalidImageError):
        preprocessor.validate(image)

def test_resize_for_detection(preprocessor):
    # Image larger than max_size (200)
    image = np.zeros((400, 300, 3), dtype=np.uint8)
    resized = preprocessor.resize_for_detection(image)
    h, w = resized.shape[:2]
    assert max(h, w) == 200
    assert h == 200
    assert w == 150

def test_resize_for_detection_no_resize(preprocessor):
    # Image smaller than max_size
    image = np.zeros((150, 100, 3), dtype=np.uint8)
    resized = preprocessor.resize_for_detection(image)
    assert resized.shape[:2] == (150, 100)

def test_normalize_for_model(preprocessor):
    image = np.ones((100, 100, 3), dtype=np.uint8) * 127
    normalized = preprocessor.normalize_for_model(image)
    assert normalized.shape == (224, 224, 3)
    # Check if normalized values are float and centered around 0 (approx)
    assert normalized.dtype == np.float32
    # Check if normalized values are within a reasonable range
    assert np.any(normalized != 0)
