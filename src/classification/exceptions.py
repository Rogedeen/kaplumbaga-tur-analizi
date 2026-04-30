class ClassificationError(Exception):
    """Sınıflandırma işlemleri sırasındaki temel hata sınıfı."""
    pass

class ModelLoadError(ClassificationError):
    """Model ağırlıkları yüklenirken oluşan hata."""
    pass
