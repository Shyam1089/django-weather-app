from django import forms
from django.utils.translation import gettext as _


class InputForm(forms.Form):
    search = forms.CharField(label=_("Select City"),
                             max_length=50, localize=True)
