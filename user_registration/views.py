from django.shortcuts import render
from pathlib import Path
from django.contrib.auth import authenticate, login as auth_login, logout as log_out
from django.shortcuts import redirect
from yolowebapp2 import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import KullaniciFormu, KullanicilarFormu
from dron_map.forms import Projects_Form
from user_registration.models import Kullanicilar
from django.shortcuts import get_object_or_404
TEMEL_DIZIN = Path(__file__).resolve().parent.parent


def kullanici_profil(request, id):
    """
    Belirli bir kullanıcının profilini görüntüler.
    
    Parametreler:
    - request: HTTP isteği
    - id: Görüntülenecek kullanıcı ID'si
    
    Dönüş:
    - Kullanıcı profili şablonu
    """
    if request.user.is_authenticated:
        try:
            kullanici = get_object_or_404(Kullanicilar, kat_id=id)
            return render(request, "user.html", {'kullanici_profili': kullanici})
        except Exception as e:
            return render(request, "error.html", {"hata": f"Kullanıcı profili görüntülenirken hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")


def kullanici_duzenle(request, id):
    """
    Kullanıcı profilini düzenleme sayfasını gösterir ve işler.
    
    Parametreler:
    - request: HTTP isteği
    - id: Düzenlenecek kullanıcı ID'si
    
    Dönüş:
    - Kullanıcı düzenleme şablonu
    """
    if request.user.is_authenticated:
        try:
            kullanici_model = Kullanicilar.objects.get(kat_id=id)

            if request.method == 'POST':
                form = KullanicilarFormu(request.POST or None,
                                request.FILES or None, instance=kullanici_model)

                if form.is_valid():
                    form.picture = form.cleaned_data['picture']
                    form.save()
                
                kullanici = get_object_or_404(Kullanicilar, kat_id=id)
                return render(request, "user_edit.html", {'kullanici_profili': kullanici})
            else:
                kullanici = get_object_or_404(Kullanicilar, kat_id=id)
                return render(request, "user_edit.html", {'kullanici_profili': kullanici})
        except Exception as e:
            return render(request, "error.html", {"hata": f"Kullanıcı profili düzenlenirken hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")


def giris(request):
    """
    Giriş sayfasını gösterir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Giriş şablonu veya yönlendirme
    """
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, "login.html")


def giris_yap(request):
    """
    Kullanıcı giriş işlemini gerçekleştirir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Başarılı ise ana sayfaya yönlendirme, başarısız ise giriş sayfası
    """
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        try:
            kullanici_adi = request.POST.get('username')
            sifre = request.POST.get('password')
            kullanici = authenticate(username=kullanici_adi, password=sifre)
            
            if kullanici is not None and kullanici.is_active:
                auth_login(request, kullanici)
                return redirect('/', kullanici)
            else:
                return redirect(settings.LOGOUT_REDIRECT_URL)
        except Exception as e:
            return render(request, "login.html", {"hata": f"Giriş yapılırken hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")


def kayit_ol(request):
    """
    Yeni kullanıcı kaydı oluşturma işlemini gerçekleştirir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Başarılı ise ana sayfaya yönlendirme, başarısız ise kayıt formu
    """
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = KullaniciFormu(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                kullanici_adi = form.cleaned_data['username']
                sifre = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                kullanici = authenticate(username=kullanici_adi,
                                password=sifre, email=email)
                auth_login(request, kullanici)
                return redirect('/')
            except Exception as e:
                return render(request, 'signup.html', {'form': form, 'hata': f"Kayıt sırasında hata oluştu: {str(e)}"})
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def sifremi_unuttum(request):
    """
    Şifremi unuttum sayfasını gösterir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Şifremi unuttum şablonu
    """
    return render(request, "forgot_password.html")


def cikis(request):
    """
    Kullanıcı çıkış işlemini gerçekleştirir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Çıkış sonrası yönlendirilen sayfa
    """
    log_out(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def takvim(request):
    """
    Takvim sayfasını gösterir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Takvim şablonu veya giriş sayfası
    """
    if request.user.is_authenticated:
        try:
            kullanici_profili = Kullanicilar.objects.get(kat_id=request.user.id)
            return render(request, "calendar.html", {"kullanici_profili": kullanici_profili})
        except Kullanicilar.DoesNotExist:
            return render(request, "error.html", {"hata": "Kullanıcı profili bulunamadı"})
        except Exception as e:
            return render(request, "error.html", {"hata": f"Takvim sayfası yüklenirken hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")


def fiyatlandirma(request):
    """
    Fiyatlandırma sayfasını gösterir.
    
    Parametreler:
    - request: HTTP isteği
    
    Dönüş:
    - Fiyatlandırma şablonu veya giriş sayfası
    """
    if request.user.is_authenticated:
        try:
            kullanici_profili = Kullanicilar.objects.get(kat_id=request.user.id)
            return render(request, "pricing.html", {"kullanici_profili": kullanici_profili})
        except Kullanicilar.DoesNotExist:
            return render(request, "error.html", {"hata": "Kullanıcı profili bulunamadı"})
        except Exception as e:
            return render(request, "error.html", {"hata": f"Fiyatlandırma sayfası yüklenirken hata oluştu: {str(e)}"})
    else:
        return render(request, "login.html")
