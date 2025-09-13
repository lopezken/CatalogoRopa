from django.shortcuts import render
from .models import Producto, Variante

def galeria_productos(request):
    # Obtenemos el parámetro 'talla' de la URL (ej: ?talla=M)
    talla_filtrada = request.GET.get('talla')

    if talla_filtrada:
        # Si se filtró por una talla, buscamos los productos que tienen esa variante.
        # .distinct() asegura que no tengamos productos duplicados en la lista.
        productos = Producto.objects.filter(variantes__talla=talla_filtrada).distinct()
    else:
        # Si no hay filtro, mostramos todos los productos.
        productos = Producto.objects.all()

    # Obtenemos una lista de todas las tallas únicas disponibles para crear los botones de filtro
    tallas_disponibles = Variante.objects.values_list('talla', flat=True).distinct()

    context = {
        'productos': productos,
        'tallas_disponibles': tallas_disponibles
    }
    
    return render(request, 'inventario/galeria.html', context)