# inventario/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Producto, Cliente, Venta
from .forms import ProductoForm, VentaForm

# --- Vistas de Productos ---

def galeria_productos(request):
    """
    Muestra la galería de todos los productos.
    """
    productos = Producto.objects.all()
    context = {
        'productos': productos
    }
    return render(request, 'inventario/galeria.html', context)


def agregar_producto(request):
    """
    Maneja el formulario para agregar un nuevo producto.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/agregar_producto.html', {'form': form})


# --- Vistas de Clientes y Ventas ---

def lista_clientes(request):
    """
    Muestra la lista de clientes con sus estadísticas de compra.
    """
    clientes = Cliente.objects.annotate(
        total_gastado=Sum('venta__precio_total'),
        cantidad_productos=Sum('venta__cantidad')
    ).order_by('-total_gastado')

    context = {
        'clientes': clientes
    }
    return render(request, 'inventario/lista_clientes.html', context)


def registrar_venta(request, producto_id):
    """
    Maneja el proceso de vender un producto a un cliente.
    """
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            cliente_existente = form.cleaned_data.get('cliente_existente')
            nuevo_cliente_nombre = form.cleaned_data.get('nuevo_cliente_nombre')

            cliente = None
            if cliente_existente:
                cliente = cliente_existente
            elif nuevo_cliente_nombre:
                cliente, created = Cliente.objects.get_or_create(nombre=nuevo_cliente_nombre)
            else:
                form.add_error(None, "Debes seleccionar un cliente existente o ingresar uno nuevo.")
            
            if cliente:
                # 1. Se crea el registro de la venta con los nuevos detalles
                Venta.objects.create(
                    producto=producto,
                    cliente=cliente,
                    # Copiamos los datos importantes
                    producto_nombre=producto.nombre,
                    producto_precio=producto.precio,
                    # Guardamos el nuevo campo
                    tipo_pago=form.cleaned_data.get('tipo_pago'),
                    cantidad=1,
                )
                
                # 2. Se elimina el producto del stock
                producto.delete()
                
                # 3. Se redirige a la galería
                return redirect('galeria_productos')
    else:
        form = VentaForm()

    context = {
        'form': form,
        'producto': producto
    }
    return render(request, 'inventario/registrar_venta.html', context)

def historial_ventas(request):
    """
    Muestra el historial completo de ventas y un resumen.
    """
    ventas = Venta.objects.all().order_by('-fecha_venta')
    
    # Calculamos los totales
    total_ventas = ventas.count()
    ingresos_totales = ventas.aggregate(Sum('producto_precio'))['producto_precio__sum'] or 0

    context = {
        'ventas': ventas,
        'total_ventas': total_ventas,
        'ingresos_totales': ingresos_totales,
    }
    return render(request, 'inventario/historial_ventas.html', context)