from datetime import date

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.cargar_datos()

    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        # Semana 16: cada usuario se carga con su rol.
        self.usuarios = [
            Usuario(
                datos.get("identificacion", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contrasena", ""),
                datos.get("rol", "Cliente"),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("categoria", ""),
                datos.get("precio", 0),
                datos.get("stock", 0),
            )
            for datos in productos_json
        ]

        # Semana 15: carga las ventas persistidas para mostrarlas en la interfaz.
        self.ventas = [
            Venta(
                datos.get("identificador", ""),
                datos.get("usuario_id", ""),
                datos.get("producto_codigo", ""),
                datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def validar_acceso(self, usuario, contrasena):
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado
        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        return self.usuarios

    def listar_productos(self):
        return self.productos

    def listar_ventas(self):
        return self.ventas

    # ── Productos ─────────────────────────────────────────────────────────────

    def guardar_productos(self):
        datos = [
            {
                "codigo": p.codigo,
                "nombre": p.nombre,
                "categoria": p.categoria,
                "precio": p.precio,
                "stock": p.stock,
            }
            for p in self.productos
        ]
        self.archivo_servicio.escribir_json("productos.json", datos)

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def registrar_producto(self, codigo, nombre, categoria, precio, stock):
        nuevo = Producto(codigo, nombre, categoria, precio, stock)
        if self.buscar_producto_por_codigo(nuevo.codigo) is not None:
            raise ValueError("Ya existe un producto con ese codigo.")
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(self, codigo, nombre, categoria, precio, stock):
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")
        validado = Producto(codigo, nombre, categoria, precio, stock)
        producto.nombre = validado.nombre
        producto.categoria = validado.categoria
        producto.precio = validado.precio
        producto.stock = validado.stock
        self.guardar_productos()
        return producto

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")
        self.productos.remove(producto)
        self.guardar_productos()
        return producto

    # ── Usuarios (Semana 16) ──────────────────────────────────────────────────

    def guardar_usuarios(self):
        datos = [
            {
                "identificacion": usuario.identificacion,
                "nombre": usuario.nombre,
                "usuario": usuario.usuario,
                "contrasena": usuario.contrasena,
                "rol": usuario.rol,
            }
            for usuario in self.usuarios
        ]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def buscar_usuario_por_identificacion(self, identificacion):
        identificacion = identificacion.strip()
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion:
                return usuario
        return None

    def buscar_usuario_por_nombre_usuario(self, nombre_usuario):
        nombre_usuario = nombre_usuario.strip()
        for usuario in self.usuarios:
            if usuario.usuario == nombre_usuario:
                return usuario
        return None

    def registrar_usuario(self, identificacion, nombre, usuario, contrasena, rol):
        nuevo = Usuario(identificacion, nombre, usuario, contrasena, rol)

        if nuevo.rol == "Administrador":
            raise ValueError(
                "No se pueden registrar nuevos administradores desde esta pantalla."
            )
        if self.buscar_usuario_por_identificacion(nuevo.identificacion) is not None:
            raise ValueError("Ya existe un usuario con esa identificacion.")
        if self.buscar_usuario_por_nombre_usuario(nuevo.usuario) is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")

        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(
        self,
        identificacion,
        nombre,
        usuario,
        contrasena,
        rol,
        identificacion_usuario_actual=None,
    ):
        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        validado = Usuario(identificacion, nombre, usuario, contrasena, rol)

        usuario_con_mismo_login = self.buscar_usuario_por_nombre_usuario(validado.usuario)
        if (
            usuario_con_mismo_login is not None
            and usuario_con_mismo_login.identificacion != usuario_actual.identificacion
        ):
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        if (
            identificacion_usuario_actual == usuario_actual.identificacion
            and usuario_actual.rol == "Administrador"
            and validado.rol != "Administrador"
        ):
            raise ValueError("No puede cambiar el rol del administrador actual.")

        usuario_actual.nombre = validado.nombre
        usuario_actual.usuario = validado.usuario
        usuario_actual.contrasena = validado.contrasena
        usuario_actual.rol = validado.rol
        self.guardar_usuarios()
        return usuario_actual

    def eliminar_usuario(self, identificacion, identificacion_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificacion(identificacion)
        if usuario_actual is None:
            raise ValueError("No existe un usuario con esa identificacion.")
        if usuario_actual.identificacion == identificacion_usuario_actual:
            raise ValueError("No puede eliminar el usuario actualmente autenticado.")

        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual

    # ── Ventas ────────────────────────────────────────────────────────────────

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def guardar_ventas(self):
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_codigo": venta.producto_codigo,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)

    def registrar_venta(self, usuario_id, producto_codigo):
        # Semana 15: valida y registra la venta delegando desde el callback.
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario_por_identificacion(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        if self.buscar_producto_por_codigo(producto_codigo) is None:
            raise ValueError("El producto seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta