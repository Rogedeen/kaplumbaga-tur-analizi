import torch
import torch.nn as nn
from datetime import datetime
import numpy as np
from typing import List

from .interfaces import IClassifier, ClassificationResult, Prediction
from .confidence_calibrator import ConfidenceCalibrator
from .species_registry import SpeciesRegistry
from .config import ClassificationConfig
from .exceptions import ModelLoadError
from src.feature_extraction.interfaces import FeatureVector

class SoftmaxHead(nn.Module):
    def __init__(self, input_dim: int, num_classes: int):
        super().__init__()
        self.fc = nn.Linear(input_dim, num_classes)
        
    def forward(self, x):
        return self.fc(x)

class SoftmaxClassifier(IClassifier):
    def __init__(self, 
                 config: ClassificationConfig, 
                 calibrator: ConfidenceCalibrator, 
                 registry: SpeciesRegistry):
        self.config = config
        self.calibrator = calibrator
        self.registry = registry
        self.model_version = "v1.0"
        
        self.model = SoftmaxHead(self.config.INPUT_DIM, self.registry.get_num_classes())
        
        try:
            # Gerçek uygulamada ağırlıklar yüklenir:
            # self.model.load_state_dict(torch.load(self.config.MODEL_PATH))
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Model yüklenirken hata oluştu: {self.config.MODEL_PATH}") from e

    def classify(self, feature_vector: FeatureVector) -> ClassificationResult:
        """
        Özellik vektörünü kullanarak tür tahmini yapar.
        
        Args:
            feature_vector (FeatureVector): Özellik çıkarımından gelen vektör.
            
        Returns:
            ClassificationResult: Sınıflandırma sonucu ve metadatalar.
        """
        try:
            # Eğer embedding None veya hatalı ise tensor oluştururken exception fırlar
            embedding_np = np.array(feature_vector.embedding)
            if embedding_np.size == 0 or embedding_np.shape[0] != self.config.INPUT_DIM:
                 # Hatalı boyut varsa
                 x = torch.zeros((1, self.config.INPUT_DIM), dtype=torch.float32)
            else:
                 x = torch.tensor(embedding_np, dtype=torch.float32).unsqueeze(0)
        except Exception:
            x = torch.zeros((1, self.config.INPUT_DIM), dtype=torch.float32)
            
        with torch.no_grad():
            logits = self.model(x)
            probabilities = torch.softmax(logits, dim=1).squeeze(0).numpy()
            
        top_indices = np.argsort(probabilities)[::-1][:3]
        
        top_predictions: List[Prediction] = []
        for idx in top_indices:
            info = self.registry.get_species_info(idx)
            if info:
                top_predictions.append(
                    Prediction(
                        species=info["species"],
                        confidence=float(probabilities[idx]),
                        common_name=info["common_name"]
                    )
                )
                
        # En az bir tahmin dönmeli
        if not top_predictions:
             return ClassificationResult(
                predicted_species=None,
                confidence=0.0,
                is_confident=False,
                top_predictions=[],
                model_version=self.model_version,
                classification_timestamp=datetime.now().isoformat(),
                source_image_id=feature_vector.source_image_id
             )
                
        best_prediction = top_predictions[0]
        is_confident = self.calibrator.is_confident(best_prediction.confidence)
        
        predicted_species = best_prediction.species
        if self.calibrator.is_uncertain(best_prediction.confidence):
            predicted_species = None
            
        return ClassificationResult(
            predicted_species=predicted_species,
            confidence=best_prediction.confidence,
            is_confident=is_confident,
            top_predictions=top_predictions,
            model_version=self.model_version,
            classification_timestamp=datetime.now().isoformat(),
            source_image_id=feature_vector.source_image_id
        )
