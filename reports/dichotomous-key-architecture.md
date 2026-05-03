# Hiyerarşik Karar Ağacı (Dichotomous Key) Mimarisi

Sistem mimarisi, kaplumbağa türlerini (yaklaşık 314 tür) tek tek özellikleriyle değil, popülasyonu ikiye veya büyük gruplara bölecek **Makro Özelliklerden**, daha dar spesifik grupları ayrıştıran **Mikro Özelliklere** doğru eleyecek şekilde yeniden tasarlanmıştır. Bu yapı, bilgisayarlı görü (OpenCV) işlemlerinde performans artışı ve hata toleransı sağlar.

---

## Seviye 1: Gaga ve Çene Geometrisi (En Büyük Makro Ayrım)
Dünyadaki kaplumbağalar, beslenme alışkanlıklarına göre çene yapılarında net bir ikili (dichotomous) ayrım gösterir.

*   **1A: Belirgin Kancalı / Sivri Gaga (Hooked Beak)**
    *   *Kapsam:* Yırtıcı tatlı su kaplumbağaları (Chelydra, Macrochelys) ve mercan yiyici deniz kaplumbağaları (Eretmochelys).
    *   *OpenCV Ölçülebilirliği:* **Orta** (Profil dış konturunda Convexity Defect ve uç açısı hesaplaması. Keskin bir dar açı (acute angle) aranır.)
    *   *Ağaç Yönlendirmesi:* -> **Seviye 2A'ya git**

*   **1B: Küt, Pürüzsüz veya Çok Hafif Kavisli Gaga (Blunt Beak)**
    *   *Kapsam:* Otçul/Hepçil deniz kaplumbağaları (Chelonia), çoğu tatlı su ve kara kaplumbağası.
    *   *OpenCV Ölçülebilirliği:* **Orta** (Gaga ucundaki kavis (curvature) değişiminin az olması, geniş açı.)
    *   *Ağaç Yönlendirmesi:* -> **Seviye 2B'ye git**

---

## Seviye 2A: "Kancalı Gaga" Grubunu Ayrıştırma (Göz Konumu ve Doku)

*   **2A-1: Gözler Yanda, Kafa Pürüzsüz/Keratin Pullu**
    *   *Kapsam:* Genellikle açık su / deniz kaplumbağaları.
    *   *OpenCV Ölçülebilirliği:* **Kolay** (Göz merkezlerinin kafa Bounding Box'ı içindeki Y ekseni oranı).
    *   *Mikro Hedef:* **Eretmochelys imbricata** (Şahin Gagalı). Göz arası 2 çift pul *(Ölçüm: Zor)* ile teyit edilir.

*   **2A-2: Gözler Tepede, Kafa ve Boyun Siğilli/Çıkıntılı (Pusu Grubu)**
    *   *Kapsam:* Dipte yatan tatlı su avcıları.
    *   *OpenCV Ölçülebilirliği:* **Orta** (Boyun konturunda Canny Edge ile düzensiz tırtık analizi ve göz merkezi Y koordinatı yüksekliği).
    *   *Mikro Özellik:* Boyunda basit tüberküller -> **Chelydra serpentina**
    *   *Mikro Özellik:* Devasa kafa, göz etrafı yıldız çıkıntılar -> **Macrochelys suwanniensis** *(Ölçüm: Zor)*.

---

## Seviye 2B: "Küt Gaga" Grubunu Ayrıştırma (Renk, Desen ve Oran)

*   **2B-1: Kafa Üzerinde Belirgin ve Uzun Renk Çizgileri/Bantları Var**
    *   *Kapsam:* Tatlı su kaplumbağalarının büyük bir kısmı (Trachemys, Chrysemys, Pseudemys).
    *   *OpenCV Ölçülebilirliği:* **Kolay** (HSV renk maskelemesi (Kırmızı/Sarı) ve Blob algılama ile ardışık uzun lekelerin tespiti).
    *   *Mikro Özellik:* Göz arkasında kalın kırmızı/turuncu yama -> **Trachemys scripta elegans**
    *   *Mikro Özellik:* Boyunda paralel ince sarı çizgiler -> **Chrysemys picta** veya diğer Trachemys alt türleri *(Ölçüm: Orta - Hough Lines)*.

*   **2B-2: Belirgin Şerit YOK (Homojen Yüzey, Benek veya Keratin Pullar)**
    *   *Kapsam:* Deniz kaplumbağaları, Kutu kaplumbağaları.
    *   *Ağaç Yönlendirmesi:* -> **Seviye 3'e git**

---

## Seviye 3: Detaylı Yüzey ve Oran Ayrışımı (Mikro / Alt-Makro Gruplar)

*   **3A: Baş Boyutu Gövdeye Göre Orantısız Büyük (Massive Head)**
    *   *Kapsam:* Kabuk kırmak için evrimleşmiş çene kaslarına sahip türler.
    *   *OpenCV Ölçülebilirliği:* **Kolay** (Yüz alanının (ROI) veya çene genişliğinin gözler arası mesafeye oranı hesabı).
    *   *Hedef Tür:* **Caretta caretta** (İribaş Deniz Kaplumbağası).

*   **3B: Başta Keratin Pullar (Scales) Var, Klasik Oranlı**
    *   *Kapsam:* Otçul/Hepçil klasik deniz kaplumbağaları.
    *   *OpenCV Ölçülebilirliği:* **Zor** (Canny/Watershed ile kapalı alan kontur sayımı. Işık/yansıma hataya açıktır).
    *   *Mikro Özellik:* Göz arası sadece 1 çift (2 adet) uzun pul -> **Chelonia mydas** veya **Natator depressus**.

*   **3C: Başta Sadece Leke/Benek (Mottling) Var, Göz İrisi Renkli**
    *   *Kapsam:* Kara ve kutu kaplumbağaları.
    *   *OpenCV Ölçülebilirliği:* **Kolay** (HSV "Sarı" filtresi ile dağınık leke sayımı).
    *   *Mikro Özellik:* Parlak kırmızı iris (erkeklerde) ve sarı/yeşil kafada dağınık benekler -> **Terrapene ornata ssp. Luteola**. *(İris ölçümü: Orta)*

*   **3D: Baş Tamamen Pürüzsüz Deri (Pul Yok), Siyah Üzeri Beyaz Benekler**
    *   *Kapsam:* Deri sırtlılar.
    *   *OpenCV Ölçülebilirliği:* **Kolay** (Düşük doku varyansı (variance of Laplacian) ve siyah maskede beyaz Blob tespiti).
    *   *Mikro Özellik:* Üst çenede belirgin "W" şeklinde çentik -> **Dermochelys coriacea**. *(W çentik ölçümü: Orta)*.
