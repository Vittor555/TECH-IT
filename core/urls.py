

from django.contrib import admin
from django.urls import path
from tienda.views import index
from tienda import views
from django.views.i18n import set_language


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'), # 9  Ruta principal

    path('smartphones/',
         views.smartphones_view, name='smartphones'), # 12.1
    path('smartphones/<str:marca>/',
     views.catalogo_smart_view, name='catalogo_smart'), # 14.2
# 17.3
    path('portatiles/',
         views.portatiles_view, name='portatiles'),
    path('portatiles/<str:marca>/',
     views.catalogo_portatil_view, name='catalogo_portatil'),

# 22
    path('producto/<int:id>/',
         views.detalle_producto_view, name='detalle_producto'),

# 24
    path('nosotros/',
         views.info_nosotros, name = 'nosotros'),

# 27.4
    path('buscar/', views.buscar_productos_view,
         name='buscar'),

# 28.3 - carrito
    path('carrito/', views.carrito_ver_view, name='carrito_ver'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_producto, name='carrito_agregar'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto, name='carrito_eliminar'),
    path('carrito/restar/<int:producto_id>/', views.restar_producto, name='carrito_restar'),
    path('carrito/limpiar/', views.limpiar_carrito, name='carrito_limpiar'),

# 30.2
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido-confirmado/', views.pedido_confirmado_view, name='pedido_confirmado'),

# 32.1 redes sociales
    path('redes-sociales/',views.redes_sociales_view, name='redes_sociales'),

# Traductor(cambio idiomas)
    path('i18n/', set_language, name='set_language'),

#37.3 report PDF
    path('generar-pdf/', views.generar_informe_pdf, name='generar_pdf'),

#38.2
    path('login/', views.login_personalizado, name='login'),
    path('gestion/', views.dashboard_gestion, name='dashboard_gestion'),

# Volver clever
    path('volver/', views.volver_a_origen, name='volver_origen'),


# 39.2
    path('gestion/editar/<int:id>/', views.editar_producto_view, name='editar_producto'),

    path('gestion/eliminar-pedido/<int:id>/', views.eliminar_pedido_view, name='eliminar_pedido'),

    ]
