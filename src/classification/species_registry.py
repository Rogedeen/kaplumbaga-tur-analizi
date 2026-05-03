from typing import Dict, Optional, Any

class SpeciesRegistry:
    def __init__(self):
        # Tür bilgileri ve onlardan beklenen fiziksel (sembolik) özelliklerin veri tabanı.
        # Bu yapı sayesinden sistem "if/else" kodlarına bağlı kalmadan yeni türlere kolayca ölçeklenebilir.
        self._registry: Dict[int, Dict[str, Any]] = {
            0: {
                "species": "Chelydra serpentina",
                "common_name": "Bayağı Kapan Kaplumbağa",
                "expected_traits": {
                    "texture_complexity": {"threshold": 0.5, "reason": "Yüksek doku yoğunluğu ve boyun pürüzleri tespit edildi."}
                }
            },
            1: {
                "species": "Terrapene ornata ssp. Luteola",
                "common_name": "Çöl Kutu Kaplumbağası",
                "expected_traits": {
                    "yellow_pattern_score": {"threshold": 0.4, "reason": "Yüzde belirgin sarı benek deseni tespit edildi."}
                }
            },
            2: {
                "species": "Trachemys scripta",
                "common_name": "Kızıl Yanaklı Su Kaplumbağası",
                "expected_traits": {
                    "red_stripe_score": {"threshold": 0.4, "reason": "Göz arkasında ayırt edici kırmızı şerit tespit edildi."},
                    "parallel_lines_score": {"threshold": 0.4, "reason": "Yüzde ve boyunda paralel yatay çizgiler saptandı."}
                }
            },
            3: {
                "species": "Macrochelys suwanniensis",
                "common_name": "Suwannee Timsah Kapan Kaplumbağası",
                "expected_traits": {
                    "beak_sharpness": {"threshold": 0.5, "reason": "Keskin ve kancalı şahin gagası yapısı tespit edildi."}
                }
            },
            4: {
                "species": "Chelonia mydas",
                "common_name": "Yeşil Deniz Kaplumbağası",
                "expected_traits": {
                    # Örneğin ileride OpenCV ile çift prefrontal pul ölçüldüğünde buraya eklenebilir.
                }
            }
        }

    def get_species_info(self, class_idx: int) -> Optional[Dict[str, Any]]:
        """Sınıf indeksine göre tür bilgisini döndürür."""
        return self._registry.get(class_idx)

    def get_num_classes(self) -> int:
        """Kayıtlı tür sayısını döndürür."""
        return len(self._registry)
