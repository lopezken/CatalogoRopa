# tienda_ropa/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- Importa esto
from django.conf.urls.static import static  # <-- Importa esto también

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
]

# Añade esta línea al final
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)