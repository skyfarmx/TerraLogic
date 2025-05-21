from django.db import models
from django.contrib.auth.models import User


class Kullanicilar(models.Model):
    """
    Kullanıcı profil bilgilerini saklayan model.
    Django'nun varsayılan User modeline ek bilgiler ekler.
    """
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    kat_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, verbose_name='Adı')
    father_name = models.CharField(max_length=250, verbose_name='Ata adı')
    last_name = models.CharField(max_length=250, verbose_name='Soyadı')
    city = models.CharField(max_length=250, verbose_name='Ülke ve ya Şehir')
    picture = models.ImageField(upload_to='assets/images', blank=True, null=True, verbose_name='Resim')
    phone = models.CharField(max_length=250, verbose_name='Telefon')
    departments = models.CharField(max_length=250, verbose_name='Departmanlar')
    gender = models.CharField(max_length=250, verbose_name='Cinsiyet')
    bio = models.CharField(max_length=2500, verbose_name='Biyografi')
    birthday = models.DateField(verbose_name='Doğum günü')
    address = models.CharField(max_length=2500, verbose_name='Adres')   
    website = models.URLField(max_length=250, default=None, verbose_name='Web sitesi')   

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Kullanıcı Profili'
        verbose_name_plural = 'Kullanıcı Profilleri'
