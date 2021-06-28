import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Penulis(models.Model):
    nama = models.CharField(max_length=60, help_text="Nama penulis")

    def __str__(self):
        return self.nama


class Buku(models.Model):
    judul = models.CharField(max_length=250, help_text="Judul buku")
    penulis = models.ForeignKey(Penulis, on_delete=models.CASCADE)
    url_sampul = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    tahun = models.CharField(max_length=5)
    lokasi = models.TextField()

    class Meta:
        ordering = ['judul', 'penulis', 'tahun']

    def get_absolute_url(self):
        return reverse('detail-buku', args=[str(self.id)])

    def __str__(self):
        return self.judul


class BukuInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    peminjam = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    batas_waktu = models.DateField(null=True, blank=True)

    @property
    def terlambat(self):
        if self.batas_waktu and (date.today() > self.batas_waktu):
            return True
        else:
            return False
    @property
    def hariTersisa(self):
        return str((self.batas_waktu - date.today()).days) + " hari"
    @property
    def terlambatBy(self):
        if self.batas_waktu and (date.today() > self.batas_waktu):
            return str((date.today()-self.batas_waktu).days) + " hari"

    @property
    def denda(self):
        dendaPerHari = 3000
        if self.batas_waktu and (date.today() > self.batas_waktu):
            return "Rp"+str((date.today()-self.batas_waktu).days*3)+" 000"
    STATUS_BUKU = (
        ('k', 'Keluar'),
        ('t', 'Tersedia'),
        ('p', 'Perawatan')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_BUKU,
        blank=True,
        default='p',
        help_text="Ketersediaan Buku"
    )

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.buku.judul)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kelas = models.CharField(blank=True, max_length=120)
    nis = models.CharField(blank=True, max_length=120)
    telepon = models.CharField(max_length=20)
    url_foto = models.CharField(max_length=200)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# Create your models here.
