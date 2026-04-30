# Clean Code Kuralları — TurtleVision

Tüm ajanlar bu kurallara uymak zorundadır.
Doğrulayıcı Ajan PR incelemesinde bu listeyi kontrol eder.

---

## İsimlendirme

### Değişkenler — Ne olduklarını söylesin
```python
# YANLIŞ
x = detect(img)
d = 0.85
res = model.predict(f)

# DOĞRU
detection_result = detect(image)
confidence_threshold = 0.85
classification_result = model.predict(feature_vector)
```

### Fonksiyonlar — Ne yaptıklarını söylesin (fiil ile başla)
```python
# YANLIŞ
def data(image): ...
def process(image): ...
def run(): ...

# DOĞRU
def extract_face_region(image: np.ndarray) -> DetectionResult: ...
def normalize_image(image: np.ndarray) -> np.ndarray: ...
def classify_turtle_species(features: FeatureVector) -> ClassificationResult: ...
```

### Sınıflar — İsim olsun, ne olduklarını söylesin
```python
# YANLIŞ
class Manager: ...
class Handler: ...
class Processor: ...

# DOĞRU
class EfficientNetFeatureExtractor: ...
class TurtleFaceDetector: ...
class SpeciesClassifier: ...
```

### Boolean değişkenler — `is_` veya `has_` ile başla
```python
# YANLIŞ
confident = confidence > threshold
detected = bbox is not None

# DOĞRU
is_confident = confidence > HIGH_THRESHOLD
has_face_detected = bbox is not None
```

---

## Fonksiyonlar

### Tek şey yap
```python
# YANLIŞ — hem tespit hem normalizasyon hem loglama yapıyor
def process_image(image, log=True):
    bbox = detect_face(image)
    normalized = normalize(image[bbox])
    if log:
        write_log(bbox, normalized)
    return normalized

# DOĞRU — her şey ayrı
def detect_face(image: np.ndarray) -> DetectionResult: ...
def normalize_crop(image: np.ndarray, bbox: BoundingBox) -> np.ndarray: ...
def log_detection(result: DetectionResult) -> None: ...
```

### Kısa tut (20 satır hedef, 40 satır mutlak üst sınır)
Bir fonksiyon 40 satırı geçiyorsa, büyük ihtimalle birden fazla iş yapıyordur.

### Flag parametresi alma
```python
# YANLIŞ — flag, fonksiyonun iki iş yaptığının işareti
def load_model(path, use_gpu=True): ...

# DOĞRU — ayrı fonksiyonlar
def load_model_on_gpu(path: str) -> Model: ...
def load_model_on_cpu(path: str) -> Model: ...
```

### Argüman sayısı (maksimum 3)
```python
# YANLIŞ
def create_result(img, bbox, conf, model, timestamp, source, version): ...

# DOĞRU — dataclass kullan
@dataclass
class ClassificationInput:
    image: np.ndarray
    bbox: BoundingBox
    model_version: str

def classify(input: ClassificationInput) -> ClassificationResult: ...
```

---

## Magic Number Yasak

```python
# YANLIŞ
if confidence > 0.7:
    ...
image = cv2.resize(image, (224, 224))

# DOĞRU — config veya named constant
HIGH_CONFIDENCE_THRESHOLD = 0.7  # config.py'dan

MODEL_INPUT_SIZE = (224, 224)     # config.py'dan

if confidence > config.HIGH_CONFIDENCE_THRESHOLD:
    ...
image = cv2.resize(image, config.MODEL_INPUT_SIZE)
```

---

## Yorumlar

### "Neden"i açıkla, "ne"yi tekrarlama
```python
# YANLIŞ — kodu tekrar ediyor
# Confidence'ı hesapla
confidence = softmax(logits).max()

# DOĞRU — neden yapıldığını açıklıyor
# Calibration sonrası ham softmax skoru kullanılıyor;
# Platt scaling uygulanmadı (araştırma önerisi: veri seti küçük olduğunda kalibre edilmiş değer daha güvenilir)
confidence = softmax(logits).max()
```

### Güncel olmayan yorum yasak
Kod değiştiyse yorum da değişmeli. Yorum kod'dan daha tehlikeli yalan söyler.

---

## Hata Yönetimi

```python
# YANLIŞ — tüm istisnaları yutma
try:
    result = detect(image)
except:
    return None

# YANLIŞ — genel Exception
except Exception as e:
    print(e)

# DOĞRU — spesifik exception, anlamlı mesaj
try:
    result = detect(image)
except InvalidImageError as e:
    logger.error(f"Invalid image format: {e}")
    raise
except ModelNotLoadedError as e:
    logger.error(f"Model not initialized: {e}")
    raise DetectionError(f"Cannot detect face: model unavailable") from e
```

---

## Type Hints — Zorunlu

```python
# YANLIŞ — tip bilgisi yok
def detect(image):
    ...

# DOĞRU — her parametre ve dönüş tipi belirtilmiş
def detect(image: np.ndarray) -> DetectionResult:
    ...
```

---

## Docstring — Public Her Şey İçin Zorunlu

```python
def extract_face_region(image: np.ndarray, config: DetectionConfig) -> DetectionResult:
    """
    Kaplumbağa görüntüsünden yüz bölgesini tespit eder ve kırpılmış görüntü döndürür.

    Args:
        image: RGB formatında numpy array, shape (H, W, 3)
        config: Tespit için eşik ve boyut ayarları

    Returns:
        DetectionResult: Tespit sonucu, başarısız durumda success=False

    Raises:
        InvalidImageError: Görüntü okunamıyorsa veya minimum boyutun altındaysa
    """
    ...
```

---

## Özet Kontrol Tablosu

| Kural | Kontrol | Geçme Koşulu |
|-------|---------|--------------|
| İsimlendirme | Değişken adı ne olduğunu söylüyor mu? | Evet |
| Fonksiyon uzunluğu | 40 satırı geçiyor mu? | Hayır |
| Magic number | Kodda sabit sayı var mı? | Hayır |
| Type hints | Her public fonksiyon tipli mi? | Evet |
| Docstring | Her public metot açıklamalı mı? | Evet |
| Hata yönetimi | Bare `except:` var mı? | Hayır |
| Yorum kalitesi | Yorum kodu tekrar mı ediyor? | Hayır |
