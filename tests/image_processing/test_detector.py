import pytest
import numpy as np
from src.image_processing.config import ImageProcessingConfig
from src.image_processing.detector import SegmentationFaceDetector
from src.image_processing.interfaces import BoundingBox

@pytest.fixture
def config():
    return ImageProcessingConfig()

def test_detector_mock_mode(config):
    detector = SegmentationFaceDetector(config, model_path=None)
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    bbox, conf = detector.detect(image)
    
    assert isinstance(bbox, BoundingBox)
    assert conf == 0.95
    assert bbox.w == 40
    assert bbox.h == 40
    assert bbox.x == 30
    assert bbox.y == 30

def test_detector_real_mode_unimplemented(config):
    detector = SegmentationFaceDetector(config, model_path="dummy_path.pt")
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    with pytest.raises(NotImplementedError):
        detector.detect(image)
