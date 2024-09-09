from django.contrib import admin
from .models import Turno, Orden, DetalleOrden

# Register your models here.
class TurnosAdmin (admin.ModelAdmin):
    list_display = ('id','turno_abierto','fondo_caja','fecha_inicio','numero_ordenes','fecha_cierre','total_efectivo','total_tarjeta')


admin.site.register(Turno, TurnosAdmin)
admin.site.register(Orden)
admin.site.register(DetalleOrden)