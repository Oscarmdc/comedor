from django.urls import path
from .views import ventas

urlpatterns = [
    path('', ventas, name='Ventas'),
]