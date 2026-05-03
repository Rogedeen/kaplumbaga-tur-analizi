import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict

from .interfaces import IClassifier, ClassificationResult, Prediction
from .confidence_calibrator import ConfidenceCalibrator
from .species_registry import SpeciesRegistry
from .config import ClassificationConfig
from src.feature_extraction.interfaces import FeatureVector

class SimilarityClassifier(IClassifier):
    def __init__(self, 
                 config: ClassificationConfig, 
                 calibrator: ConfidenceCalibrator, 
                 registry: SpeciesRegistry):
        self.config = config
        self.calibrator = calibrator
        self.registry = registry
        self.model_version = "v2.1-cosine-similarity-real"
        
        self.reference_vectors: Dict[int, np.ndarray] = {}
        json_path = os.path.join("src", "classification", "data", "reference_embeddings.json")
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
                for str_idx, embedding_list in data.items():
                    idx = int(str_idx)
                    vec = np.array(embedding_list, dtype=float)
                    norm = np.linalg.norm(vec)
                    if norm > 0:
                        vec = vec / norm
                    self.reference_vectors[idx] = vec
        else:
            # Testler veya JSON'un henüz oluşturulmadığı durumlar için Fallback
            np.random.seed(42)
            for idx in range(self.registry.get_num_classes()):
                vec = np.random.rand(self.config.INPUT_DIM)
                vec = vec / np.linalg.norm(vec)
                self.reference_vectors[idx] = vec

    def classify(self, feature_vector: FeatureVector, face_image: np.ndarray = None, symbolic_extractor = None) -> ClassificationResult:
        """
        Gelen özellik vektörünü bilinen referans vektörleri ile karşılaştırıp
        Kosinüs Benzerliği (Cosine Similarity) skoru üzerinden sınıflandırma yapar.
        Adım Adım Eleme (Decision Tree) ve Hybrid Neuro-Symbolic mimarisi kullanır.
        """
        try:
            target_vec = np.array(feature_vector.embedding, dtype=float)
            if target_vec.shape[0] != self.config.INPUT_DIM:
                raise ValueError(f"Beklenen vektör boyutu {self.config.INPUT_DIM}, alınan boyut {target_vec.shape[0]}")
            
            target_norm = np.linalg.norm(target_vec)
            if target_norm == 0:
                raise ValueError("Sıfır vektörü geldi.")
                
            # Gelen vektörü normalize et
            target_vec = target_vec / target_norm
            
            predictions: List[Prediction] = []
            
            reasons = []
            symbolic_features = {}
            
            # Lazy Evaluation Helper Function
            def get_trait(name: str) -> float:
                if name not in symbolic_features and symbolic_extractor and face_image is not None:
                    try:
                        symbolic_features[name] = symbolic_extractor.analyze(name, face_image)
                    except ValueError:
                        symbolic_features[name] = 0.0
                return symbolic_features.get(name, 0.0)
            
            # Tüm adaylar (0: Chelydra, 1: Terrapene, 2: Trachemys, 3: Macrochelys, 4: Chelonia)
            candidates = list(self.registry._registry.keys())
            
            # --- ADIM ADIM ELEME (Dichotomous Key / Decision Tree) ---
            if symbolic_extractor and face_image is not None:
                beak_sharpness = get_trait("beak_sharpness")
                
                # Seviye 1: Gaga Kancalılığı
                if beak_sharpness >= 0.4:
                    reasons.append("Gaga sivri/kancalı olduğu için küt gagalı otçul/hepçil türler elendi.")
                    candidates = [c for c in candidates if c in [0, 3]] # Chelydra, Macrochelys
                    
                    texture_complexity = get_trait("texture_complexity")
                    if texture_complexity >= 0.4:
                        reasons.append("Boyun ve kafada yüksek pürüz (tüberkül) olduğu için pusu grubu avcıları doğrulandı.")
                else:
                    reasons.append("Gaga küt veya hafif kavisli olduğu için yırtıcı/kancalı gagalı türler elendi.")
                    candidates = [c for c in candidates if c in [1, 2, 4]] # Terrapene, Trachemys, Chelonia
                    
                    red_stripe = get_trait("red_stripe")
                    parallel_lines = get_trait("parallel_lines")
                    yellow_pattern = get_trait("yellow_pattern")
                    
                    if red_stripe >= 0.3 or parallel_lines >= 0.3:
                        reasons.append("Yüzde belirgin renk çizgileri/bantları tespit edildiği için diğer türler elendi.")
                        candidates = [2] # Trachemys
                    elif yellow_pattern >= 0.3:
                        reasons.append("Yüzde yoğun sarı benek deseni tespit edildiği için diğer türler elendi.")
                        candidates = [1] # Terrapene
                    elif len(candidates) > 1:
                        reasons.append("Belirgin bir renk deseni veya şerit bulunamadı, sade yüzeyli türler aranıyor.")
                        
            # Kalan adaylar için Neuro-Symbolic Skorlama
            reasons_dict = {}
            for idx in candidates:
                ref_vec = self.reference_vectors.get(idx)
                if ref_vec is None:
                    continue
                    
                cos_sim = np.dot(target_vec, ref_vec)
                neuro_score = max(0.0, float(cos_sim))
                
                symbolic_score = neuro_score
                candidate_reasons = list(reasons) # Ortak eleme geçmişini kopyala
                
                # Mikro Özellik Kontrolü
                info = self.registry.get_species_info(idx)
                if info and "expected_traits" in info:
                    traits = info["expected_traits"]
                    if traits and symbolic_features:
                        total_trait_score = 0.0
                        matched_traits = 0
                        
                        for feature_name, trait_config in traits.items():
                            # Eğer trait string'i _score ile bitiyorsa kaldır (Geriye dönük uyumluluk)
                            clean_feature_name = feature_name.replace("_score", "")
                            val = get_trait(clean_feature_name)
                            if val >= trait_config["threshold"]:
                                candidate_reasons.append(trait_config["reason"])
                                total_trait_score += val
                                matched_traits += 1
                                
                        if len(traits) > 0:
                            symbolic_score = (total_trait_score / len(traits)) if matched_traits > 0 else 0.0
                            
                if not symbolic_features or symbolic_score == 0.0:
                    final_confidence = neuro_score
                else:
                    final_confidence = 0.6 * neuro_score + 0.4 * symbolic_score
                    
                reasons_dict[idx] = candidate_reasons
                
                if info:
                    predictions.append(
                        Prediction(
                            species=info["species"],
                            confidence=final_confidence,
                            common_name=info["common_name"]
                        )
                    )
                    
            # Eğer hiçbir aday kalmadıysa (çok düşük ihtimal ama fallback)
            if not predictions:
                predictions.append(Prediction(species="Unknown", confidence=0.0, common_name="Unknown"))
                reasons_dict[-1] = reasons + ["Hiçbir tür ile eşleşme sağlanamadı."]
                best_idx = -1
            else:
                # En yüksek benzerliğe göre sırala
                predictions.sort(key=lambda x: x.confidence, reverse=True)
                
                # Sadece kalan adayları (max 3) döndür
                top_predictions = predictions[:3]
                best_prediction = top_predictions[0]
                
                # En iyi tahminin id'sini bul
                best_idx = -1
                for idx, info in self.registry._registry.items():
                    if info["species"] == best_prediction.species:
                        best_idx = idx
                        break
            
            best_prediction = predictions[0]
            is_confident = self.calibrator.is_confident(best_prediction.confidence)
            predicted_species = best_prediction.species if is_confident else None
            
            final_reasons = reasons_dict.get(best_idx, [])
            if is_confident and not any("yüksek derecede uyuşuyor" in r for r in final_reasons):
                final_reasons.append(f"Derin öğrenme modeli ile %{best_prediction.confidence*100:.0f} uyuşma sağlandı.")
                
            return ClassificationResult(
                predicted_species=predicted_species,
                confidence=best_prediction.confidence,
                is_confident=is_confident,
                top_predictions=predictions[:3],
                model_version="v4.0-dichotomous-neuro-symbolic",
                classification_timestamp=datetime.now().isoformat(),
                source_image_id=feature_vector.source_image_id,
                reasons=final_reasons,
                symbolic_features=symbolic_features
            )
            
        except Exception as e:
            print("EXCEPTION IN CLASSIFY:", e)
            # Hata durumunda boş döndür
            return ClassificationResult(
                predicted_species=None,
                confidence=0.0,
                is_confident=False,
                top_predictions=[],
                model_version=self.model_version,
                classification_timestamp=datetime.now().isoformat(),
                source_image_id=feature_vector.source_image_id
            )
