# inventario/forms.py

from django import forms
from .models import Producto, Cliente, Venta 

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'talla', 'imagen']

# --- NUEVO FORMULARIO ---

class VentaForm(forms.Form):
    cliente_existente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Seleccionar Cliente Existente"
    )
    nuevo_cliente_nombre = forms.CharField(max_length=200, required=False, label="O Ingresar Nuevo Cliente")
    
    # --- AÑADE ESTE CAMPO ---
    tipo_pago = forms.ChoiceField(
        choices=Venta.TIPO_PAGO_CHOICES,
        label="Método de Pago"
    )