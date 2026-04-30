from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
from src.feature_extraction.interfaces import FeatureVector

@dataclass
class Prediction:
    species: str
    confidence: float
    common_name: Optional[str]

@dataclass
class ClassificationResult:
    predicted_species: Optional[str]
    confidence: float
    is_confident: bool
    top_predictions: List[Prediction]
    model_version: str
    classification_timestamp: str
    source_image_id: str

class IClassifier(ABC):
    @abstractmethod
    def classify(self, feature_vector: FeatureVector) -> ClassificationResult:
        """
        Özellik vektörünü alır ve tür sınıflandırması yapar.
        
        Args:
            feature_vector (FeatureVector): Özellik çıkarımından gelen vektör.
            
        Returns:
            ClassificationResult: Sınıflandırma sonucu ve metadatalar.
        """
        pass
