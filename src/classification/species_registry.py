from typing import Dict, Optional

class SpeciesRegistry:
    def __init__(self):
        # Hedef türlerin listesi
        self._registry: Dict[int, Dict[str, str]] = {
            0: {"species": "Chelonia mydas", "common_name": "Green Sea Turtle"},
            1: {"species": "Caretta caretta", "common_name": "Loggerhead Sea Turtle"},
            2: {"species": "Eretmochelys imbricata", "common_name": "Hawksbill Sea Turtle"},
            3: {"species": "Dermochelys coriacea", "common_name": "Leatherback Sea Turtle"},
            4: {"species": "Lepidochelys kempii", "common_name": "Kemp's Ridley Sea Turtle"}
        }

    def get_species_info(self, class_idx: int) -> Optional[Dict[str, str]]:
        """Sınıf indeksine göre tür bilgisini döndürür."""
        return self._registry.get(class_idx)

    def get_num_classes(self) -> int:
        """Kayıtlı tür sayısını döndürür."""
        return len(self._registry)
