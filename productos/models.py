from django.db import models

# Create your models here.
class Categorias (models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        verbose_name= 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        return self.nombre


class Productos(models.Model):
    nombre = models.CharField(max_length=250, null=False, blank=False)
    descripcion = models.CharField(max_length=300, null=False, blank=False)
    precio = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    stock = models.IntegerField(null=False, blank=False)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', null=True,blank=True)

    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name= 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.nombre


    