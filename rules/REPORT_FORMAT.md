# Rapor Formatı — TurtleVision

Her ajan, görev süresince kendi rapor dosyasını tutar.
Bu dosyalar proje sonunda "süreç kanıtı" olarak kullanılır.

---

## Rapor Dosyaları

| Ajan | Dosya |
|------|-------|
| Orkestratör | `reports/orchestrator-log.md` |
| Araştırma | `reports/research-agent-log.md` |
| Araştırma (öneriler) | `reports/technology-recommendations.md` |
| Görüntü İşleme | `reports/image-processing-log.md` |
| Özellik Çıkarım | `reports/feature-extraction-log.md` |
| Sınıflandırma | `reports/classification-log.md` |
| Doğrulayıcı | `reports/validator-log.md` |

---

## Genel Kurallar

1. **Üzerine yazma** — her yeni giriş dosyanın altına eklenir, eskiler silinmez
2. **Zaman damgası** — her giriş `[YYYY-MM-DD HH:MM]` ile başlar
3. **Kısa ve öz** — paragraf yazma, madde listesi kullan
4. **Sayısal değer** — mümkün olan her yerde ölçüm ekle (süre, doğruluk, sayı)
5. **Hata da yaz** — başarısız denemeler de kayıt altına alınır

---

## Proje Sonu Özet Raporu

Tüm işler tamamlandığında Orkestratör, `reports/FINAL_REPORT.md` dosyasını oluşturur:

```markdown
# TurtleVision — Final Raporu

## Doğruluk Sonucu
- Test seti boyutu: N görüntü
- Doğru tahmin: N (%XX)
- Güven eşiği üstü tahminler: %XX
- Belirsiz (eşik altı): %XX

## SOLID Uyum Özeti
- Doğrulayıcı tarafından PASS verilen PR sayısı: N
- FAIL → düzeltme döngüsü sayısı: N
- Kalan SOLID iyileştirme önerileri: [liste]

## Ajan Performans Özeti
| Ajan | Başlatılma | Tamamlanma | FAIL sayısı |
|------|-----------|-----------|-------------|
| ...  | ...       | ...       | ...         |

## Kullanılan Teknolojiler (Araştırma Doğrulamalı)
[Araştırma Ajanı bulgularına dayanarak seçilen teknolojiler]

## Öğrenilen Dersler
[Her ajan için kısa not]
```
