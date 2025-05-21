from django.shortcuts import render
from pathlib import Path
from yolowebapp2 import histogram as hs
import os, json, subprocess
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .forms import Projects_Form  # UserForm, UsersForm,
from .models import Users, Projects
from django.shortcuts import get_object_or_404
from yolowebapp2 import predict_tree, hashing, tasknode, options
TEMEL_DIZIN = Path(__file__).resolve().parent.parent
from asgiref.sync import sync_to_async
import asyncio
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def projeler(request):
    """
    Kullanıcıya ait projeleri listeler.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - İşleme sonuçları içeren şablon
    """
    if request.user.is_authenticated:
        try:
            kullanici_profili = Users.objects.get(kat_id=request.user.id)
            projeler_listesi = Projects.objects.filter(kat_user__kat_id=request.user.id)
            print(projeler_listesi)
            return render(request, "projects.html", {"kullanici_profili": kullanici_profili, "projeler_listesi": projeler_listesi})
        except Users.DoesNotExist:
            return render(request, "error.html", {"hata": "Kullanıcı profili bulunamadı"})
    else:
        return render(request, "login.html")


def proje_ekle(request, slug=None, id=None):
    """
    Proje ekleme, güncelleme veya silme işlemlerini yönetir.
    
    Parametreler:
    - request: HTTP isteği
    - slug: İşlem türü (add, update, delete)
    - id: İşlem yapılacak proje ID'si
    
    Dönüş:
    - İşleme sonuçları içeren şablon
    """
    if request.user.is_authenticated:
        try:
            kullanici_profili = get_object_or_404(Users, kat_id=request.user.id)

            if slug == "update" and id is not None:
                proje = Projects.objects.get(id=id)
                if request.method == 'POST':
                    form = Projects_Form(request.POST or None,
                                        request.FILES or None, instance=proje)
                    print(form.is_valid(), form.errors)
                    if form.is_valid():
                        form.picture = form.cleaned_data['picture']
                        print(request.FILES)
                        form.save()
                    return render(request, "add-projects.html", {'kullanici_profili': kullanici_profili, "proje": proje})
                else:
                    return render(request, "add-projects.html", {'kullanici_profili': kullanici_profili, "proje": proje})

            elif slug == "delete" and id is not None:
                proje = Projects.objects.get(id=id).delete()
                return redirect("dron_map:projeler")

            elif slug == "add" and id is None:
                if request.method == 'POST':
                    form = Projects_Form(request.POST or None, request.FILES or None)
                    baslik = request.POST.get('Title')
                    alan = request.POST.get('Field')
                    print(form.is_valid(), form.errors, form)
                    
                    if form.is_valid():
                        try:
                            hash_deger = hashing.add_prefix(filename=f"{baslik}{alan}")
                            print(hash_deger)
                            resim_listesi = request.FILES.getlist('picture')
                            form.picture = form.cleaned_data['picture']
                            form.instance.hashing_path = f"{hash_deger[1]}"
                            form.save()
                            
                            for resim in resim_listesi:
                                dosya_sistemi = FileSystemStorage(location=str(hash_deger[0]))
                                kaydedilen_dosya_adi = dosya_sistemi.save(resim.name, resim)
                                
                            p = tasknode.Node_processing(f"{hash_deger[0]}")
                            p.download_task(f"{TEMEL_DIZIN}/static/results/{hash_deger[1]}")
                            print(p.get_uuid(), p.get_tasks(p.get_uuid()))
                        except Exception as e:
                            return render(request, "add-projects.html", {
                                'kullanici_profili': kullanici_profili,
                                'hata': f"Proje eklenirken hata oluştu: {str(e)}"
                            })
                            
                    return render(request, "add-projects.html", {'kullanici_profili': kullanici_profili})
                else:
                    return render(request, "add-projects.html", {'kullanici_profili': kullanici_profili})
        except Exception as e:
            return render(request, "error.html", {"hata": f"İşlem sırasında hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")


def gorev_yolu(id, path, file):
    """
    Göreve ait dosya yolunu döndürür.
    
    Parametreler:
    - id: Proje kimliği
    - path: Alt dizin yolu
    - file: Dosya adı
    
    Dönüş:
    - String: Dosya yolu
    """
    return f'results/{id}/{path}/{file}'


def tam_gorev_yolu_al(id, path, file):
    """
    Göreve ait tam dosya yolunu döndürür.
    
    Parametreler:
    - id: Proje kimliği
    - path: Alt dizin yolu
    - file: Dosya adı
    
    Dönüş:
    - String: Tam dosya yolu
    """
    return os.path.join(TEMEL_DIZIN, f'static/results/{id}/{path}', file)


def istatistik_al(id, tur):
    """
    Proje istatistiklerini ve görüntü verilerini döndürür.
    
    Parametreler:
    - id: Proje hash kimliği
    - tur: İstenilen veri türü
    
    Dönüş:
    - Dict: İstatistik verileri
    """
    if tur == "static":
        gorev = tam_gorev_yolu_al(id, "odm_report", "stats.json")
        print("gorev", gorev)
        if os.path.isfile(gorev):
            try:
                with open(gorev) as f:
                    j = json.loads(f.read())
            except Exception as e:
                return str(e)
            return {
                'gsd': j.get('odm_processing_statistics', {}).get('average_gsd'),
                'alan': j.get('processing_statistics', {}).get('area'),
                'tarih': j.get('processing_statistics', {}).get('date'),
                'bitis_tarihi': j.get('processing_statistics', {}).get('end_date'),
            }
        else:
            return {}

    elif tur == "orthophoto" or tur == "plant":
        gorev = gorev_yolu(id, "odm_orthophoto", "odm_orthophoto.tif")
        return {"odm_orthophoto": gorev}

    elif tur == "dsm":
        gorev = gorev_yolu(id, "odm_dem", "dsm.tif")
        return {"dsm": gorev}

    elif tur == "dtm":
        gorev = gorev_yolu(id, "odm_dem", "dtm.tif")
        return {"dtm": gorev}

    elif tur == "camera_shots":
        gorev = gorev_yolu(id, "odm_report", "shots.geojson")
        if os.path.isfile(gorev):
            try:
                with open(gorev) as f:
                    j = json.loads(f.read())
            except Exception as e:
                return str(e)
            return {"camera_shots": j}
        else:
            return {}

    elif tur == "images_info":
        gorev = tam_gorev_yolu_al(id, '/', 'images.json')
        print(gorev, "images_info")
        if os.path.exists(gorev):
            try:
                with open(gorev) as f:
                    j = json.loads(f.read())
            except Exception as e:
                return str(e)
            return {
                'kamera_model': j[0].get('camera_model'),
                'yukseklik': j[0].get('altitude'),
            }
        else:
            return {}


def donustur(giris_yolu, cikis_yolu):
    """
    Görüntülerin coğrafi referanslarını bir dosyadan diğerine aktarır.
    
    Parametreler:
    - giris_yolu: Kaynak dosya yolu
    - cikis_yolu: Hedef dosya yolu
    """
    try:
        from osgeo import gdal
        dataset1 = gdal.Open(giris_yolu)
        projection = dataset1.GetProjection()
        geotransform = dataset1.GetGeoTransform()

        dataset2 = gdal.Open(cikis_yolu, gdal.GA_Update)
        dataset2.SetGeoTransform(geotransform)
        dataset2.SetProjection(projection)
        dataset2.GetRasterBand(1).SetNoDataValue(0)
    except Exception as e:
        print(f"Dönüştürme hatası: {str(e)}")


def haritalama(request, id):
    """
    Drone görüntülerini farklı vejetasyon indeksleriyle işleme ve haritalama.
    
    Parametreler:
    - request: HTTP isteği
    - id: Proje ID'si
    
    Dönüş:
    - İşleme sonuçları içeren harita şablonu
    """
    if request.user.is_authenticated:
        try:
            kullanici_profili = Users.objects.get(kat_id=request.user.id)
            proje = Projects.objects.get(id=id)
            algoritmalar = options.algorithm
            renkler = options.colormaps
            
            if request.method == 'POST':
                try:
                    orthophoto = istatistik_al(id=proje.hashing_path, tur="orthophoto")
                    statik = istatistik_al(id=proje.hashing_path, tur="static")
                    resim_bilgileri = istatistik_al(id=proje.hashing_path, tur="images_info")
                    post_aralik = tuple(map(float, request.POST.getlist('range')))
                    post_aralik = (-abs(post_aralik[0]), abs(post_aralik[1]))
                    saglik_renk = request.POST.get('health_color')
                    renk_haritasi = request.POST.get('cmap')

                    secilen_algoritma = algoritmalar[saglik_renk]
                    secilen_renk_haritasi = renkler[renk_haritasi]

                    if saglik_renk == "detect":
                        resim_yolu = os.path.split(f'{TEMEL_DIZIN}/static/{proje.picture}')[-1]
                        resim_yolu2 = f'detected/{resim_yolu}'
                        tespit = predict_tree.preddict(
                            path_to_weights="agac.pt",
                            path_to_source=f'{TEMEL_DIZIN}/static/{orthophoto["odm_orthophoto"]}'
                        )
                        donustur(
                            f'{TEMEL_DIZIN}/static/{orthophoto["odm_orthophoto"]}',
                            f'{TEMEL_DIZIN}/static/detected/odm_orthophoto.tif'
                        )
                        return render(request, "map.html", {
                            "kullanici_profili": kullanici_profili,
                            "orthophoto": {
                                'path': f"detected/odm_orthophoto.tif",
                                'colormap': renk_haritasi,
                                'ranges': post_aralik,
                            },
                            "algoritmalar": algoritmalar,
                            "renkler": renkler,
                            "statik": statik,
                            "resim_bilgileri": resim_bilgileri,
                            "tespit": tespit[-5:-1].decode("utf-8")
                        })
                    else:
                        # Vejetasyon indeksi hesaplamaları için algoritma çağrıları
                        a = hs.algos(f'{TEMEL_DIZIN}/static/{orthophoto["odm_orthophoto"]}', proje.hashing_path)
                        
                        # Hangi algoritmanın seçildiğine göre uygun metot çağrılır
                        if saglik_renk == "ndvi":
                            sonuc = a.Ndvi(post_aralik, renk_haritasi)
                        elif saglik_renk == "gli":
                            sonuc = a.Gli(post_aralik, renk_haritasi)
                        elif saglik_renk == "vari":
                            sonuc = a.Vari(post_aralik, renk_haritasi)
                        elif saglik_renk == "vndvi":
                            sonuc = a.VNDVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "ndyi":
                            sonuc = a.NDYI(post_aralik, renk_haritasi)
                        elif saglik_renk == "ndre":
                            sonuc = a.NDRE(post_aralik, renk_haritasi)
                        elif saglik_renk == "ndwi":
                            sonuc = a.NDWI(post_aralik, renk_haritasi)
                        elif saglik_renk == "ndvi_blue":
                            sonuc = a.NDVI_Blue(post_aralik, renk_haritasi)
                        elif saglik_renk == "endvi":
                            sonuc = a.ENDVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "mpri":
                            sonuc = a.MPRI(post_aralik, renk_haritasi)
                        elif saglik_renk == "exg":
                            sonuc = a.EXG(post_aralik, renk_haritasi)
                        elif saglik_renk == "tgi":
                            sonuc = a.TGI(post_aralik, renk_haritasi)
                        elif saglik_renk == "bai":
                            sonuc = a.BAI(post_aralik, renk_haritasi)
                        elif saglik_renk == "gndvi":
                            sonuc = a.GNDVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "grvi":
                            sonuc = a.GRVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "savi":
                            sonuc = a.SAVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "mnli":
                            sonuc = a.MNLI(post_aralik, renk_haritasi)
                        elif saglik_renk == "msr":
                            sonuc = a.MSR(post_aralik, renk_haritasi)
                        elif saglik_renk == "rdvi":
                            sonuc = a.RDVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "tdvi":
                            sonuc = a.TDVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "osavi":
                            sonuc = a.OSAVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "lai":
                            sonuc = a.LAI(post_aralik, renk_haritasi)
                        elif saglik_renk == "evi":
                            sonuc = a.EVI(post_aralik, renk_haritasi)
                        elif saglik_renk == "arvi":
                            sonuc = a.ARVI(post_aralik, renk_haritasi)
                        else:
                            # Eğer bilinmeyen bir algoritma seçildiyse
                            return render(request, "map.html", {
                                "kullanici_profili": kullanici_profili,
                                "hata": "Geçersiz algoritma seçimi",
                                "algoritmalar": algoritmalar,
                                "renkler": renkler
                            })
                            
                        return render(request, "map.html", {
                            "kullanici_profili": kullanici_profili,
                            "orthophoto": sonuc,
                            "algoritmalar": algoritmalar,
                            "renkler": renkler,
                            "statik": statik,
                            "resim_bilgileri": resim_bilgileri
                        })
                except Exception as e:
                    return render(request, "map.html", {
                        "kullanici_profili": kullanici_profili,
                        "hata": f"İşlem sırasında hata oluştu: {str(e)}",
                        "algoritmalar": algoritmalar,
                        "renkler": renkler
                    })
            else:
                orthophoto = istatistik_al(id=proje.hashing_path, tur="orthophoto")
                statik = istatistik_al(id=proje.hashing_path, tur="static")
                resim_bilgileri = istatistik_al(id=proje.hashing_path, tur="images_info")
                print("resim_bilgileri", resim_bilgileri)
                return render(request, "map.html", {
                    "kullanici_profili": kullanici_profili,
                    "proje": proje,
                    "orthophoto": orthophoto,
                    "algoritmalar": algoritmalar,
                    "renkler": renkler,
                    "statik": statik,
                    "resim_bilgileri": resim_bilgileri
                })
        except Exception as e:
            return render(request, "error.html", {"hata": f"Haritalama işlemi sırasında hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")
