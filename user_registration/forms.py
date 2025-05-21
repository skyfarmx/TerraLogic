from django import forms
from django.contrib.auth.forms import UserCreationForm  
from user_registration.models import Kullanicilar
from django.contrib import admin


class KullaniciFormu(UserCreationForm):
    """
    Kullanıcı oluşturma formu, e-posta alanı eklenmiş hali.
    """
    email = forms.EmailField(max_length=200) 
    USERNAME_FIELD = 'email' 


class KullanicilarFormu(forms.ModelForm):
    """
    Kullanıcı profil bilgileri için form.
    """
    class Meta:
        model = Kullanicilar
        fields = '__all__'


# Admin panelinde Kullanicilar modelini kaydet
admin.site.register(Kullanicilar)
