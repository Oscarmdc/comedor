from django.db import models
from productos.models import Productos

# Create your models here.
class Turno(models.Model):
    # al abrir turno
    turno_abierto = models.BooleanField(default=True, null=False)
    fondo_caja = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    # al cerrar turno
    numero_ordenes = models.IntegerField(null= True, blank=True)
    fecha_cierre = models.DateTimeField(null= True, blank=True)
    total_efectivo = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    total_tarjeta = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    # llaves foraneas

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'


class Orden(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=15, decimal_places=2,null=False,blank=False, default=0)
    efectivo = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tarjeta = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    numero_orden = models.IntegerField()
    # llaves foraneas
    id_turno = models.ForeignKey(Turno, null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Productos, null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de Orden'