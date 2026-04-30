# SOLID Prensipleri — TurtleVision Kural Dosyası

Bu dosya tüm ajanlar için bağlayıcıdır.
Her PR, bu kurallara göre Doğrulayıcı Ajan tarafından denetlenir.

---

## S — Single Responsibility (Tek Sorumluluk)

**Kural:** Bir sınıfın değişmesi için yalnızca tek bir nedeni olmalıdır.

### Bu projede ne anlama geliyor?
```python
# YANLIŞ — YüzTespit sınıfı hem tespit hem normalizasyon yapıyor
class FaceDetector:
    def detect(self, image): ...
    def normalize(self, image): ...   # bu burada olmamalı

# DOĞRU — ayrı sınıflar
class FaceDetector:
    def detect(self, image) -> BoundingBox: ...

class ImageNormalizer:
    def normalize(self, image) -> np.ndarray: ...
```

### Kontrol sorusu:
"Bu sınıf neden değişebilir?" sorusuna birden fazla cevap varsa → ihlal.

---

## O — Open/Closed (Açık/Kapalı)

**Kural:** Sınıflar genişlemeye açık, değişikliğe kapalı olmalıdır.

### Bu projede ne anlama geliyor?
```python
# YANLIŞ — yeni model eklemek mevcut kodu değiştiriyor
class Classifier:
    def classify(self, features):
        if self.model_type == "efficientnet":
            ...
        elif self.model_type == "resnet":   # her model için elif ekleniyor
            ...

# DOĞRU — interface + implementation
class IClassifier(ABC):
    @abstractmethod
    def classify(self, features: FeatureVector) -> ClassificationResult: ...

class EfficientNetClassifier(IClassifier):
    def classify(self, features): ...

class ResNetClassifier(IClassifier):           # mevcut kod değişmedi
    def classify(self, features): ...
```

---

## L — Liskov Substitution (Liskov İkamesi)

**Kural:** Alt sınıflar, üst sınıfın yerine geçebilir olmalıdır.

### Bu projede ne anlama geliyor?
```python
# YANLIŞ — alt sınıf üst sınıfın sözleşmesini bozuyor
class IDetector(ABC):
    @abstractmethod
    def detect(self, image: np.ndarray) -> DetectionResult: ...

class MyDetector(IDetector):
    def detect(self, image):
        return None   # DetectionResult döndürmesi gerekirken None → ihlal

# DOĞRU — sözleşme tam karşılanıyor
class MyDetector(IDetector):
    def detect(self, image: np.ndarray) -> DetectionResult:
        return DetectionResult(success=False, ...)   # başarısız ama tip doğru
```

---

## I — Interface Segregation (Arayüz Ayrımı)

**Kural:** Sınıflar kullanmadıkları metodlara bağımlı olmamalıdır.

### Bu projede ne anlama geliyor?
```python
# YANLIŞ — tek dev interface
class IAgent(ABC):
    @abstractmethod
    def detect_face(self): ...     # sınıflandırma ajanı bunu kullanmıyor
    @abstractmethod
    def classify(self): ...        # görüntü işleme ajanı bunu kullanmıyor
    @abstractmethod
    def extract_features(self): ...

# DOĞRU — küçük, odaklı interfaceler
class IFaceDetector(ABC):
    @abstractmethod
    def detect(self, image: np.ndarray) -> DetectionResult: ...

class IFeatureExtractor(ABC):
    @abstractmethod
    def extract(self, image: np.ndarray) -> FeatureVector: ...

class IClassifier(ABC):
    @abstractmethod
    def classify(self, features: FeatureVector) -> ClassificationResult: ...
```

---

## D — Dependency Inversion (Bağımlılığı Tersine Çevir)

**Kural:** Üst seviye modüller, alt seviye modüllere bağımlı olmamalıdır. Her ikisi de soyutlamalara bağımlı olmalıdır.

### Bu projede ne anlama geliyor?
```python
# YANLIŞ — pipeline concrete sınıfa bağımlı
class TurtlePipeline:
    def __init__(self):
        self.detector = YoloDetector()     # concrete — bağımlılık kilitleniyor

# DOĞRU — bağımlılık dışarıdan enjekte ediliyor
class TurtlePipeline:
    def __init__(self, detector: IFaceDetector, extractor: IFeatureExtractor):
        self.detector = detector       # interface — herhangi bir implementasyon geçebilir
        self.extractor = extractor

# Kullanım
pipeline = TurtlePipeline(
    detector=YoloDetector(),
    extractor=EfficientNetExtractor()
)
```

---

## Özet Kontrol Tablosu

| Prensip | Kontrol Sorusu | Geçme Koşulu |
|---------|----------------|--------------|
| S | Bu sınıf neden değişir? | Tek bir neden |
| O | Yeni özellik eklemek için hangi dosya değişti? | Sadece yeni dosya |
| L | Alt sınıf üst sınıfın her metodunu tam karşılıyor mu? | Evet |
| I | Interface'de implement edilmeyen metot var mı? | Hayır |
| D | Constructor'da `SomeConcrete()` var mı? | Hayır (inject edilmeli) |
