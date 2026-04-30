### Kaynak 1: [Local Ocean Conservation - Sea Turtle Face Detection (Zindi)](https://github.com/HamzaGbada/Local-Ocean-Conservation-Sea-Turtle-Face-Detection)
- **URL:** https://github.com/HamzaGbada/Local-Ocean-Conservation-Sea-Turtle-Face-Detection
- **Tür:** GitHub Repo / Yarışma Çözümü
- **Yöntem:** Bounding box tabanlı kafa ölçek deseni (scale pattern) kırpma.
- **Doğruluk:** Yarışma metriği IoU üzerinden değerlendirildi.
- **Veri Seti:** Zindi LOC (Local Ocean Conservation)
- **Yeniden Kullanılabilir Kod:** Evet
- **Notlar:** Model yüzdeki pulları (scale patterns) belirlemek için kullanılıyor.

### Kaynak 2: [SeaTurtles_Images](https://github.com/kim2429/SeaTurtles_Images)
- **URL:** https://github.com/kim2429/SeaTurtles_Images
- **Tür:** GitHub Repo / Veri Seti
- **Yöntem:** Bounding box ve polygon formatlarında etiketleme.
- **Doğruluk:** N/A (Veri seti)
- **Veri Seti:** iNaturalist ve Google Görseller'den toplanmış veri seti.
- **Yeniden Kullanılabilir Kod:** N/A
- **Notlar:** Çeşitli açılardan ve zeminlerden (sualtı/kara) toplanmış veriler, modelin genelleme başarısını artırmak için kullanılabilir.

### Kaynak 3: [Deep learning-based image classification for imported turtle species](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10709346/)
- **URL:** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10709346/
- **Tür:** Makale (Scientific Reports)
- **Yöntem:** SSD (Single Shot MultiBox Detector) modellerinin CNN backbone'lar (ResNet, DenseNet, VGGNet vb.) ile karşılaştırılması.
- **Doğruluk:** ResNet18 backbone kullanan SSD modeli %88.1 mAP (mean Average Precision) sağladı.
- **Veri Seti:** 36 ithal kaplumbağa türü veri seti.
- **Yeniden Kullanılabilir Kod:** Hayır
- **Notlar:** ResNet18 hızlı çıkarım (inference) ve yüksek doğruluk için dengeli bir temel (baseline) oluşturuyor.

### Kaynak 4: [Comparison of YOLOv5 and YOLOv5-seg for sea turtle monitoring](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313323)
- **URL:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0313323
- **Tür:** Makale (PLOS ONE)
- **Yöntem:** Nesne Tespiti (YOLOv5) ile Örnek Bölütleme (Instance Segmentation - YOLOv5-seg) karşılaştırması.
- **Doğruluk:** YOLOv5-seg daha üstün performans gösterdi.
- **Veri Seti:** Sualtı ve karmaşık arka planlı kaplumbağa veri setleri.
- **Yeniden Kullanılabilir Kod:** Kısmen (Mimari bilindiği için YOLOv5 reposu kullanılabilir)
- **Notlar:** Karmaşık sualtı arka planlarında örnek bölütleme (instance segmentation) bbox tabanlı nesne tespitine kıyasla daha başarılıdır.

### Kaynak 5: [turtleRecall - CNN for Turtle Recognition](https://github.com/dhesenkamp/turtleRecall)
- **URL:** https://github.com/dhesenkamp/turtleRecall
- **Tür:** GitHub Repo / Yarışma
- **Yöntem:** Derin CNN ile görüntü sınıflandırma.
- **Doğruluk:** Belirtilmemiş
- **Veri Seti:** Zindi LOC
- **Yeniden Kullanılabilir Kod:** Evet (Colab Notebook'u içeriyor)
- **Notlar:** Pipeline Colab üzerinden online GBucket'tan veri okuyarak çalışabiliyor.

### Kaynak 6: [Zindi-LOC-Sea-Turtle-Face-Detector](https://github.com/vbookshelf/Zindi-LOC-Sea-Turtle-Face-Detector)
- **URL:** https://github.com/vbookshelf/Zindi-LOC-Sea-Turtle-Face-Detector
- **Tür:** GitHub Repo / Yarışma
- **Yöntem:** Segmentation + Connected Components (MobileNet encoder + U-Net decoder).
- **Doğruluk:** Leaderboard IOU: 0.828 (MobileNet) / ~0.87 (DenseNet161).
- **Veri Seti:** Zindi LOC
- **Yeniden Kullanılabilir Kod:** Evet
- **Notlar:** MobileNet tabanlı model sadece 27MB boyutunda ve oldukça hızlı çalışıyor, bu nedenle üretim ortamında mobil/edge deployment için ideal bir yaklaşım.
