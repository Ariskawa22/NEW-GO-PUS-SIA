from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms

from catalog.models import Profile


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField()

    def clean_renewal_date(self):
        data = self.cleaned_data['batas_waktu']

        if data < datetime.date.today():
            raise ValidationError(_('Tanggal invalid - Batas waktu tidak bisa berada di masa lalu'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Tanggal invalid - Batas waktu terbatas pada 4 minggu.'))

        # Remember to always return the cleaned data.
        return data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('kelas', 'nis', 'telepon', 'url_foto')
