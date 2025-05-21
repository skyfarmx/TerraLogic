# Tarım Analiz

<div align="center">
  <h1>🌱 TARIM ANALİZ 🧠</h1>
  <h3>Yapay Zeka ve Derin Öğrenme Teknolojisi ile Bitki Koruma için Sürdürülebilir Çözüm</h3>
</div>

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Teknolojiler](#-teknolojiler)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

## 🌱 Proje Hakkında

**Terra Logic**, geleneksel bitki koruma yöntemlerine sürdürülebilir bir alternatif sunmak amacıyla geliştirilmiş, yapay zeka ve derin öğrenme teknolojilerini kullanan bir projedir. Tarımsal üretimde kullanılan kimyasal ilaçların miktarını azaltarak, çevre dostu ve ekonomik bir yaklaşım sunar.

Projemiz, drone ve uydu görüntülerini analiz ederek:
- Bitki hastalıklarını erken tespit eder
- Zararlı böcekleri tanımlar
- Hassas tarım uygulamalarını destekler
- İlaçlama optimizasyonu sağlar

Bu sayede çiftçilerin daha verimli, sürdürülebilir ve çevre dostu bir şekilde üretim yapmalarına olanak tanır.

## 🔧 Teknolojiler

Terra Logic, modern teknolojilerin bir araya gelmesiyle oluşturulmuştur:

### Yapay Zeka ve Görüntü İşleme
- **PyTorch**: Derin öğrenme modelleri için temel kütüphane
- **OpenCV**: Görüntü işleme ve analizi
- **Pillow**: Python görüntü işleme kütüphanesi
- **TensorBoard**: Model eğitim sürecinin görselleştirilmesi

### Geomekânsal Veri İşleme
- **OSGeo4W**: Geomekânsal araçlar paketi
- **Rasterio**: Raster coğrafi veriler için Python kütüphanesi
- **PyODM**: Drone görüntülerinden fotogrametri
- **PyProj**: Koordinat dönüşümleri

### Web Uygulaması
- **Django**: Web çerçevesi
- **PostgreSQL**: Veritabanı
- **Gunicorn**: WSGI HTTP Sunucusu

### Veri İşleme
- **Pandas**: Veri manipülasyonu ve analizi
- **NumPy**: Bilimsel hesaplama
- **SciPy**: Bilimsel ve teknik hesaplama

## ✨ Özellikler

### 1. Bitki Hastalığı Tespiti
- 50+ yaygın bitki hastalığını %93+ doğrulukla tespit etme
- Hastalık şiddetinin derecelendirilmesi
- Tedavi önerileri ve önleyici tedbirler

### 2. Zararlı Böcek Tanımlama
- 30+ zararlı böcek türünü gerçek zamanlı tanımlama
- Popülasyon yoğunluğu analizi
- Biyolojik mücadele yöntemleri önerileri

### 3. Hassas Tarım Desteği
- Bitki sağlığı haritalaması
- Verimlilik analizi
- Sulama optimizasyonu

### 4. İlaçlama Optimizasyonu
- Nokta atışı ilaçlama planları
- Kimyasal kullanımında %60'a varan tasarruf
- Ürün kalitesinde iyileştirme

### 5. Erken Uyarı Sistemi
- Hava durumu verilerine dayalı hastalık risk tahminleri
- SMS ve e-posta ile bildirimler
- Sezonluk tahmin raporları

## 🚀 Kurulum

### Önkoşullar
- Python 3.9+
- PostgreSQL
- OSGeo4W (Windows için)

### Adımlar

1. **Repoyu klonlayın**
   ```bash
   git clone https://github.com/kullaniciadi/tarimanaliz.git
   cd tarimanaliz
   ```

2. **Sanal ortam oluşturun**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **Veritabanı ayarlarını yapın**
   ```bash
   cp .env.example .env
   ```
   `.env` dosyasını düzenleyerek veritabanı bilgilerinizi girin.

5. **Veritabanı migrasyonlarını gerçekleştirin**
   ```bash
   python manage.py migrate
   ```

6. **Sunucuyu başlatın**
   ```bash
   python manage.py runserver
   ```

## 💻 Kullanım

### Web Arayüzü

Terra Logic web arayüzüne `http://localhost:8000` adresinden erişebilirsiniz. Kullanıcı dostu arayüz ile:

1. Drone veya uydu görüntülerini yükleyebilir
2. Analiz sonuçlarını görselleştirebilir
3. Raporlar oluşturabilir
4. İlaçlama planları hazırlayabilirsiniz

### API Kullanımı

Terra Logic API'si, diğer sistemlerle entegrasyon için RESTful bir arayüz sunar:

```python
import requests

# Görüntü analizi için örnek API çağrısı
url = "https://api.tarimanaliz.com/v1/analyze"
files = {"image": open("field_image.jpg", "rb")}
response = requests.post(url, files=files)

results = response.json()
print(results)
```

## 📚 API Dokümantasyonu

API dokümantasyonuna [https://docs.terralogic.ai](https://docs.tarimanaliz.com) adresinden erişebilir veya sunucu çalışırken `http://localhost:8000/api/docs/` adresini ziyaret edebilirsiniz.

### Temel Endpoints

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/api/v1/analyze` | POST | Görüntü analizi gerçekleştirir |
| `/api/v1/diseases` | GET | Tespit edilebilen hastalıkları listeler |
| `/api/v1/pests` | GET | Tanımlanabilen zararlıları listeler |
| `/api/v1/reports` | GET | Kullanıcı raporlarını getirir |
| `/api/v1/reports` | POST | Yeni rapor oluşturur |

## 👥 Katkıda Bulunma

Tarim Analiz'e katkıda bulunmak için:

1. Bu repoyu forklayın
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

Katkıda bulunmadan önce lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun.

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 📬 İletişim

Proje Yöneticileri: [Murad Aliyev](mailto:murad.aliyev@tarimanaliz.com) ve [Altug Tatlisu](mailto:altug.tatlisu@tarimanaliz.com)

Proje Sayfası: [https://www.terralogic.ai](https://www.tarimanaliz.com)

---

<div align="center">
  <p>Terra Logic &copy; 2025 - Sürdürülebilir Tarım için Yapay Zeka Çözümleri</p>
</div>
