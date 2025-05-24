import flet as ft
from db.bd_ventas import *
from ui.vista_clientes import vista_clientes  # Importamos la vista de clientes
from ui.vista_roles import vista_roles  # Importamos la vista de roles

def main(page: ft.Page):
    page.title = "Dashboard con NavigationDrawer"
    page.theme_mode = "dark"
    #page.window_width = 800
    #page.window_height = 600

    # Crear el NavigationDrawer
    drawer = ft.NavigationDrawer(
        selected_index=0,
        controls=[
            ft.NavigationDrawerDestination(icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationDrawerDestination(icon=ft.Icons.VERIFIED_USER, label="Roles"),
            ft.NavigationDrawerDestination(icon=ft.Icons.ANALYTICS, label="Reportes"),
            ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS, label="Configuración"),
        ],
    )

    # Función para manejar la navegación
    def on_drawer_change(e):
        routes = ["/", 
                  "/roles", "/reportes", "/configuracion"]
        selected = drawer.selected_index
        drawer.open = False
        page.go(routes[selected])

    drawer.on_change = on_drawer_change

    # Función para abrir el drawer
    def open_drawer(e):
        drawer.open = True
        page.update()

    # Función para manejar el cambio de ruta
    def route_change(e):
        content = vista_clientes(page)
        if page.route == "/roles":
            content = vista_roles(page)
            
        if page.route == "/reportes":
            content = ft.Text(f"Estás en la ruta: {page.route}", size=25)
           
        elif page.route == "/configuracion":
            content = ft.Text("Vista de Configuración", size=25)

        # Crear la vista con el drawer asignado
        view = ft.View(
            route=page.route,
            controls=[
                ft.AppBar(
                    title=ft.Text("Dashboard"),
                    leading=ft.IconButton(ft.Icons.MENU, on_click=open_drawer),
                    #bgcolor=ft.colors.BLUE,
                ),
                content,
            ],
            drawer=drawer,
            
        )

        page.views.clear()
        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
init_db()
ft.app(target=main)