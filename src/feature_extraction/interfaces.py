from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

@dataclass
class FeatureVector:
    embedding: np.ndarray      # shape: (embedding_dim,)
    model_name: str            # hangi model kullanıldı
    extraction_timestamp: str
    source_image_id: str       # izlenebilirlik için

class IFeatureExtractor(ABC):
    @abstractmethod
    def extract(self, image: np.ndarray, source_image_id: str = "unknown") -> FeatureVector:
        """
        Kırpılmış kaplumbağa yüzünden feature vector (embedding) çıkarır.
        
        Args:
            image (np.ndarray): Kırpılmış görüntü (RGB). Shape genellikle (224, 224, 3) şeklindedir.
            source_image_id (str): Görüntünün kimliği.
            
        Returns:
            FeatureVector: Çıkarılan özellik vektörü ve meta veriler.
        """
        pass
