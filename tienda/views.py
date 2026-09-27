from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import Producto, InformacionEmpresa, Pedido, LineaPedido, Proveedor # 21 y 26.3(InformacionEmpresa) + last step (Pedido, LineaPedido) + 39.3 (Proveedor)
from .carrito import Carrito
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProductoForm # 39.3

# 8
def index(request):
    return render(request, 'index.html')
#12.1
def smartphones_view(request):
    return render(request, 'smartphones.html')

#14.1  / 18.1 - creacion diccionario (es decir cambiamos 14.1) /
# 21 - cambiamos  18.1 - (porque ya tenemos db creada y no hace falta tener diccionario)
def catalogo_smart_view(request, marca):
    # no sea doble click al vover
    request.session['ultima_url'] = request.build_absolute_uri()

    # 21 Buscamos en la DB: filtramos por categoría SMART y por la marca
    # 21 Usamos __iexact para que no importe si es 'Apple' o 'apple'
    productos = Producto.objects.filter(categoria='SMART', marca__iexact=marca)

    context = {
        'marca': marca.upper(),
        'productos': productos
    }
    return render(request, 'productossmart.html', context)


# 17.2
def portatiles_view(request):
    return render(request, 'portatiles.html')


# 17.2 / 18.1 - creacion dic (es decir cambiamos 17.2)
# 21 - cambiamos  18.1 - (porque ya tenemos db creada y no hace falta tener diccionario)

def catalogo_portatil_view(request, marca):


    request.session['ultima_url'] = request.build_absolute_uri()

    # 21 Lo mismo para portátiles, pero categoría LAPTOP
    productos = Producto.objects.filter(categoria='LAPTOP', marca__iexact=marca)

    context = {
        'marca': marca.upper(),
        'productos': productos
    }
    return render(request, 'productosportatil.html', context)


# 22
def detalle_producto_view(request, id):
    producto = get_object_or_404(Producto, id=id) # busqueda por id

    return render(request, 'detalles.html', {'producto': producto})

#24

# 26.3 (es decir 24 - modificamos)
def info_nosotros(request):
    # Cogemos el primer registro que encuentre en la base de datos
    info = InformacionEmpresa.objects.first()

    # Pasamos el objeto 'info' dentro del diccionario de contexto
    return render(request, 'infonosotros.html', {'info': info})

# 27.3
def buscar_productos_view(request):
    # lo que el usuario escribió en el input con name="q"
    query = request.GET.get('q', '')

    # Si ha escrito algo, filtramos en la base de datos por el nombre
    if query:
        # __icontains busca coincidencias sin importar mayúsculas o minúsculas
        resultados = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query) |
            Q(proveedor__nombre__icontains=query)  # Busca  proveedor
        ).distinct()  # Evita que salgan resultados duplicados
    else:
        resultados = Producto.objects.none()  # Devuelve una lista vacía si no hay texto

    context = {
        'productos': resultados,
        'busqueda': query
    }
    return render(request, 'resultados_busqueda.html', context)

# 28.2

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto=producto)

    # carrito con producto añadido - mensaje
    messages.success(request, f"¡{producto.nombre} INCORPORADO AL SISTEMA!")

    return redirect(request.META.get('HTTP_REFERER', 'index'))

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto=producto)
    return redirect("carrito_ver")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto=producto)
    return redirect("carrito_ver")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito_ver")


def carrito_ver_view(request): #28.5
    # Inicializamos el carrito de la sesión
    carrito_sesion = request.session.get('carrito', {})

    # Calculamos el total (precio * cantidad) de cada producto
    total_general = 0
    for item in carrito_sesion.values():
        total_general += float(item['precio']) * item['cantidad']

    context = {
        'carrito': carrito_sesion,
        'total_general': total_general
    }
    return render(request, 'carrito.html', context)

# 30.1
def checkout_view(request):
    # Recuperamos el carrito para calcular el total en la pantalla de pago también
    carrito_sesion = request.session.get('carrito', {})
    total_general = 0
    for item in carrito_sesion.values():
        total_general += float(item['precio']) * item['cantidad']

    context = {
        'carrito': carrito_sesion,
        'total_general': total_general
    }
    return render(request, 'checkout.html', context)

# 30.1 + last step (modification - well, was changed all)
def pedido_confirmado_view(request):
    carrito_sesion = request.session.get('carrito', {})
    # Si el carrito está vacío, redirigimos al index para evitar registros vacíos
    if not carrito_sesion:
        return redirect('index')

    # total general del pedido
    total_general = 0
    for item in carrito_sesion.values():
        total_general += float(item['precio']) * item['cantidad']

    #Creamos el objeto Pedido principal en la Base de Datos
    nuevo_pedido = Pedido.objects.create(total=total_general)

    # Recorer el carrito + insertar cada producto en la tabla LineaPedido
    for item in carrito_sesion.values():
        # Recuperar la instancia real del producto usando su ID
        producto_instancia = get_object_or_404(Producto, id=item['producto_id'])

        LineaPedido.objects.create(
            pedido=nuevo_pedido,
            producto=producto_instancia,
            cantidad=item['cantidad'],
            precio_unitario=float(item['precio'])
        )

    # 4. Una vez guardado de forma permanente en la DB, vaciamos la sesión
    carrito = Carrito(request)
    carrito.limpiar()

    # Pasamos el pedido al contexto por si quieres mostrar el N° de Pedido en la plantilla html
    return render(request, 'pedido_confirmado.html', {'pedido': nuevo_pedido})

# 32.1 redes sociales

def redes_sociales_view (request):
    return render(request, 'socialred.html')

# "volver" clever (last url(came from))
def volver_a_origen(request):
    url_origen = request.session.get('ultima_url', 'index')
    return redirect(url_origen)

#37.2 report

def generar_informe_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Inventario_TechIT.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Encabezado con estilo
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "INFORME DE INVENTARIO - TECH-IT")
    p.line(50, height - 60, 550, height - 60)

    # Cuerpo del informe
    p.setFont("Helvetica", 12)
    productos = Producto.objects.all().select_related('proveedor')
    y = height - 100

    for prod in productos:
        proveedor_nombre = prod.proveedor.nombre if prod.proveedor else "N/A"
        texto = f"Producto: {prod.nombre} | Marca: {prod.marca} | Proveedor: {proveedor_nombre} | Precio: {prod.precio} €"
        p.drawString(50, y, texto)
        y -= 25

        # Si llegamos al final de la página, creamos una nueva
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 12)

    p.showPage()
    p.save()
    return response

# 38. Vista de Login

def login_personalizado(request):
    if request.method == 'POST':
        #  usuario y contraseña del formulario
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard_gestion') #  al panel de control

        else:
            # mensaje de error
            messages.error(request, "Usuario o contraseña incorrecto.")

    return render(request, 'login.html')

#38.3 (   now it's 39.3)
@login_required
def dashboard_gestion(request):
    todos_productos = Producto.objects.all().select_related('proveedor')
    ultimos_pedidos = Pedido.objects.all().order_by('-fecha_creacion')[:10]

    context = {
        'productos': todos_productos,
        'pedidos': ultimos_pedidos
    }
    return render(request, 'dashboard_gestion.html', context)

# 39.3 (continuamos) for edit all of product
@login_required
def editar_producto_view(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        # Pasamos los datos del formulario POST directamente a la instancia del producto
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Django hace el UPDATE en la DB de todos los campos automáticamente
            messages.success(request, f"¡{producto.nombre} actualizado correctamente!")
            return redirect('dashboard_gestion')
    else:
        # Si entramos de primeras, carga el formulario relleno con los datos actuales del producto
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_pedido_view(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    id_guardado = pedido.id # Guardamos el número para el mensaje
    pedido.delete() # ¡Bum! Borrado de la base de datos
    messages.success(request, f"¡Pedido #{id_guardado} eliminado del sistema!")
    return redirect('dashboard_gestion')