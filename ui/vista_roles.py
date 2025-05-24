import flet as ft
import re
from controllers.roles_controller import*
def vista_roles(page: ft.Page):
    # texto informativo de lo que esta ocurriendo en la aplicacion 
    mensaje = ft.Text(size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE) 
    lista_de_roles = ft.ListView(expand=True, spacing=2)
    # Variables para modo edición
    modo_edicion = {"activo": False, "rol": None}

    def poner_encabezdo():
        return ft.Row(
            controls=[
                ft.Text("Rol", width=200, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Descripcion", width=100, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Estado", width=100, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Acciones", width=100, weight=ft.FontWeight.BOLD, size=18),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    
    # Inputs de clientes
    nombre_rol =  ft.TextField(label="Rol",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)
    descripcion_rol =  ft.TextField(label="Descripcion",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)
    estado_rol =  ft.TextField(label="Estado",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)

    def cargar_datos():
        registros_roles = controller_obtener_rol()
        registros = []
        for id, rol, desc, estado in registros_roles:
            fila = ft.Row(
                controls=[
                    ft.Text(rol, width=200),
                    ft.Text(desc, width=100),
                    ft.Text(estado, width=100),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT, 
                                width=45, 
                                on_click=lambda e, r=rol, d=desc, es=estado: on_editar_rol(r, d, es)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE, 
                                width=45, 
                                on_click=lambda e, r=rol: on_eliminar_rol(r)
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
            registros.append(fila)
        return registros
    
    def on_eliminar_rol(id):
        def confirmar_eliminacion(e):
            try:
                controller_eliminar_rol(id)
                mensaje.value = "Rol eliminado."
            except Exception as ex:
                mensaje.value = f"Error al eliminar rol: {ex}"
            # Actualiza la lista después de eliminar
            lista_de_roles.controls.clear()
            lista_de_roles.controls.extend(cargar_datos())
            lista_de_roles.update()
            dialogo.open = False
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar rol"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el rol con ID {id}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialogo.close()),
                ft.TextButton("Eliminar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        #page.update()
    def limpiar_campos(e):
        nombre_rol.value = descripcion_rol.value = estado_rol.value = ""
        modo_edicion["activo"] = False
        modo_edicion["rol"] = None
        boton_registrar.text = "REGISTRAR"
        mensaje.value = "Operacion cancelada"
        page.update()

    def on_editar_rol(rol, desc, estado):
        nombre_rol.value = rol
        descripcion_rol.value = desc
        estado_rol.value = estado
        modo_edicion["activo"] = True
        modo_edicion["rol"] = rol
        mensaje.value = "Editando rol..."
        boton_registrar.text = "ACTUALIZAR"
        boton_registrar.update()
        page.update()
        
    def on_registrar_rol(e):
        # Validar que el nombre no esté vacío
        if not nombre_rol.value.strip():
            mensaje.value = "El nombre no puede estar vacío."
            page.update()
            return
        # Validar formato de DNI (8 dígitos numéricos)
        """if not re.fullmatch(r"\d{8}", dni_cliente.value):
            mensaje.value = "El DNI debe tener exactamente 8 números."
            page.update()
            return"""

        # Validar formato de teléfono (7 a 15 dígitos numéricos)
        '''if not re.fullmatch(r"\d{7,15}", tel_cliente.value):
            mensaje.value = "El teléfono debe tener entre 7 y 15 números."
            page.update()
            return'''
        # Validar que el nombre del rol no se repita (solo al registrar, no al editar)
        if not modo_edicion["activo"]:
            conn = sqlite3.connect("ventas.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM roles WHERE nombre = ?", (nombre_rol.value,))
            existe = cursor.fetchone()[0]
            conn.close()
            if existe:
                mensaje.value = "Este rol ya está registrado."
                page.update()
                return

        if modo_edicion["activo"]:
            # Actualizar cliente
            try:
                controller_actualizar_rol(modo_edicion["rol"], descripcion_rol.value, estado_rol.value)
                mensaje.value = "Rol actualizado."
            except Exception as ex:
                mensaje.value = f"Error al actualizar rol: {ex}"
            modo_edicion["activo"] = False
            modo_edicion["rol"] = None
            boton_registrar.text = "REGISTRAR"
            boton_registrar.update()
        else:
            # Registrar cliente nuevo
            try:
                controller_registrar_rol(nombre_rol.value, descripcion_rol.value, estado_rol.value)
                mensaje.value = "Rol Registrado."
            except:
                mensaje.value = "Error al registrar rol."
        nombre_rol.value = descripcion_rol.value = estado_rol.value = ""
        lista_de_roles.controls.clear()
        lista_de_roles.controls.extend(cargar_datos())
        lista_de_roles.update()
        page.update()
    
    # Campo de búsqueda
    campo_busqueda = ft.TextField(
        border_radius=10,
        hint_text="Buscar por rol o id",
        on_submit=lambda e: buscar_roles(),
        expand=True,
        color=ft.Colors.BLUE
    )

    def buscar_roles():
        texto = campo_busqueda.value.strip().lower()
        lista_de_roles.controls.clear()
        if texto:
            roles=controller_buscar_rol(texto,texto)
        else:
            roles=controller_obtener_rol()
        for id, rol, desc, estado in roles:
            fila = ft.Row(
                controls=[
                    ft.Text(rol, width=200),
                    ft.Text(desc, width=100),
                    ft.Text(estado, width=100),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT, 
                                width=45, 
                                on_click=lambda e, r=rol, d=desc, es=estado: on_editar_rol(r, d, es)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE, 
                                width=45, 
                                on_click=lambda e, r=rol: on_eliminar_rol(r)
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
            lista_de_roles.controls.append(fila)
        lista_de_roles.update()


    # Crea el botón como variable para poder actualizar su texto
    boton_registrar = ft.FilledButton("REGISTRAR", on_click=on_registrar_rol, expand=True)
    boton_cancelar = ft.FilledButton(text="CANCELAR", bgcolor=ft.Colors.RED, on_click=limpiar_campos, expand=True) 
    # Armamos la vista
    columna_registro = ft.Column(
        controls=[
            mensaje,
            ft.Text("NUEVO ROL", size=22),
            ft.Divider(),
            ft.Row(controls=[nombre_rol]),
            ft.Row(controls=[descripcion_rol]),
            ft.Row(controls=[estado_rol]),
            ft.Row(controls=[boton_registrar]),  # Usa la variable aquí
            ft.Row(controls=[boton_cancelar])
        ],
        expand=1,
    )
    # columna de listado de clientes
    columna_lista = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("LISTA DE ROLES", size=22),
                    ft.Container(expand=True),
                    campo_busqueda,
                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        icon_color=ft.Colors.BLUE,
                        on_click=lambda e: buscar_roles()
                    ),
                ]
            ),
            ft.Divider(),
            poner_encabezdo(),
            ft.Container(content=lista_de_roles, height=400 ,bgcolor=ft.Colors.BLACK45),
            #mensaje
        ],
        expand=4,
    )

    contenedor = ft.Container(
        content=ft.Row(controls=[columna_registro, ft.Container(width=60), columna_lista], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=20,
        bgcolor=ft.Colors.BLACK26,
        border_radius=10,
        border=ft.border.all(3, ft.Colors.BLUE),
    )

    #  Cargar los datos del ListView apenas la página esté renderizada
    lista_de_roles.controls.extend(cargar_datos())
    #lista_de_clientes.update()
    page.update()

    return contenedor
