import pytest
from src.classification.species_registry import SpeciesRegistry

def test_species_registry():
    registry = SpeciesRegistry()
    
    info = registry.get_species_info(0)
    assert info is not None
    assert info["species"] == "Chelydra serpentina"
    assert info["common_name"] == "Bayağı Kapan Kaplumbağa"
    
    assert registry.get_num_classes() == 5
    
    invalid_info = registry.get_species_info(999)
    assert invalid_info is None
