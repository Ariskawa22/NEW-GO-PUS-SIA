from django.contrib import admin
from .models import Penulis, Buku, BukuInstance, Profile


class BukuInline(admin.TabularInline):
    model = Buku


class InstanceBukuInline(admin.TabularInline):
    model = BukuInstance


@admin.register(Penulis)
class PenulisAdmin(admin.ModelAdmin):
    list_display = ['nama']
    fields = ['nama']
    inlines = [BukuInline]


class BukuAdmin(admin.ModelAdmin):
    list_filter = ('judul', 'penulis')
    inlines = [InstanceBukuInline]


@admin.register(BukuInstance)
class BukuInstanceAdmin(admin.ModelAdmin):
    list_display = ("buku", "peminjam", "id", "status", "batas_waktu")
    list_filter = ("status", "batas_waktu")
    fields = ("id", "buku", "peminjam", "status", "batas_waktu")


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'kelas', 'nis', 'telepon')


admin.site.register(Profile, ProfileAdmin)
