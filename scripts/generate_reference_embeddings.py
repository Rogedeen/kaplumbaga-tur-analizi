import os
import json
import numpy as np
import cv2

from src.image_processing.pipeline import ImageProcessingPipeline
from src.image_processing.preprocessor import DefaultImagePreprocessor
from src.image_processing.detector import SegmentationFaceDetector
from src.image_processing.config import ImageProcessingConfig

from src.feature_extraction.resnet_extractor import ResNetExtractor
from src.feature_extraction.config import FeatureExtractionConfig

def main():
    print("Starting generation of reference embeddings...")
    
    # Init Image Processing
    img_config = ImageProcessingConfig(default_model_path="yolov8s-seg.pt")
    preprocessor = DefaultImagePreprocessor(img_config)
    detector = SegmentationFaceDetector(img_config)
    pipeline = ImageProcessingPipeline(preprocessor, detector, img_config)
    
    # Init Feature Extraction
    feat_config = FeatureExtractionConfig()
    extractor = ResNetExtractor(feat_config)
    
    # Image mapping based on index
    images = {
        0: "turtle photos/1.jpeg",
        1: "turtle photos/2.jpg",
        2: "turtle photos/3.jpg",
        3: "turtle photos/4.jpg",
        4: "turtle photos/5.jpg"
    }
    
    reference_embeddings = {}
    
    for idx, img_path in images.items():
        print(f"Processing image for class {idx}: {img_path}")
        if not os.path.exists(img_path):
            print(f"ERROR: Image {img_path} not found.")
            continue
            
        result = pipeline.process_image(img_path)
        
        if result.success and result.cropped_image is not None:
            image_to_extract = result.cropped_image
        else:
            print(f"WARNING: Face detection failed for {img_path}. Error: {result.error_message}. Fallback to raw image.")
            # Fallback
            raw_img = cv2.imread(img_path)
            raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
            image_to_extract = raw_img
            
        feature_vector = extractor.extract(image_to_extract, source_image_id=str(idx))
        embedding_list = feature_vector.embedding.tolist()
        reference_embeddings[str(idx)] = embedding_list
        print(f"Successfully generated embedding for class {idx}.")
        
    out_dir = os.path.join("src", "classification", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "reference_embeddings.json")
    
    with open(out_path, "w") as f:
        json.dump(reference_embeddings, f, indent=4)
        
    print(f"Reference embeddings saved to {out_path}")

if __name__ == "__main__":
    main()
