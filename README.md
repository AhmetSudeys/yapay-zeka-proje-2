# yapay-zeka-proje-2
Bu repoda yer alan dosyalar, Yapay Zeka Sistemleri dersi kapsamında hazırlanan 2. proje ödevini içermektedir.


Projede amaç, Isparta il merkezinde belirlenen afet ve acil durum toplanma alanları arasında bir acil durum nakliye dronu için en uygun (toplam mesafesi en kısa) rotayı bulmaktır.

Bu repoda hem uygulama (Streamlit) sürümü hem de sunum/savunma için hazırlanan notebook sürümü birlikte yer almaktadır.

---

# Odev2 – Karınca Kolonisi Algoritması ile Yol Optimizasyonu (Senaryo 8)

Bu repoda iki farklı format birlikte sunulmuştur:

- `main.py` ve modüler `.py` dosyaları: Streamlit arayüzü üzerinden etkileşimli şekilde çalıştırılabilen uygulama sürümü.
- `Odev2.ipynb`: Jupyter Notebook sürümü. Problem tanımı, yöntem, ara çıktılar, yakınsama grafiği ve (isteğe bağlı) harita görselleştirme akışı notebook üzerinde adım adım incelenebilir.

Değerlendirme sürecinde özellikle notebook dosyasının akışı, açıklayıcılığı ve projeye hakimiyet düzeyi inceleneceği için `Odev2.ipynb` dosyası projenin ana teslim formatıdır.

---

## 1. Problem Tanımı (Senaryo 8)

Bir acil durum nakliye dronu, Isparta merkezde bulunan afet ve acil durum toplanma alanlarına paket taşımakla görevlidir. Dronun izleyeceği rotanın toplam mesafesi, görev süresini ve operasyon verimliliğini doğrudan etkiler.

Bu projede hedef:

- Belirlenen tüm toplanma alanlarını kapsayan
- Bir başlangıç noktasından çıkıp tüm noktaları birer kez ziyaret eden
- Başlangıç noktasına geri dönen
- Toplam yol mesafesi minimum olan

en uygun rotayı bulmaktır.

Bu problem yapısı itibarıyla Gezgin Satıcı Problemi (TSP) benzeri bir optimizasyon problemidir.

---

## 2. Neden Gerçek Yol Mesafesi (Google Maps) Kullanıldı?

Kuş uçuşu (Öklidyen) mesafe, gerçek şehir içi yol koşullarını temsil etmez. Yol ağları, tek yönler, dönüşler ve sokak geometrisi nedeniyle gerçek sürüş mesafeleri farklılık gösterebilir.

Bu nedenle projede mesafeler:

- Google Maps API üzerinden
- driving (sürüş) modu seçilerek

alınmış ve noktalar arası mesafelerden bir mesafe matrisi oluşturulmuştur. Böylece optimizasyon, daha gerçekçi bir veri üzerinde gerçekleştirilmiştir.

---

## 3. Neden Karınca Kolonisi Algoritması (ACO)?

Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO), özellikle TSP benzeri yol optimizasyon problemlerinde sık kullanılan sezgisel bir yöntemdir.

Temel fikir:

- Her karınca olası bir tur (rota) üretir.
- İyi (kısa) turlar feromon ile ödüllendirilir.
- Zamanla feromon buharlaşır ve algoritma erken yakınsamaya kilitlenmeden farklı rotaları keşfetmeye devam eder.
- Olasılıksal seçim mekanizması sayesinde iyi çözümler daha sık tercih edilirken çeşitlilik de korunur.

Bu projede ACO ile hedef, toplam yol mesafesini minimize eden rotayı bulmaktır.

---

## 4. Kullanılan Noktalar (Toplanma Alanları)

Projede Isparta il merkezinden seçilen 10 adet toplanma alanı kullanılmıştır ve koordinatlar e-devlet üzerinden alınmıştır.

- Noktalar gerçek koordinatlar (enlem, boylam) ile temsil edilmiştir.
- Uygulama içinde her nokta hem indeks hem isim ile gösterilir.
- Nokta verileri `data/coordinates.py` dosyasında tutulur.

---

## 5. Proje Klasör Yapısı ve Neden Bu Şekilde Tasarlandı?

Proje, okunabilirliği artırmak ve her bileşeni ayrı sorumluluk alanına taşımak için modüler bir yapıda geliştirilmiştir.

Repo yapısı:
├── main.py

├── config.py

├── requirements.txt

├── Odev2.ipynb

├── README.md

│
├── data/

│ └── coordinates.py

│
├── core/

│ ├── google_maps.py

│ └── aco_algorithm.py

│
└── visual/

├── plotting.py

└── mapping.py


Açıklamalar:

- `main.py`
  Streamlit uygulamasının çalıştığı ana dosyadır. Arayüz, parametre girişleri, buton tetiklemeleri ve sonuçların gösterimi burada yönetilir.

- `config.py`
  Varsayılan ACO parametreleri (alfa, beta, buharlaşma, karınca sayısı, iterasyon sayısı vb.) burada tutulur. Böylece ayarlar tek noktadan yönetilebilir.

- `requirements.txt`
  Projeyi çalıştırmak için gerekli kütüphaneleri listeler. Kurulum ve yeniden çalıştırılabilirlik açısından zorunludur.

- `data/coordinates.py`
  Toplanma alanlarının koordinatları ve isimleri burada tutulur. Veri katmanı ayrı tutulduğu için değişiklik yapmak kolaydır.

- `core/google_maps.py`
  Google Maps API ile mesafe matrisi oluşturma işlemleri burada yapılır. API çağrıları ve yanıtların matrise dönüştürülmesi bu modüldedir.

- `core/aco_algorithm.py`
  ACO algoritmasının çekirdek kısmıdır. Karıncaların rota üretimi, olasılık hesabı, feromon güncelleme ve yakınsama tarihçesi burada yürütülür.

- `visual/plotting.py`
  Yakınsama grafiği gibi görsel çıktılar bu dosyada üretilir.

- `visual/mapping.py`
  Harita üzerinde rota çizimi (pydeck katmanları) bu dosyada hazırlanır. Harita ve çizgi rengi/kalınlığı gibi görsel özellikler burada yönetilir.

Bu yapı, sunumda kodun parçalarını ayrı ayrı anlatmayı kolaylaştırır ve “hangi kod ne iş yapıyor” sorusuna net cevap verilmesini sağlar.

---

## 6. Streamlit Arayüzünde Çalışma Akışı

Uygulama çalıştırıldığında kullanıcı:

- Nokta listesini görür
- ACO parametrelerini (karınca sayısı, iterasyon, alfa, beta, buharlaşma) girer
- Mesafe tipi (driving / walking) seçebilir
- Başlangıç noktası indeksini belirleyebilir
- “Rota Hesapla” butonu ile algoritmayı başlatır

Sonuç olarak:

- En iyi rota (index) gösterilir
- En iyi rota (index - isim) gösterilir
- Toplam mesafe kilometre cinsinden yazdırılır
- Yakınsama grafiği oluşturulur
- Harita üzerinde rota çizilir

---

## 7. Güvenlik ve Gizlilik (API Key Yönetimi)

Google Maps API anahtarı repoya kesinlikle yazılmamalıdır.

Bu projede anahtar:

- `.streamlit/secrets.toml` veya `.env` dosyasında saklanır
- `.gitignore` ile repoya dahil edilmesi engellenir

Bu sayede anahtar repo içinde paylaşılmaz ve yetkisiz kullanım riski azaltılır.

Not: Notebook (`Odev2.ipynb`) tarafında harita çıktısı üretilirse bazı görselleştirmeler HTML çıktısına API key gömebilir. Bu nedenle notebook dosyası repoya yüklenmeden önce çıktılar temizlenmiş (Restart & Clear Output) şekilde paylaşılmalıdır.

---

## 8. Kurulum ve Çalıştırma

### 8.1 Kütüphanelerin kurulumu

Proje klasöründe terminal açarak:
pip install -r requirements.txt


### 8.2 Streamlit ile çalıştırma

Proje kök dizininde:
python -m streamlit run main.py

Tarayıcıda uygulama açıldıktan sonra parametreleri girip hesaplama başlatılabilir.

---

## 9. Notebook (Odev2.ipynb) Kullanımı

`Odev2.ipynb` dosyası:

- Problem tanımını
- Mesafe matrisi elde etme adımlarını
- ACO algoritmasının temel mantığını
- Yakınsama grafiğini
- Sonuçların yorumunu

tek bir akış halinde sunar.

Sunum esnasında anlatım için öncelikli dosya olarak hazırlanmıştır.

---

## 10. Sonuç

Bu projede, Isparta merkezde belirlenen toplanma alanları için Google Maps üzerinden gerçek sürüş mesafeleri kullanılarak bir mesafe matrisi oluşturulmuş ve Karınca Kolonisi Algoritması ile toplam mesafesi minimum olan rota başarıyla bulunmuştur. Modüler kod yapısı, Streamlit arayüzü ve notebook akışı ile proje hem çalışır hem de sunumda açıklanabilir bir formatta tamamlanmıştır.






