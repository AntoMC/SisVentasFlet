import flet as ft
import re
from db.bd_ventas import *  # Asegúrate de que esta importación esté correcta
def vista_clientes(page: ft.Page):
    # texto informativo de lo que esta ocurriendo en la aplicacion 
    mensaje = ft.Text(size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE) 
    lista_de_clientes = ft.ListView(expand=True, spacing=2)
    # Variables para modo edición
    modo_edicion = {"activo": False, "dni": None}

    def poner_encabezdo():
        return ft.Row(
            controls=[
                ft.Text("Nombre", width=200, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Dni", width=100, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Telefono", width=100, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Direccion", width=100, weight=ft.FontWeight.BOLD, size=18),
                ft.Text("Acciones", width=100, weight=ft.FontWeight.BOLD, size=18),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    
    # Inputs de clientes
    nombre_cliente =  ft.TextField(label="Nombre",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)
    dni_cliente =  ft.TextField(label="Dni",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)
    tel_cliente =  ft.TextField(label="Telefono",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)
    dir_cliente =  ft.TextField(label="DIreccion",height=50, expand=True, border=ft.InputBorder.UNDERLINE, border_color="gray",text_size=16,content_padding=ft.padding.symmetric(horizontal=8, vertical=5), color=ft.Colors.BLUE)

    def cargar_datos():
        conn = sqlite3.connect("ventas.db")
        cursor = conn.cursor()
        registros_clientes = cursor.execute("""
            SELECT nombre, dni, telefono, direccion
            FROM clientes
        """)
        registros = []
        for nombre, dni, tel, dir in registros_clientes:
            fila = ft.Row(
                controls=[
                    ft.Text(nombre, width=200),
                    ft.Text(dni, width=100),
                    ft.Text(tel, width=100),
                    ft.Text(dir, width=100),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT, 
                                width=45, 
                                on_click=lambda e, n=nombre, d=dni, t=tel, di=dir: on_editar_cliente(n, d, t, di)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE, 
                                width=45, 
                                on_click=lambda e, d=dni: on_eliminar_cliente(d)
                            ),
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
            registros.append(fila)
        return registros
    
    def on_eliminar_cliente(dni):
        def confirmar_eliminacion(e):
            try:
                conn = sqlite3.connect("ventas.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni,))
                conn.commit()
                conn.close()
                mensaje.value = "Cliente eliminado."
            except Exception as ex:
                mensaje.value = f"Error al eliminar cliente: {ex}"
            # Actualiza la lista después de eliminar
            lista_de_clientes.controls.clear()
            lista_de_clientes.controls.extend(cargar_datos())
            lista_de_clientes.update()
            dialogo.open = False
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Eliminar Cliente"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el cliente con DNI {dni}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialogo.close()),
                ft.TextButton("Eliminar", on_click=confirmar_eliminacion),
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        #page.update()

    def on_editar_cliente(nombre, dni, tel, dir):
        nombre_cliente.value = nombre
        dni_cliente.value = dni
        tel_cliente.value = tel
        dir_cliente.value = dir
        modo_edicion["activo"] = True
        modo_edicion["dni"] = dni
        mensaje.value = "Editando cliente..."
        boton_registrar.text = "Actualizar"
        boton_registrar.update()
        page.update()
        
    def on_registrar_cliente(e):
        # Validar que el nombre no esté vacío
        if not nombre_cliente.value.strip():
            mensaje.value = "El nombre no puede estar vacío."
            page.update()
            return
        # Validar formato de DNI (8 dígitos numéricos)
        if not re.fullmatch(r"\d{8}", dni_cliente.value):
            mensaje.value = "El DNI debe tener exactamente 8 números."
            page.update()
            return

        # Validar formato de teléfono (7 a 15 dígitos numéricos)
        '''if not re.fullmatch(r"\d{7,15}", tel_cliente.value):
            mensaje.value = "El teléfono debe tener entre 7 y 15 números."
            page.update()
            return'''
        # Validar que el DNI no se repita (solo al registrar, no al editar)
        if not modo_edicion["activo"]:
            conn = sqlite3.connect("ventas.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE dni = ?", (dni_cliente.value,))
            existe = cursor.fetchone()[0]
            conn.close()
            if existe:
                mensaje.value = "El DNI ya está registrado."
                page.update()
                return

        if modo_edicion["activo"]:
            # Actualizar cliente
            try:
                conn = sqlite3.connect("ventas.db")
                cursor = conn.cursor()
                actualizar_cliente(nombre_cliente.value, modo_edicion["dni"], tel_cliente.value, dir_cliente.value)
                conn.commit()
                conn.close()
                mensaje.value = "Cliente actualizado."
            except Exception as ex:
                mensaje.value = f"Error al actualizar cliente: {ex}"
            modo_edicion["activo"] = False
            modo_edicion["dni"] = None
            boton_registrar.text = "Registrar"
            boton_registrar.update()
        else:
            # Registrar cliente nuevo
            try:
                registrar_cliente(nombre_cliente.value, dni_cliente.value, tel_cliente.value, dir_cliente.value)
                mensaje.value = "Cliente Registrado."
            except:
                mensaje.value = "Error al registrar cliente."
        nombre_cliente.value = dni_cliente.value = tel_cliente.value = dir_cliente.value = ""
        lista_de_clientes.controls.clear()
        lista_de_clientes.controls.extend(cargar_datos())
        lista_de_clientes.update()
        page.update()
    
    # Campo de búsqueda
    campo_busqueda = ft.TextField(
        border_radius=10,
        hint_text="Buscar por nombre o DNI",
        on_submit=lambda e: buscar_clientes(),
        expand=True,
        color=ft.Colors.BLUE
    )

    def buscar_clientes():
        texto = campo_busqueda.value.strip().lower()
        lista_de_clientes.controls.clear()
        conn = sqlite3.connect("ventas.db")
        cursor = conn.cursor()
        if texto:
            cursor.execute("""
                SELECT nombre, dni, telefono, direccion FROM clientes
                WHERE LOWER(nombre) LIKE ? OR dni LIKE ?
            """, (f"%{texto}%", f"%{texto}%"))
        else:
            cursor.execute("SELECT nombre, dni, telefono, direccion FROM clientes")
        for nombre, dni, tel, dir in cursor.fetchall():
            fila = ft.Row(
                controls=[
                    ft.Text(nombre, width=200),
                    ft.Text(dni, width=100),
                    ft.Text(tel, width=100),
                    ft.Text(dir, width=100),
                    ft.IconButton(
                        icon=ft.Icons.EDIT, 
                        width=100, 
                        on_click=lambda e, n=nombre, d=dni, t=tel, di=dir: on_editar_cliente(n, d, t, di)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND
            )
            lista_de_clientes.controls.append(fila)
        conn.close()
        lista_de_clientes.update()


    # Crea el botón como variable para poder actualizar su texto
    boton_registrar = ft.FilledButton("REGISTRAR", on_click=on_registrar_cliente, expand=True,)

    # Armamos la vista
    columna_registro = ft.Column(
        controls=[
            mensaje,
            ft.Text("NUEVO CLIENTE", size=22),
            ft.Divider(),
            ft.Row(controls=[nombre_cliente]),
            ft.Row(controls=[dni_cliente]),
            ft.Row(controls=[tel_cliente]),
            ft.Row(controls=[dir_cliente]),
            ft.Row(controls=[boton_registrar])  # Usa la variable aquí
        ],
        expand=1,
    )
    # columna de listado de clientes
    columna_lista = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("LISTA DE CLIENTES", size=22),
                    ft.Container(expand=True),
                    campo_busqueda,
                    ft.IconButton(
                        icon=ft.Icons.SEARCH,
                        icon_color=ft.Colors.BLUE,
                        on_click=lambda e: buscar_clientes()
                    ),
                ]
            ),
            ft.Divider(),
            poner_encabezdo(),
            ft.Container(content=lista_de_clientes, height=400 ,bgcolor=ft.Colors.BLACK45),
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
    lista_de_clientes.controls.extend(cargar_datos())
    #lista_de_clientes.update()
    page.update()

    return contenedor
