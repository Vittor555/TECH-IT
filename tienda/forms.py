from django import forms
from .models import Producto

# 39.1
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Añadimos todos los campos que queremos que el empleado pueda editar
        fields = ['nombre', 'marca', 'categoria', 'imagen', 'precio', 'descripcion', 'proveedor']

        # Le añadimos estilos CSS bonitos para que se integre con tu estética cyberpunk
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
        }