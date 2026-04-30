import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from .config import FeatureExtractionConfig
from .exceptions import ModelLoadError
import logging

logger = logging.getLogger(__name__)

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
        ResNet18 modelini yükler, feature extraction için hazırlar ve device'a atar.
        """
        try:
            device = cls.get_device()
            logger.info(f"Yükleme için seçilen device: {device}")
            
            weights = ResNet18_Weights.IMAGENET1K_V1 if config.pretrained else None
            model = resnet18(weights=weights)
            
            # Sınıflandırma katmanını (fc) çıkarıp, sadece özellikleri döndürecek şekilde ayarla.
            # Identity kullanarak fc katmanını pasif hale getiriyoruz.
            model.fc = nn.Identity()
            
            if config.freeze_strategy == "all":
                # Tüm parametreleri dondur
                for param in model.parameters():
                    param.requires_grad = False
            
            model = model.to(device)
            model.eval() # Çıkarım modunda olduğumuzdan emin olalım
            
            return model
            
        except Exception as e:
            logger.error(f"Model yüklenirken hata oluştu: {str(e)}")
            raise ModelLoadError(f"Model yüklenemedi: {str(e)}")
