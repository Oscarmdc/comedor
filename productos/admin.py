from django.contrib import admin
from productos.models import Categorias, Productos

# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    readonly_fields = ('create', 'update')
    search_fields = (('nombre'),)
    list_filter = ['categoria']
    

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    list_filter = ['nombre']
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Categorias, CategoriaAdmin)
admin.site.register(Productos, ProductoAdmin)