import numpy as np
from datetime import datetime
from typing import List

from .interfaces import IClassifier, ClassificationResult, Prediction
from .confidence_calibrator import ConfidenceCalibrator
from .species_registry import SpeciesRegistry
from .config import ClassificationConfig
from src.feature_extraction.interfaces import FeatureVector

class SoftmaxClassifier(IClassifier):
    def __init__(self, 
                 config: ClassificationConfig, 
                 calibrator: ConfidenceCalibrator, 
                 registry: SpeciesRegistry):
        self.config = config
        self.calibrator = calibrator
        self.registry = registry
        self.model_version = "v1.0-imagenet"
        
        # ImageNet kaplumbağa ID'leri
        self.turtle_classes = {
            33: {"species": "Caretta caretta", "common_name": "Loggerhead"},
            34: {"species": "Dermochelys coriacea", "common_name": "Leatherback"},
            35: {"species": "Kinosternidae", "common_name": "Mud Turtle"},
            36: {"species": "Malaclemys terrapin", "common_name": "Terrapin"},
            37: {"species": "Terrapene", "common_name": "Box Turtle"}
        }

    def classify(self, feature_vector: FeatureVector) -> ClassificationResult:
        try:
            logits = np.array(feature_vector.embedding)
            if logits.shape[0] != 1000:
                raise ValueError("Expected 1000-dim ImageNet logits")
                
            # Softmax
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / exp_logits.sum()
            
            top_idx = int(np.argmax(probs))
            confidence = float(probs[top_idx])
            
            is_confident = self.calibrator.is_confident(confidence)
            
            if top_idx in self.turtle_classes:
                info = self.turtle_classes[top_idx]
                pred = Prediction(species=info["species"], confidence=confidence, common_name=info["common_name"])
                predicted_species = info["species"] if not self.calibrator.is_uncertain(confidence) else "Low Confidence"
            else:
                pred = Prediction(species="Not a Turtle", confidence=confidence, common_name="Unknown Object")
                predicted_species = "Not a Turtle"
                
            return ClassificationResult(
                predicted_species=predicted_species,
                confidence=confidence,
                is_confident=is_confident,
                top_predictions=[pred],
                model_version=self.model_version,
                classification_timestamp=datetime.now().isoformat(),
                source_image_id=feature_vector.source_image_id
            )
        except Exception as e:
            return ClassificationResult(
                predicted_species="Error",
                confidence=0.0,
                is_confident=False,
                top_predictions=[],
                model_version=self.model_version,
                classification_timestamp=datetime.now().isoformat(),
                source_image_id=feature_vector.source_image_id
            )
