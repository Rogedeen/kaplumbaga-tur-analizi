from dataclasses import dataclass

@dataclass
class FeatureExtractionConfig:
    """Configuration for feature extraction model."""
    model_name: str = "resnet18"
    embedding_dim: int = 512  # ResNet18 fc layer input dimension
    pretrained: bool = True
    freeze_strategy: str = "all"  # 'all' means freeze all conv layers
    
    # Input image expected parameters
    input_size: tuple = (224, 224)
    mean: tuple = (0.485, 0.456, 0.406)  # ImageNet means
    std: tuple = (0.229, 0.224, 0.225)   # ImageNet stds
