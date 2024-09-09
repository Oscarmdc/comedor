from django.urls import path, include
from .views import menu

urlpatterns = [
    path('', menu, name='Menu'),
    path('Caja/', include('caja.urls')),
    path('Productos/', include('productos.urls')),
    path('Informes/', include('informes.urls')),
    path('Ventas/', include('ventas.urls')),
]