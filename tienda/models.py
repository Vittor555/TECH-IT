from django.db import models


# 35
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la empresa")
    nif = models.CharField(max_length=20, unique=True, verbose_name="NIF / CIF")
    contacto_nombre = models.CharField(max_length=100, verbose_name="Persona de contacto")
    email = models.EmailField(verbose_name="Email corporativo")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")

    def __str__(self):
        return f"{self.nombre} ({self.nif})"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

# 19.1 base de datos

class Producto(models.Model):

    CATEGORIAS = [
        ('SMART', 'Smartphone'),
        ('LAPTOP', 'Portátil'),
    ]

    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50) # apple, samsung, etc.
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    imagen = models.CharField(max_length=255) # Aquí guardaremos la ruta: 'imgsmartphones/...'
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")

    def __str__(self):
        return f"{self.marca.upper()} - {self.nombre}"

# 23 - galeria
class ImagenProducto(models.Model):
        #  foto con un producto específico
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
        # ruta de la foto extra
    imagen = models.CharField(max_length=255)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

#26.1
class InformacionEmpresa(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título de la página")
    historia = models.TextField(verbose_name="Historia o información principal")

    class Meta:
        verbose_name = "Información de la Empresa"
        verbose_name_plural = "Información de la Empresa"

    def __str__(self):
        return self.titulo

# the last step(create a table for DB for products buyed)

class Pedido(models.Model):
    # Guardamos la fecha de forma automática al crearse
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total del Pedido")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion'] # Los más nuevos primero

    def __str__(self):
        return f"Pedido N° {self.id} - Total: {self.total}€"


class LineaPedido(models.Model):
    # Si se borra el pedido general, se borran sus líneas en cascada
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    # Si se borra un producto de la tienda, mantenemos la línea cambiando a SET_NULL para no perder el histórico de ventas
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Guardamos el precio del momento de la compra

    class Meta:
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedidos"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Eliminado'}"