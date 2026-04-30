# TurtleVision

Kaplumbağa yüzünden tür tanıma — çoklu ajan sistemi ile.

## Proje Hakkında

TurtleVision, kaplumbağa fotoğraflarından yüz bölgesini tespit edip pul desenlerini analiz ederek tür sınıflandırması yapan bir derin öğrenme sistemidir. Proje, Google Antigravity IDE üzerinde paralel çalışan çoklu ajan mimarisine dayanır.

## Ajan Yapısı

```
agents/
  ORCHESTRATOR_AGENT.md      — İş koordinasyonu, GitHub yönetimi
  RESEARCH_AGENT.md          — Literatür tarama, teknoloji önerileri
  IMAGE_PROCESSING_AGENT.md  — Yüz tespiti, görüntü ön işleme
  FEATURE_EXTRACTION_AGENT.md — Embedding çıkarımı
  CLASSIFICATION_AGENT.md    — Tür tahmini, güven skoru
  VALIDATOR_AGENT.md         — SOLID denetimi, PR onayı
```

## Kurallar

```
rules/
  SOLID_PRINCIPLES.md   — Kod mimarisi kuralları
  CLEAN_CODE_RULES.md   — İsimlendirme, yapı, yorum kuralları
  REPORT_FORMAT.md      — Ajan rapor formatları
```

## Raporlar

```
reports/
  orchestrator-log.md
  research-agent-log.md
  technology-recommendations.md
  image-processing-log.md
  feature-extraction-log.md
  classification-log.md
  validator-log.md
  FINAL_REPORT.md         — Proje sonu özet (otomatik üretilir)
```

## MCP Server Bağlantıları

| MCP | Amaç | Kurulum |
|-----|------|---------|
| GitHub MCP | Repo tarama, branch, PR | PAT token ile |
| Fetch MCP | arXiv, PubMed, biorXiv | URL listesi ile |
| Filesystem MCP | Rapor dosyaları | Proje dizini ile sınırlı |

## Başlangıç Sırası

1. Antigravity'de MCP server'ları bağla
2. Araştırma Ajanını başlat (`agents/RESEARCH_AGENT.md` brief'i ile)
3. Araştırma tamamlanınca Orkestratörü başlat
4. Orkestratör paralel olarak Görüntü İşleme + Özellik Çıkarım ajanlarını başlatır
5. Doğrulayıcı her PR'ı denetler

## Prensipler

- **SOLID** — Her sınıf, her interface, her bağımlılık
- **Clean Code** — İsimlendirme, fonksiyon boyutu, tip güvenliği
- **Test Coverage** — Minimum %80
- **İzlenebilirlik** — Her tahmin kaynağına kadar takip edilebilir
