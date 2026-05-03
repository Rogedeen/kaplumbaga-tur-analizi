# Hybrid Neuro-Symbolic Mimari: OpenCV ile Ölçülebilir Fiziksel Kurallar

Bu belge, derin öğrenme (Deep Learning) tespiti ile kural tabanlı (Symbolic) klasik bilgisayarlı görü yaklaşımlarını harmanlamak için ilk 5 hedef türün OpenCV ile ölçülebilirlik analizlerini içerir.

### 1. Chelydra serpentina (Bayağı Kapan Kaplumbağa)
- **Kural 1: Boyun Tüberkülleri (Çıkıntılar)**
  - **Fiziksel Özellik:** Çene altında ve boyun çevresinde siğil/diken benzeri pürüzlü etli çıkıntılar.
  - **OpenCV Ölçülebilirliği:** Boyun ROI'si (Region of Interest) üzerinde Kontur Analizi (Contour Analysis). Pürüzsüz boyunlu türlerin aksine, dış hat konturunda çok sayıda tepe-çukur (convexity defect) bulunacaktır.
  - **Güçlük Seviyesi:** **Orta** (Arka plandan ayırmak için iyi kontrast gerekir).
- **Kural 2: Üstte Konumlanmış Gözler**
  - **Fiziksel Özellik:** Gözlerin kafanın yanından çok tepeye doğru (yukarı ve öne bakar) konumlanması.
  - **OpenCV Ölçülebilirliği:** Göz tespiti (Haar/DL) yapıldıktan sonra, göz merkezlerinin Y-ekseni koordinatının kafa bounding box'ının üst %20'lik diliminde yer alması.
  - **Güçlük Seviyesi:** **Kolay / Orta**

### 2. Terrapene ornata ssp. Luteola (Çöl Kutu Kaplumbağası)
- **Kural 1: Kırmızı/Turuncu İris (Genellikle Erkekler)**
  - **Fiziksel Özellik:** İrisin çok canlı kırmızı veya turuncu renkte olması.
  - **OpenCV Ölçülebilirliği:** Göz ROI'si bulunduktan sonra HSV renk uzayında kırmızı/turuncu (Red/Orange) maskeleme yapılarak piksel yoğunluğunun ölçülmesi.
  - **Güçlük Seviyesi:** **Orta** (Göz bebeğinin küçüklüğü ve ışık yansıması (glare) analizi zorlaştırabilir).
- **Kural 2: Kafa Üzerinde Sarı Benekler**
  - **Fiziksel Özellik:** Gri/yeşil-kahve zemin üzerinde kafa ve yanaklarda dağınık sarı benekler (mottling).
  - **OpenCV Ölçülebilirliği:** Kafa ROI'sinde HSV "Sarı" (Yellow) maskelemesi uygulanıp Blob Detection (Leke Tespiti) ile sarı alanların alan/sayı hesabının yapılması.
  - **Güçlük Seviyesi:** **Kolay**

### 3. Trachemys scripta (Kızıl Yanaklı Su Kaplumbağası vd.)
- **Kural 1: Göz Arkası Renkli Şerit**
  - **Fiziksel Özellik:** Gözün arkasından boyuna doğru yatay uzanan çok belirgin kırmızı, turuncu veya sarı kalın şerit.
  - **OpenCV Ölçülebilirliği:** Göz merkezinin X koordinatının ardında kalan alan ROI olarak belirlenir. HSV renk filtresi ile kalın, eliptik konturun (Blob) aranması.
  - **Güçlük Seviyesi:** **Kolay** (Renklerin zıtlığı nedeniyle klasik görüntü işlemenin en iyi sonuç vereceği özelliktir).
- **Kural 2: Yüzde Yatay Sarı Çizgiler**
  - **Fiziksel Özellik:** Koyu zemin üzerine ağız, çene ve yanak etrafında birbirine paralel ince sarı çizgiler.
  - **OpenCV Ölçülebilirliği:** Sarı renk maskesi üzerinden Canny kenar tespiti veya Hough Line Transform (Hough Çizgi Dönüşümü) uygulanarak paralel çizgilerin bulunması.
  - **Güçlük Seviyesi:** **Orta**

### 4. Macrochelys suwanniensis (Suwannee Timsah Kapan Kaplumbağası)
- **Kural 1: Aşırı Kıvrık Şahin Gagası**
  - **Fiziksel Özellik:** Üst çeneden aşağıya doğru kanca gibi çok keskin ve belirgin sarkan gaga.
  - **OpenCV Ölçülebilirliği:** Yüz profilinin uç noktası bulunup, dış kontur (Convex Hull) çıkarılır. Gaganın ucundaki eğim (kavis açısı) açı hesaplama fonksiyonlarıyla ölçülür. Çok dar bir açı keskin gagayı ifade eder.
  - **Güçlük Seviyesi:** **Orta** (Sadece profilden çekilmiş (yandan) fotoğraflarda sağlıklı ölçülebilir).
- **Kural 2: Göz Çevresi "Kirpik" Çıkıntıları**
  - **Fiziksel Özellik:** Gözlerin hemen etrafında yıldız biçiminde, etli ve dikenli dokular.
  - **OpenCV Ölçülebilirliği:** Göz çevresine dairesel maske uygulanıp, yüksek frekanslı doku analizi (Corner/Harris detection) yapılması.
  - **Güçlük Seviyesi:** **Zor** (Bulanık görüntülerde, çamurda veya düşük çözünürlükte tamamen gürültü (noise) olarak algılanıp kaybolacaktır).

### 5. Chelonia mydas (Yeşil Deniz Kaplumbağası)
- **Kural 1: Çift Prefrontal Pul**
  - **Fiziksel Özellik:** Gözlerin arasında sadece 1 çift (toplam 2 adet) belirgin ve uzun prefrontal pul olması (diğer çoğu deniz kaplumbağasında 2 çift vardır).
  - **OpenCV Ölçülebilirliği:** Gözler arası bölgede Canny ve Watershed bölütleme algoritmaları kullanılarak kapalı poligonların (konturların) sayılması.
  - **Güçlük Seviyesi:** **Zor** (Su altı yansımaları, pulların birleşim çizgilerinin (seam) silik olması ve açının tam üstten olmaması durumu sayımı imkansız kılabilir).
- **Kural 2: Küt Gaga**
  - **Fiziksel Özellik:** Çene ucunda kanca olmaması, küt ve hafif testere dişli kenar yapısı.
  - **OpenCV Ölçülebilirliği:** Çene ucu kontur kavis (curvature) analizi. Kavis değişiminin az olması.
  - **Güçlük Seviyesi:** **Orta**
