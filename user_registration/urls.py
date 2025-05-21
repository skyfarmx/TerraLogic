from django.urls import path, re_path

from . import views
app_name = 'kullanici_kayit'


urlpatterns = [
    re_path(r'kullanici_profil/(?:id-(?P<id>[0-9]+)/)?$', views.kullanici_profil, name='kullanici_profil'),          
    re_path(r'kullanici_duzenle/(?:id-(?P<id>[0-9]+)/)?$', views.kullanici_duzenle, name='kullanici_duzenle'),          
    path('cikis', views.cikis, name='cikis'),
    path('fiyatlandirma', views.fiyatlandirma, name='fiyatlandirma'),
    path('takvim', views.takvim, name='takvim'),
    path('giris', views.giris, name='giris'),      
    path('giris_yap', views.giris_yap, name='giris_yap'),      
    path('kayit_ol', views.kayit_ol, name='kayit_ol'),    
    path('sifremi_unuttum', views.sifremi_unuttum, name='sifremi_unuttum'), 
    path('fiyatlandirma', views.fiyatlandirma, name='fiyatlandirma'),
    path('takvim', views.takvim, name='takvim'),
]
