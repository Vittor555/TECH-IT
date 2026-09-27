# TECH-IT — Plataforma E-Commerce y Gestión de Inventario

**TECH-IT** es una solución web integral desarrollada con **Django** que combina una tienda en línea dinámica para los clientes con un módulo completo de administración
y control de inventario (`/gestion/`).

🎬 **Identidad Multimedia Integrada:** La plataforma incluye un video promocional e interactivo generado mediante **Inteligencia Artificial**,
diseñado para dotar a la web de una identidad propia, dinámica y atractiva para los usuarios.

## 🚀 Características Principales
* **Experiencia Multimedia:** Integración de video promocional/corporativo generado por IA para mejorar la autenticidad y el engagement visual.
* **Catálogo de Productos:** Navegación por categorías, fichas detalladas e imágenes asociadas.
* **Carrito de Compras y Pedidos:** Gestión interactiva de carrito, cálculo automático de importes y generación de pedidos (`tienda_pedido` y `tienda_lineapedido`).
* **Panel de Administración (`/gestion/`):** Control de existencias, productos y proveedores.
* **Internacionalización:** Preparado para soporte multiidioma con archivos `locale`.

## 🛠️ Tecnologías Utilizadas
* **Backend:** Python 3.x, Django Framework.
* **Bases de Datos:** SQLite3 / PostgreSQL.
* **Frontend:** HTML5, CSS3, JavaScript.
* **Herramientas IA:** Generación y optimización de contenido multimedia (video).

## ⚙️ Instalación y Configuración Local

1. **Clonar el repositorio:**
   git clone [https://github.com/Vittor555/TECH-IT.git](https://github.com/Vittor555/TECH-IT.git)
   cd TECH-IT
2. **Crear y activar entorno virtual:**
   python -m venv .venv
# En Windows:
.venv\Scripts\activate

3. **Instalar dependencias:**
   pip install -r requirements.txt

4. **Aplicar migraciones y ejecutar servidor:**
   python manage.py migrate
   python manage.py runserver
   
