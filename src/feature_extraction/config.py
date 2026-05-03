from dataclasses import dataclass

@dataclass
class FeatureExtractionConfig:
    """Configuration for feature extraction model."""
    model_name: str = "resnet18_metric_learning"
    embedding_dim: int = 512  # ResNet18 fc layer input dimension (L2 normalized)
    pretrained: bool = True
    freeze_strategy: str = "all"  # 'all' means freeze all conv layers
    
    # Input image expected parameters
    input_size: tuple = (256, 256)
    crop_size: tuple = (160, 160) # High zoom on the center of the scute area
    mean: tuple = (0.5, 0.5, 0.5)
    std: tuple = (0.225, 0.225, 0.225) # Boosting contrast to emphasize textures
