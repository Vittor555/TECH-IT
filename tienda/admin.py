from django.contrib import admin
from .models import Producto,ImagenProducto,InformacionEmpresa, Proveedor, Pedido, LineaPedido


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 3 #  3 fotos de golpe

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]

#26.2 (+ import: from .models import InformacionEmpresa )
admin.site.register(InformacionEmpresa)

#35.2

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nif', 'contacto_nombre', 'telefono')
    search_fields = ('nombre', 'nif')

admin.site.register(Pedido)
admin.site.register(LineaPedido)