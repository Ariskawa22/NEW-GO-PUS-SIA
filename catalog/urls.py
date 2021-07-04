from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from catalog.views import index, BukuUpdate, BukuDelete, BukuCreate, BukuDetailView, SemuaBukuKeluar, \
    BukuListView, bukuKeluarUser, perbaharui_status_buku, PenulisListView, PenulisDetailView, PenulisCreate, \
    PenulisUpdate, view_profile, create_profile, create_user, raw, search, panduan

urlpatterns = [
    path('', index, name='index'),
    path('buku/', search, name="search"),
    path('buku/raw', raw, name="raw"),
    path('buku/<int:pk>', BukuDetailView.as_view(), name="detail-buku"),
    path('bukusaya/', bukuKeluarUser, name="buku-saya"),
    path(r'buku/keluar/', SemuaBukuKeluar.as_view(), name="buku-keluar"),
    path('buku/<int:pk>/perbaharui', perbaharui_status_buku, name="perbaharui-buku"),
    path('buku/tambah/', BukuCreate.as_view(), name="tambah-buku"),
    path('buku/ubah/', BukuUpdate.as_view(), name="ubah-buku"),
    path('buku/hapus/', BukuDelete.as_view(), name="hapus-buku"),
    path('penulis/', PenulisListView.as_view(), name="penulis"),
    path('penulis/<int:pk>', PenulisDetailView.as_view(), name="detail-penulis"),
    path('penulis/tambah', PenulisCreate.as_view(), name="tambah-penulis"),
    path('penulis/ubah', PenulisUpdate.as_view(), name="ubah-penulis"),
    path('profil', view_profile, name="view-profile"),
    url('login/', auth_views.LoginView.as_view(),name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', create_user, name="register"),
    path('account-details/', create_profile, name="profile-details"),
    path('panduan/', panduan, name="panduan")
]
