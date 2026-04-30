import pytest
import numpy as np
import cv2
import os
from src.image_processing.config import ImageProcessingConfig
from src.image_processing.preprocessor import DefaultImagePreprocessor
from src.image_processing.detector import SegmentationFaceDetector
from src.image_processing.pipeline import ImageProcessingPipeline

@pytest.fixture
def pipeline():
    config = ImageProcessingConfig(min_width=50, min_height=50)
    preprocessor = DefaultImagePreprocessor(config)
    detector = SegmentationFaceDetector(config, model_path=None)
    return ImageProcessingPipeline(preprocessor, detector, config)

def test_pipeline_success(pipeline, tmp_path):
    # Create a dummy image file
    image_path = str(tmp_path / "dummy.jpg")
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(image_path, img)
    
    result = pipeline.process_image(image_path)
    
    assert result.success is True
    assert result.bbox is not None
    assert result.confidence == 0.95
    assert result.cropped_image is not None
    assert result.cropped_image.shape == (224, 224, 3)
    assert result.error_message is None

def test_pipeline_invalid_image_path(pipeline):
    result = pipeline.process_image("non_existent_file.jpg")
    
    assert result.success is False
    assert "Could not read image" in result.error_message

def test_pipeline_resolution_too_low(pipeline, tmp_path):
    image_path = str(tmp_path / "small.jpg")
    img = np.zeros((40, 40, 3), dtype=np.uint8)
    cv2.imwrite(image_path, img)
    
    result = pipeline.process_image(image_path)
    
    assert result.success is False
    assert "resolution" in result.error_message
