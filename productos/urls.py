from django.urls import path
from .views import producto

urlpatterns = [
    path('', producto, name='Productos'),
]