from django.urls import path
from .views import informes

urlpatterns = [
    path('', informes, name='Informes'),
]