from django.urls import path
from .views import caja

urlpatterns = [
    path('', caja, name='Caja'),
]