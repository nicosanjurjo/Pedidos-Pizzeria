from django import forms
from .models import Producto


class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormProductoEdit(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'