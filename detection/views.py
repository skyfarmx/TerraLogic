from django.shortcuts import render
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import time
import os
from datetime import date
from django.http import FileResponse
from dron_map.models import Users
from yolowebapp2 import predict_tree, hashing  # ,tasknode,options

TEMEL_DIZIN = Path(__file__).resolve().parent.parent

def dosya_turunu_dogrula(dosya):
    """
    Yüklenen dosyanın geçerli bir resim dosyası olup olmadığını kontrol et.
    
    Parametreler:
    - dosya: Yüklenen dosya nesnesi
    
    Dönüş:
    - Boolean: Dosya türü geçerli ise True, değilse False
    """
    gecerli_uzantilar = ['.jpg', '.jpeg', '.png']
    uzanti = os.path.splitext(dosya.name)[1]
    return uzanti.lower() in gecerli_uzantilar

def kullanici_olustur_veya_al(kullanici):
    """
    Mevcut kullanıcıyı al veya yeni bir kullanıcı oluştur.
    
    Parametreler:
    - kullanici: Mevcut kullanıcı nesnesi
    
    Dönüş:
    - Users: Kullanıcı nesnesi
    """
    try:
        kullanici_profili = Users.objects.get(kat_id=kullanici)
    except Users.DoesNotExist:
        # Gerekli alanlarla yeni bir Users kaydı oluştur
        kullanici_profili = Users.objects.create(
            kat_id=kullanici,
            birthday=date(2000, 1, 1),  # Varsayılan doğum günü
            website='',  # Varsayılan boş website
            # Gerekirse buraya diğer zorunlu alanları ekle
        )
        kullanici_profili.save()
    return kullanici_profili

def index(request):
    """
    Tek resim yüklemelerini işleyip meyve tespiti yapar.
    
    Parametreler:
    - request: Meyve_grubu, agac_sayi, agac_yasi, ekilis_sira ve dosya içeren POST verisi
    
    Dönüş:
    - İşleme sonuçları veya form içeren şablon
    """
    if request.user.is_authenticated:
        print(str(TEMEL_DIZIN), "TEMEL_DIZIN")
        kullanici_profili = kullanici_olustur_veya_al(request.user)
        yanit = {}
        
        if request.method == 'POST':
            meyve_grubu = request.POST.get('meyve_qrupu')
            agac_sayi = request.POST.get('agac_sayi')
            agac_yasi = request.POST.get('agac_yasi')
            ekilis_sira = request.POST.get('ekilis_sira')
            dosya = request.FILES.get('file')
            
            if all([meyve_grubu, agac_sayi, agac_yasi, ekilis_sira, dosya]):
                if not dosya_turunu_dogrula(dosya):
                    yanit['hata'] = "Geçersiz dosya türü. Lütfen JPG veya PNG resim yükleyin."
                    return render(request, "main.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})
                
                # Windows için sabit yol
                statik_resimler_yolu = os.path.join(TEMEL_DIZIN, "static", "images")
                dosya_sistemi = FileSystemStorage(location=statik_resimler_yolu)
                kaydedilen_dosya_adi = dosya_sistemi.save(dosya.name, dosya)
                baslangic_zamani = time.time()
                
                # Sabit yol - kaydedilen_dosya_adi kullan
                tam_resim_yolu = os.path.join(statik_resimler_yolu, kaydedilen_dosya_adi)
                
                try:
                    if meyve_grubu == "mandalina":
                        if 0 < int(agac_yasi) <= 4:
                            tespit = predict_tree.preddict(path_to_weights="mandalina.pt", path_to_source=tam_resim_yolu)
                            yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.125
                            yanit['adet'] = tespit[-3:-1].decode("utf-8")
                            yanit['toplam_agirlik'] = int(agac_sayi)*yanit['kilo']
                        elif 4 < int(agac_yasi) <= 8:
                            pass
                        elif 8 < int(agac_yasi) <= 30:
                            pass

                    elif meyve_grubu == "elma":
                        tespit = predict_tree.preddict(path_to_weights="elma.pt", path_to_source=tam_resim_yolu)
                        yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.105
                        yanit['adet'] = tespit[-3:-1].decode("utf-8")
                        yanit['toplam_agirlik'] = int(agac_sayi)*yanit['kilo']

                    elif meyve_grubu == "armut":
                        tespit = predict_tree.preddict(path_to_weights="armut.pt", path_to_source=tam_resim_yolu)
                        yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.220
                        yanit['adet'] = tespit[-3:-1].decode("utf-8")
                        yanit['toplam_agirlik'] = int(agac_sayi)*yanit['kilo']

                    elif meyve_grubu == "seftali":
                        tespit = predict_tree.preddict(path_to_weights="seftali.pt", path_to_source=tam_resim_yolu)
                        yanit['adet'] = tespit[-3:-1].decode("utf-8")
                        yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.185
                        yanit['toplam_agirlik'] = int(agac_sayi)*yanit['kilo']

                    elif meyve_grubu == "nar":
                        tespit = predict_tree.preddict(path_to_weights="nar.pt", path_to_source=tam_resim_yolu)
                        yanit['adet'] = tespit[-3:-1].decode("utf-8")
                        yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.300
                        yanit['toplam_agirlik'] = int(agac_sayi)*yanit['kilo']

                    elif meyve_grubu == "hurma":
                        tespit = predict_tree.preddict(path_to_weights="hurma.pt", path_to_source=tam_resim_yolu)
                        yanit['adet'] = tespit[-3:-1].decode("utf-8")
                        # yanit['kilo'] = int(tespit[-3:-1].decode("utf-8"))*0.125
                    
                    yanit['zaman'] = f"{(time.time()-baslangic_zamani):.2f}"
                    yanit['resim'] = f'images/{kaydedilen_dosya_adi}'
                    yanit['tespit_resmi'] = f'detected/{kaydedilen_dosya_adi}'  # kaydedilen_dosya_adi kullanmak için düzeltildi
                
                except Exception as e:
                    yanit['hata'] = f"Resim işlenirken hata oluştu: {str(e)}"
                
                return render(request, "main.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})
            else:
                return render(request, "main.html", {"kullanici_profili": kullanici_profili})
        else:
            return render(request, "main.html", {"kullanici_profili": kullanici_profili})
    else:
        return render(request, "login.html",)


def coklu_tespit_resim(request):
    """
    Çoklu resim yüklemelerini işleyip meyve tespiti yapar.
    
    Parametreler:
    - request: Meyve_grubu, ekilis_sira ve dosyalar içeren POST verisi
    
    Dönüş:
    - İşleme sonuçları veya form içeren şablon
    """
    if request.user.is_authenticated:
        print(str(TEMEL_DIZIN), "TEMEL_DIZIN")
        kullanici_profili = kullanici_olustur_veya_al(request.user)
        yanit = {}
        
        if request.method == 'POST':
            meyve_grubu = request.POST.get('meyve_qrupu')            
            ekilis_sira = request.POST.get('ekilis_sira')            
            dosyalar = request.FILES.getlist('file')
            print(dosyalar, "Dosya Adları")
            
            if not dosyalar:
                yanit['hata'] = "Lütfen en az bir resim dosyası yükleyin."
                return render(request, "multi_detection_fruit.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})
            
            # Tüm dosyaların geçerli resim dosyaları olduğunu kontrol et
            for dosya in dosyalar:
                if not dosya_turunu_dogrula(dosya):
                    yanit['hata'] = "Geçersiz dosya türü tespit edildi. Lütfen sadece JPG veya PNG resimler yükleyin."
                    return render(request, "multi_detection_fruit.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})
            
            baslangic_zamani = time.time()
            
            try:
                if meyve_grubu == "mandalina":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)         
                    
                    tespit = predict_tree.multi_predictor(path_to_weights="mandalina.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])

                elif meyve_grubu == "elma":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                    tespit = predict_tree.multi_predictor(path_to_weights="elma.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])

                elif meyve_grubu == "armut":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                    tespit = predict_tree.multi_predictor(path_to_weights="armut.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])

                elif meyve_grubu == "seftali":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                    tespit = predict_tree.multi_predictor(path_to_weights="seftali.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])

                elif meyve_grubu == "nar":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                    tespit = predict_tree.multi_predictor(path_to_weights="nar.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])

                elif meyve_grubu == "hurma":
                    hash_deger = hashing.add_prefix2(filename=f"{time.time()}") 
                    dosya_sistemi = FileSystemStorage(location=str(hash_deger[0])) 
                    for resim in dosyalar:                    
                        kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                    tespit = predict_tree.multi_predictor(path_to_weights="hurma.pt", path_to_source=hash_deger[0], ekilis_sira=ekilis_sira, hashing=hash_deger[1])
                else:
                    yanit['hata'] = "Geçersiz meyve grubu seçildi."
                    return render(request, "multi_detection_fruit.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})

                yanit['zaman'] = f"{(time.time()-baslangic_zamani):.2f}"
                return render(request, "multi_detection_fruit.html", {"yanit": hash_deger[1], "kullanici_profili": kullanici_profili})
            
            except Exception as e:
                yanit['hata'] = f"Resimler işlenirken hata oluştu: {str(e)}"
                return render(request, "multi_detection_fruit.html", {"yanit": yanit, "kullanici_profili": kullanici_profili})
        else:
            return render(request, "multi_detection_fruit.html", {"kullanici_profili": kullanici_profili})
    else:
        return render(request, "login.html",)


def resim_indir(request, slug):
    """
    İşlenen resim sonuçlarını zip dosyası olarak indir.
    
    Parametreler:
    - request: HTTP isteği
    - slug: İndirilecek dosya için tanımlayıcı
    
    Dönüş:
    - FileResponse: İndirilebilir zip dosyası
    """
    print(slug, "slug değeri")
    try:
        dosya_yolu = os.path.join(TEMEL_DIZIN, "media", f"{slug}_result.zip")
        return FileResponse(open(dosya_yolu, 'rb'), as_attachment=True)
    except FileNotFoundError:
        return render(request, "hata.html", {"hata": "İstenen dosya bulunamadı."})
    except Exception as e:
        return render(request, "hata.html", {"hata": f"Dosya indirilirken hata oluştu: {str(e)}"})
