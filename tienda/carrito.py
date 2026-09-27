

class Carrito: # 28/28.1 carrito
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': 1,
                'imagen': producto.imagen
            }
        else:
            self.carrito[producto_id]['cantidad'] += 1
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] -= 1
            if self.carrito[producto_id]['cantidad'] < 1:
                self.eliminar(producto)
            else:
                self.guardar_carrito()

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True