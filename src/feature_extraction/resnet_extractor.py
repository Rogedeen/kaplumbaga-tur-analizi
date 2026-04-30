import torch
import torchvision.transforms as transforms
import numpy as np
from datetime import datetime
from PIL import Image

from .interfaces import IFeatureExtractor, FeatureVector
from .config import FeatureExtractionConfig
from .model_loader import ModelLoader
from .exceptions import ExtractionError

class ResNetExtractor(IFeatureExtractor):
    def __init__(self, config: FeatureExtractionConfig = None):
        self.config = config or FeatureExtractionConfig()
        self.device = ModelLoader.get_device()
        self.model = ModelLoader.load_resnet18(self.config)
        
        # Ön işleme (preprocessing) adımları
        self.transform = transforms.Compose([
            transforms.Resize(self.config.input_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.config.mean, std=self.config.std)
        ])
        
    def extract(self, image: np.ndarray, source_image_id: str = "unknown") -> FeatureVector:
        """
        Kırpılmış ve normalize edilmiş kaplumbağa yüzünden feature vector (embedding) çıkarır.
        
        Args:
            image (np.ndarray): Özellik çıkarımı yapılacak girdi görüntüsü.
            source_image_id (str): Görüntünün kimliği veya yolu (loglama/izlenebilirlik için).
            
        Returns:
            FeatureVector: Çıkarılan 1D özellik vektörü ve ilgili meta veriler.
            
        Raises:
            ExtractionError: Görüntü işlenirken veya çıkarım sırasında bir hata oluşursa.
        """
        try:
            # Görüntüyü PIL Image formatına çevir
            if not isinstance(image, np.ndarray):
                raise ValueError("Girdi görüntüsü numpy dizisi olmalıdır.")
            
            # Görüntünün (H, W, C) formatında ve np.uint8 dtype olduğunu varsayıyoruz. 
            # Eğer dtype float ise [0,1] aralığındaysa dönüştürülmesi gerekebilir.
            if image.dtype != np.uint8:
                if image.max() <= 1.0:
                    image = (image * 255).astype(np.uint8)
                else:
                    image = image.astype(np.uint8)
                    
            pil_image = Image.fromarray(image)
            
            # Transform ve tensör oluşturma
            tensor_image = self.transform(pil_image)
            tensor_image = tensor_image.unsqueeze(0) # Batch boyutu (1, C, H, W)
            tensor_image = tensor_image.to(self.device)
            
            # Çıkarım
            with torch.no_grad():
                output = self.model(tensor_image)
                
            # Numpy'a çevir
            embedding = output.cpu().numpy().squeeze()
            
            # Vektörün beklenen boyutta olduğunu doğrula
            if embedding.shape[0] != self.config.embedding_dim:
                raise ValueError(f"Beklenen embedding boyutu {self.config.embedding_dim}, alınan boyut {embedding.shape[0]}")
            
            timestamp = datetime.now().isoformat()
            
            return FeatureVector(
                embedding=embedding,
                model_name=self.config.model_name,
                extraction_timestamp=timestamp,
                source_image_id=source_image_id
            )
            
        except Exception as e:
            raise ExtractionError(f"Özellik çıkarımı başarısız oldu: {str(e)}")
