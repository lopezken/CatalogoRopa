from django.urls import path
from . import views

urlpatterns = [
    path('', views.galeria_productos, name='galeria_productos'),
]