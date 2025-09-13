from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen_principal = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.nombre

class Variante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    talla = models.CharField(max_length=50)
    color = models.CharField(max_length=50) 
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.producto.nombre} - Talla: {self.talla} - Color: {self.color}'