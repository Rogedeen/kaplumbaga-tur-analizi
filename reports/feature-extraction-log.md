# Feature Extraction Log

## [2026-05-01 00:50] Çalıştırma 2 (Metric Learning / Siamese Network Update)

**Model:** resnet18_metric_learning (MetricLearningResNet)
**Freeze stratejisi:** all (sadece çıkarım yapılıyor)
**Embedding boyutu:** 512 (L2 Normalize edilmiş)
**Notlar:** Gelen bildirim üzerine Zindi LOC dataset yapısına ve yüz pulları analizine uygun olarak Metric Learning yaklaşımına geçildi. Orijinal ResNet18 sınıflandırma katmanı (fc) iptal edildi, çıkarılan özellik vektörleri `torch.nn.functional.normalize` ile Euclidean mesafeyi kosinüs benzerliğine bağlayacak şekilde L2 normalizasyonundan geçirildi. Boyut tekrar 512'ye sabitlendi.

---

## [2026-04-30 22:53] Çalıştırma 1 (Initial Setup)

**Model:** resnet18
**Freeze stratejisi:** all (tüm conv katmanları donduruldu)
**Embedding boyutu:** 512
**İşlenen görüntü sayısı:** 0 (Test/Kurulum)
**Ortalama çıkarım süresi:** N/A
**Device:** CPU / GPU (Otomatik seçilecek)
**Notlar:** Özellik çıkarım ajanı altyapısı kuruldu, ResNet18 model loader ve extractor kodları eklendi. Testler hazırlandı.
