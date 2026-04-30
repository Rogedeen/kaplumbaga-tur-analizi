import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from src.image_processing import (
    ImageProcessingPipeline,
    DefaultImagePreprocessor,
    SegmentationFaceDetector,
    ImageProcessingConfig
)
from src.feature_extraction.resnet_extractor import ResNetExtractor
from src.classification import (
    SoftmaxClassifier,
    ConfidenceCalibrator,
    SpeciesRegistry,
    ClassificationConfig
)

app = FastAPI(title="TurtleVision API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
image_config = ImageProcessingConfig()
preprocessor = DefaultImagePreprocessor(image_config)
detector = SegmentationFaceDetector(image_config)
pipeline = ImageProcessingPipeline(preprocessor, detector, image_config)

extractor = ResNetExtractor()

class_config = ClassificationConfig()
calibrator = ConfidenceCalibrator(class_config)
registry = SpeciesRegistry()
classifier = SoftmaxClassifier(class_config, calibrator, registry)


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Kullanıcıdan bir kaplumbağa görüntüsü (UploadFile) alır ve sırasıyla;
    1. Yüz tespiti ve kırpma (Image Processing),
    2. Özellik vektörü çıkarımı (Feature Extraction),
    3. Tür sınıflandırması (Classification)
    işlemlerinden geçirir.
    
    Args:
        file (UploadFile): Tahmin edilecek kaplumbağa görüntüsü.
        
    Returns:
        Dict[str, Any]: Tahmin sonucu, güven skoru (confidence) ve işlemlerle ilgili metadata bilgileri.
        
    Raises:
        HTTPException: Dosya yüklenemezse veya tespit başarısız olursa 400 döner. İşlem esnasında hata çıkarsa 500 döner.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    # Save the file temporarily
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        
    try:
        # Step 1: Image Processing (Face Detection & Cropping)
        detection_result = pipeline.process_image(temp_path)
        if not detection_result.success:
            raise HTTPException(status_code=400, detail=detection_result.error_message)
            
        # Step 2: Feature Extraction
        feature_vector = extractor.extract(detection_result.cropped_image, source_image_id=file.filename)
        
        # Step 3: Classification
        classification_result = classifier.classify(feature_vector)
        
        # Prepare response
        return {
            "success": True,
            "predicted_species": classification_result.predicted_species,
            "confidence": classification_result.confidence,
            "is_confident": classification_result.is_confident,
            "top_predictions": [
                {
                    "species": pred.species,
                    "confidence": pred.confidence,
                    "common_name": pred.common_name
                }
                for pred in classification_result.top_predictions
            ],
            "metadata": {
                "model_version": classification_result.model_version,
                "timestamp": classification_result.classification_timestamp,
                "face_bbox": {
                    "x": detection_result.bbox.x,
                    "y": detection_result.bbox.y,
                    "w": detection_result.bbox.w,
                    "h": detection_result.bbox.h
                } if detection_result.bbox else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
def health_check():
    """
    API'nin ve orkestre edilen modüllerin ayakta olup olmadığını kontrol eder.
    
    Returns:
        dict: Sağlık durumunu belirten {'status': 'healthy'} sözlüğü.
    """
    return {"status": "healthy"}
