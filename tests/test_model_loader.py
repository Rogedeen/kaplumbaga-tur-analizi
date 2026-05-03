import pytest
import torch
from src.feature_extraction.model_loader import ModelLoader
from src.feature_extraction.config import FeatureExtractionConfig

def test_get_device():
    device = ModelLoader.get_device()
    assert isinstance(device, torch.device)

def test_load_resnet18():
    config = FeatureExtractionConfig(pretrained=False)
    model = ModelLoader.load_resnet18(config)
    
    # Modelin fc katmanı Identity olmalıdır
    assert isinstance(model.backbone.fc, torch.nn.Identity)
    
    # Eval modunda olmalıdır
    assert not model.training
    
    # Freeze stratejisi "all" olduğu için requires_grad False olmalıdır
    for param in model.backbone.parameters():
        assert not param.requires_grad
