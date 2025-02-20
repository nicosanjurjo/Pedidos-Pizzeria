from django import forms
from .models import Zona


class FormZona(forms.ModelForm):
    class Meta:
        model = Zona
        fields = '__all__'

class FormZonaEdit(forms.ModelForm):
    class Meta:
        model = Zona
        fields = '__all__'