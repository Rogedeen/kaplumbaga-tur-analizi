import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.api.app import app
from src.image_processing.interfaces import DetectionResult, BoundingBox
from src.feature_extraction.interfaces import FeatureVector
from src.classification.interfaces import ClassificationResult, Prediction

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("src.api.app.pipeline")
@patch("src.api.app.extractor")
@patch("src.api.app.classifier")
def test_predict_success(mock_classifier, mock_extractor, mock_pipeline):
    """Test predict endpoint with successful pipeline execution."""
    # Mocking pipeline
    mock_pipeline.process_image.return_value = DetectionResult(
        success=True,
        bbox=BoundingBox(x=10, y=10, w=100, h=100),
        confidence=0.95,
        cropped_image=None,  # Not used in test, only passed down
        error_message=None
    )
    
    # Mocking extractor
    import numpy as np
    mock_extractor.extract.return_value = FeatureVector(
        embedding=np.zeros(512),
        model_name="resnet18",
        extraction_timestamp="2026-04-30T10:00:00Z",
        source_image_id="test.jpg"
    )
    
    # Mocking classifier
    mock_classifier.classify.return_value = ClassificationResult(
        predicted_species="Caretta caretta",
        confidence=0.88,
        is_confident=True,
        top_predictions=[
            Prediction(species="Caretta caretta", confidence=0.88, common_name="Loggerhead"),
            Prediction(species="Chelonia mydas", confidence=0.10, common_name="Green Turtle")
        ],
        model_version="v1.0",
        classification_timestamp="2026-04-30T10:00:01Z",
        source_image_id="test.jpg"
    )
    
    # Send request
    file_content = b"fake image content"
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", file_content, "image/jpeg")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["predicted_species"] == "Caretta caretta"
    assert data["common_name"] == "Loggerhead"
    assert data["confidence"] == 0.88
    assert data["is_confident"] is True
    assert len(data["top_predictions"]) == 2
    assert data["metadata"]["model_version"] == "v1.0"
    assert data["metadata"]["face_bbox"] == {"x": 10, "y": 10, "w": 100, "h": 100}

@patch("src.api.app.pipeline")
def test_predict_detection_failure(mock_pipeline):
    """Test predict endpoint when image processing fails."""
    mock_pipeline.process_image.return_value = DetectionResult(
        success=False,
        bbox=None,
        confidence=0.0,
        cropped_image=None,
        error_message="No face detected"
    )
    
    file_content = b"fake image content"
    response = client.post(
        "/predict",
        files={"file": ("test.jpg", file_content, "image/jpeg")}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "No face detected"

def test_predict_no_file():
    """Test predict endpoint without a file."""
    response = client.post("/predict")
    assert response.status_code == 422  # Unprocessable Entity (FastAPI validation)
