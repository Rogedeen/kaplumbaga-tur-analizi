## Araştırma Sonuçları — Teknoloji Önerileri

### Model Önerisi
Kaplumbağa türü sınıflandırması ve genel kaplumbağa tespiti için Instance Segmentation (Örnek Bölütleme) yöntemleri klasik Bounding Box tabanlı Obje Tespiti yöntemlerine göre üstünlük sağlamaktadır. Özellikle PLOS ONE makalesindeki bulgulara dayanarak, karmaşık su altı arka planlarında **YOLOv5-seg (veya güncel versiyonu olan YOLOv8-seg)** kullanılması önerilir.
Tür sınıflandırması için transfer learning şarttır. *Scientific Reports* çalışması, SSD yapılarında **ResNet18** backbone kullanıldığında %88.1 mAP ile performans-hız dengesi açısından en iyi sonucu verdiğini göstermektedir.

### Yüz Tespiti Önerisi
Sadece yüz bölgesini tespit etmek istendiğinde, segmentation (bölütleme) + connected components yaklaşımı oldukça etkilidir. vbookshelf reposundaki çözüme göre, **MobileNet encoder ile U-Net decoder** kombinasyonu hızlı (27 MB model boyutu) ve iyi bir IOU skoru (0.828) sağlamıştır. Edge cihazlarda ya da hızlı çıkarım (inference) istenen senaryolarda bu MobileNet + U-Net yapısı kullanılabilir. Eğer işlem gücü kısıtı yoksa ve maksimum doğruluk (IoU ~0.87) isteniyorsa encoder olarak **DenseNet161** tercih edilebilir.

### Veri Seti Önerisi
- **Zindi LOC Sea Turtle Face Detection:** Yarışma veri seti. Özellikle yüz pullarının tespiti (face scale detection) için optimize edilmiştir.
- **SeaTurtles_Images (kim2429 repo):** iNaturalist ve Google Görseller'den toplanmış, bbox ve polygon formatında etiketlenmiş karma veri seti. Modelin açık deniz veya kumsaldaki farklı aydınlatma koşullarına karşı genelleme yapabilmesi için eğitim sürecinde augmentation ile birlikte kullanılmalıdır. Lisanslı ve açık verilerin derlenmesinden oluşur, kullanım öncesi ticari koşullar için kaynak lisanslarının kontrol edilmesi gerekir.

### Mimari Notları
1. **Model Başlatma (Fine-Tuning):** Sıfırdan eğitim yerine, ImageNet ile önceden eğitilmiş bir backbone kullanılmalıdır (Örn: ResNet18 veya MobileNet).
2. **Segmentation Yapısı:** Sadece yüzü bulmak yerine yüz hatlarını segmentation (maskeleme) ile çıkarmak, arka plandaki mercan/deniz tabanı gürültülerini filtrelediği için YOLO-seg ve U-Net gibi modellere odaklanılmalıdır.
3. **Değerlendirme Metriği:** Yüz tespiti/kırpma işlemi için Intersection over Union (IoU) metriği optimize edilmeli; tür sınıflandırması tarafında mAP veya F1-Score baz alınmalıdır.
