import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.checks import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from . import forms
from .forms import RenewBookForm, ProfileForm, UserForm, RegistrationForm
from .models import Buku, BukuInstance, Penulis, Profile
from django.views import generic


# Create your views here.

def index(request):
    jumlah_koleksi = Buku.objects.all().count()
    jumlah_buku = BukuInstance.objects.all().count()
    jumlah_buku_tersedia = BukuInstance.objects.filter(status__exact="t").count()
    jumlah_penulis = Penulis.objects.all().count()

    return render(
        request,
        "index.html",
        context={
            'jumlah_koleksi': jumlah_koleksi,
            'jumlah_buku': jumlah_buku,
            'jumlah_buku_tersedia': jumlah_buku_tersedia,
            'jumlah_penulis': jumlah_penulis}
    )


class BukuListView(generic.ListView):
    model = Buku
    paginate_by = 10


class BukuDetailView(generic.DetailView):
    model = Buku


class PenulisListView(generic.ListView):
    model = Penulis
    paginate_by = 10


class PenulisDetailView(generic.DetailView):
    model = Penulis


class BukuKeluarUser(LoginRequiredMixin, generic.ListView):
    model = BukuInstance
    template_name = 'daftar_buku_terpinjam_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BukuInstance.objects.filter(peminjam=self.request.user).filter(status__exact="k").order_by('batas_waktu')


class SemuaBukuKeluar(PermissionRequiredMixin, generic.ListView):
    model = BukuInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'daftar_semua_buku_terpinjam'
    paginate_by = 10

    def get_queryset(self):
        return BukuInstance.objects.filter(status__exact="k").order_by('batas_waktu')


@login_required
@permission_required('catalog.can_mark_returned')
def perbaharui_status_buku(request, pk):
    book_instance = get_object_or_404(BukuInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            BukuInstance.batas_waktu = form.cleaned_data['renewal_date']
            BukuInstance.save()
            return HttpResponseRedirect(reverse('buku-keluar'))
    else:
        batas_waktu_baru = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': batas_waktu_baru})

    context = {
        'form': form,
        'book_instance': BukuInstance,
    }

    return render(request, 'perbaharui_buku.html', context)


class PenulisCreate(PermissionRequiredMixin, CreateView):
    model = Penulis
    fields = ['nama']
    permission_required = 'catalog.can_mark_returned'


class PenulisUpdate(PermissionRequiredMixin, UpdateView):
    model = Penulis
    fields = ['nama']
    permission_required = "catalog.can_mark_returned"


class BukuCreate(PermissionRequiredMixin, CreateView):
    model = Buku
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BukuUpdate(PermissionRequiredMixin, UpdateView):
    model = Buku
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BukuDelete(PermissionRequiredMixin, DeleteView):
    model = Buku
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


@transaction.atomic()
@login_required()
def view_profile(request):
    return render(request, 'view_profile.html')


@transaction.atomic()
def create_user(request):
    form = RegistrationForm(request.POST)
    message = "Create your account"
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data.get("username"),
                                    password=form.cleaned_data.get("password1"))
            """if authenticate(request, new_user):"""
            login(request, new_user)
            return HttpResponseRedirect('/account-details/')
    context = {'form': form}
    return render(request, 'auth/register.html', context)


@transaction.atomic()
@login_required()
def create_profile(request):
    form = ProfileForm(request.POST)
    message = "Add your profile"
    if request.method == 'POST':
        formProfile = ProfileForm(request.POST, instance=request.user.profile)
        if formProfile.is_valid():
            formProfile.save()
            return redirect('view-profile')
    else:
        current_user = request.user.get_username()
        context = {
            'form': ProfileForm(instance=request.user.profile),
            'name': request.user.first_name
        }

    return render(request, 'auth/add_profile.html', context)


@transaction.atomic()
@login_required()
def view_profile(request):
    return render(request, 'auth/view_profile.html')


