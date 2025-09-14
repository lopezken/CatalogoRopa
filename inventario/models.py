# inventario/models.py

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    talla = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - Talla: {self.talla}'

# --- NUEVOS MODELOS ---

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    # Dejamos la relación por si en el futuro no borramos los productos
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    # --- NUEVOS CAMPOS PARA GUARDAR EL HISTORIAL ---
    # Copiamos los datos para que no se pierdan si el producto se borra
    producto_nombre = models.CharField(max_length=200)
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # --- CAMPO NUEVO PARA TIPO DE PAGO ---
    TIPO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]
    tipo_pago = models.CharField(
        max_length=50,
        choices=TIPO_PAGO_CHOICES,
        default='Efectivo'
    )

    cantidad = models.PositiveIntegerField(default=1)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venta de {self.producto_nombre} a {self.cliente.nombre}'