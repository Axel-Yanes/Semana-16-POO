# Sistema de Gestión de Restaurante — Semana 16

## Nombre del estudiante
Axel Dilan Yanes Urbano

## Propósito de la Semana 16
Evolución de restaurante_app aplicando el manejo de eventos en Tkinter en una situación real del sistema: la gestión de usuarios. La sección Usuarios pasa de ser una tabla de consulta a un CRUD completo (registrar, consultar, actualizar y eliminar) con formulario y Treeview, usando los eventos `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>` mediante `bind()`, y los botones mediante `command=`. Se incorpora el atributo `rol` al modelo `Usuario` y los cambios se persisten en `usuarios.json`.

## Evolución del proyecto

| Semana | Enfoque principal |
|--------|-------------------|
| Semana 13 | Primera interfaz gráfica con Tkinter. Login, visualización de productos y usuarios. Ventas pendiente. |
| Semana 14 | Mejora visual con componentes y contenedores. Panel lateral, formularios, tablas Treeview y CRUD completo de productos. |
| Semana 15 | Manejo de eventos con `command=`. Nueva sección Ventas, callbacks, persistencia en `ventas.json`. |
| Semana 16 | Manejo de eventos con `bind()`. Gestión de usuarios con roles, Treeview, atajos de teclado y evento del Combobox. |

El proyecto nunca fue reconstruido desde cero. La Semana 16 conserva el inicio de sesión, la navegación, la gestión de productos, las ventas, la persistencia y los recursos de `assets/`.

### Cambios realizados en la Semana 16

- `modelos/usuario.py`: nuevo atributo `rol` con validación (`Administrador`, `Empleado`, `Cliente`).
- `datos/usuarios.json`: cada usuario guarda su rol.
- `servicios/restaurante_servicio.py`: nuevos métodos para registrar, actualizar, eliminar y guardar usuarios, con sus validaciones.
- `ui/main_view.py`: la sección Usuarios ahora tiene formulario, botones, Treeview y eventos. El menú Usuarios solo se muestra al Administrador.

## Estructura del proyecto
```
restaurante_app/
├── assets/
│   ├── icons/
│   │   ├── home.png
│   │   ├── users.png
│   │   ├── products.png
│   │   ├── sales.png
│   │   ├── logout.png
│   │   ├── add.png
│   │   ├── edit.png
│   │   ├── delete.png
│   │   ├── search.png
│   │   └── clean.png
│   └── logo/
│       ├── logo.png
│       └── icono.png
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

## Descripción de cada capa

**`modelos/`**: define las clases `Producto`, `Usuario` y `Venta` con propiedades y validaciones mediante setters. `Usuario` incluye el rol y valida que sea uno de los roles permitidos.

**`servicios/`**: contiene `ArchivoServicio` para lectura y escritura de JSON, y `RestauranteServicio` con la lógica de negocio: autenticación, CRUD de productos, CRUD de usuarios, registro de ventas y persistencia. La interfaz no accede directamente a los archivos JSON.

**`datos/`**: almacena la información en `productos.json`, `usuarios.json` y `ventas.json`.

**`ui/`**: contiene `LoginView` para la autenticación y `MainView` para la interfaz principal con navegación lateral, formularios y tablas.

**`assets/`**: íconos PNG para el menú y los botones, y el logo del sistema.

## Gestión de usuarios

Solo el Administrador ve la sección Usuarios en el menú. Desde ahí puede:

- **Registrar** usuarios de tipo Empleado o Cliente.
- **Consultar** los usuarios en un Treeview con identificación, nombre, usuario y rol (la contraseña no se muestra en la tabla).
- **Actualizar** los datos del usuario seleccionado.
- **Eliminar** el usuario seleccionado, con confirmación previa.
- **Limpiar** el formulario.

Las validaciones están en `RestauranteServicio`:

- No se repite la identificación ni el nombre de usuario.
- No se registran nuevos administradores desde esta pantalla.
- No se puede eliminar la cuenta que tiene la sesión iniciada.
- El administrador actual no puede cambiar su propio rol.

## Roles utilizados

| Rol | Acceso |
|-----|--------|
| Administrador | Accede a la gestión de usuarios y al resto del sistema. |
| Empleado | Accede a Inicio, Productos y Ventas. No ve la gestión de usuarios. |
| Cliente | Accede a Inicio, Productos y Ventas. No ve la gestión de usuarios. |

El Administrador gestiona usuarios Empleado y Cliente. No se implementó un sistema complejo de permisos.

## Eventos implementados

| Evento | Asociado con | Callback | Función |
|--------|--------------|----------|---------|
| `<<TreeviewSelect>>` | `bind()` en la tabla de usuarios | `al_seleccionar_usuario` | Toma la identificación de la fila seleccionada, busca el usuario en `RestauranteServicio` y carga sus datos en el formulario. |
| `<Return>` | `bind()` en los campos del formulario | `al_presionar_enter` | Ejecuta `registrar_usuario()`. |
| `<Escape>` | `bind()` en los campos y en la tabla | `al_presionar_escape` | Ejecuta `limpiar_formulario_usuario()`: limpia el formulario y quita la selección. |
| `<<ComboboxSelected>>` | `bind()` en el Combobox de rol | `al_seleccionar_rol` | Actualiza el texto "Rol seleccionado". |

## Uso de bind(), command= y callbacks

- **`bind()`**: asocia un evento (una selección, una tecla, un cambio de opción) con una función. La función recibe el parámetro `event`.
- **`command=`**: se usa en los botones Registrar, Actualizar, Eliminar y Limpiar. Ejecuta su función al hacer clic.
- **Callback**: es la función que se ejecuta cuando ocurre el evento o el clic. Coordina la interfaz y delega en el servicio.

Los callbacks de `<Return>` y `<Escape>` no repiten código: reutilizan `registrar_usuario()` y `limpiar_formulario_usuario()`, los mismos métodos que usan los botones.

## Flujo de manejo de eventos

```
Selección de una fila en el Treeview
      ↓
<<TreeviewSelect>>
      ↓
bind() → al_seleccionar_usuario(event)
      ↓
Obtiene la identificación de la fila
      ↓
RestauranteServicio.buscar_usuario_por_identificacion()
      ↓
Carga los datos en el formulario
      ↓
Actualizar / Eliminar / Limpiar (command=)
      ↓
RestauranteServicio valida y guarda en usuarios.json
      ↓
refrescar_usuarios() actualiza el Treeview
      ↓
messagebox muestra la respuesta al usuario
```

## Persistencia mediante usuarios.json

Cada usuario se guarda con identificación, nombre, usuario, contraseña y rol. Después de registrar, actualizar o eliminar, `RestauranteServicio.guardar_usuarios()` escribe el archivo mediante `ArchivoServicio`. Al cerrar y volver a ejecutar la aplicación, los usuarios se recuperan desde `usuarios.json`.

```
datos/usuarios.json   → CRUD de usuarios con rol, guardado después de cada operación
datos/productos.json  → CRUD de productos
datos/ventas.json     → registro de ventas
```

Ninguna vista accede directamente a los archivos JSON.

## Credenciales de demostración

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin   | 1234       | Administrador |
| cajero  | abcd       | Empleado |

## Pasos para ejecutar main.py

1. Abrir una terminal en Windows.
2. Navegar hasta la carpeta del proyecto:
```
cd "C:\Users\Usuario\OneDrive\Documentos\Clase Semana 16 POO\restaurante_app"
```
3. Ejecutar con:
```
py main.py
```
   O si `python` está disponible:
```
python main.py
```
4. Ingresar las credenciales en el login.
5. Con `admin` se accede a Inicio, Usuarios, Productos y Ventas. Con `cajero` no aparece Usuarios.