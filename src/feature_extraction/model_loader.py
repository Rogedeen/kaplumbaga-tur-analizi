import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from .config import FeatureExtractionConfig
from .exceptions import ModelLoadError
import logging

logger = logging.getLogger(__name__)

class MetricLearningResNet(nn.Module):
    """
    Kaplumbağa yüz pullarını (scale patterns) analiz etmek ve 
    Siamese Network/Metric Learning altyapısına uygun L2-normalize 
    özellik vektörü (embedding) çıkarmak için ResNet18 wrapper'ı.
    """
    def __init__(self, config: FeatureExtractionConfig):
        super().__init__()
        weights = ResNet18_Weights.IMAGENET1K_V1 if config.pretrained else None
        self.backbone = resnet18(weights=weights)
        
        # Sınıflandırma katmanını iptal edip, sadece özellikleri (512-dim) alıyoruz.
        self.backbone.fc = nn.Identity()
        
        if config.freeze_strategy == "all":
            # Tüm parametreleri dondur
            for param in self.backbone.parameters():
                param.requires_grad = False
                
    def forward(self, x):
        features = self.backbone(x)
        # Metric Learning için özellikleri L2 normalize et
        # Bu işlem kosinüs benzerliğini Öklid mesafesine bağlar ve aynı kaplumbağa
        # resimlerinin birbirine yakınlaşmasını sağlar.
        features = torch.nn.functional.normalize(features, p=2, dim=1)
        return features

class ModelLoader:
    """Yükleme, konfigürasyon ve device yönetimini yapar."""
    
    @staticmethod
    def get_device() -> torch.device:
        """
        Sistemde kullanılabilir olan en uygun işlem birimini (CUDA, MPS veya CPU) belirler.
        
        Returns:
            torch.device: PyTorch'un kullanacağı işlem birimi.
        """
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")

    @classmethod
    def load_resnet18(cls, config: FeatureExtractionConfig) -> nn.Module:
        """
        Zindi LOC Sea Turtle veriseti mantığına uygun olarak, 
        kaplumbağa yüz pullarından özellik çıkarmak için hazırlanmış
        Metric Learning modelini yükler.
        """
        try:
            device = cls.get_device()
            logger.info(f"Yükleme için seçilen device: {device}")
            
            model = MetricLearningResNet(config)
            
            model = model.to(device)
            model.eval() # Çıkarım modunda olduğumuzdan emin olalım
            
            return model
            
        except Exception as e:
            logger.error(f"Model yüklenirken hata oluştu: {str(e)}")
            raise ModelLoadError(f"Model yüklenemedi: {str(e)}")
