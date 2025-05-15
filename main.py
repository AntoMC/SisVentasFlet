import flet as ft
import sqlite3
from db.bd_ventas import *

# Interfaz Flet
def main(page: ft.Page):
    page.title = "Sistema de Ventas"
    page.scroll = "auto"

    # Inputs de productos
    nombre = ft.TextField(label="Nombre")
    precio = ft.TextField(label="Precio", keyboard_type="number")
    stock = ft.TextField(label="Stock", keyboard_type="number")

    nombre_cliente=ft.TextField(hint_text="Nombre")
    dni_cliente=ft.TextField(hint_text="Dni")
    tel_cliente=ft.TextField(hint_text="Telefono")
    dir_cliente=ft.TextField(hint_text="Direccion")

    # Inputs de venta
    producto_dropdown = ft.Dropdown(label="Producto", options=[])
    cantidad_input = ft.TextField(label="Cantidad", keyboard_type="number")

    mensaje = ft.Text()

    def actualizar_dropdown():
        producto_dropdown.options.clear()
        for p in obtener_productos():
            producto_dropdown.options.append(ft.dropdown.Option(str(p[0]), p[1]))
        page.update()
    def on_registrar_cliente(e):
        try:
            registrar_cliente(nombre_cliente.value, dni_cliente.value, tel_cliente.value, dir_cliente.value )
            mensaje.value = "Cliente Registrado."
            nombre_cliente.value = dni_cliente.value = tel_cliente.value = dir_cliente.value = ""
            #actualizar_tabla_clientes()
        except :
            mensaje.value = "Error al registrar cliente."
        page.update()
    def on_agregar_producto(e):
        try:
            agregar_producto(nombre.value, float(precio.value), int(stock.value))
            mensaje.value = "Producto agregado."
            nombre.value = precio.value = stock.value = ""
            actualizar_dropdown()
        except:
            mensaje.value = "Error al agregar producto."
        page.update()

    def on_realizar_venta(e):
        try:
            producto_id = int(producto_dropdown.value)
            cantidad = int(cantidad_input.value)
            resultado = registrar_venta(producto_id, cantidad)
            mensaje.value = resultado
            cantidad_input.value = ""
            actualizar_tabla_ventas()
            actualizar_dropdown()
        except:
            mensaje.value = "Error en la venta."
        page.update()

    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Fecha"))
        ],
        rows=[]
    )

    def actualizar_tabla_ventas():
        tabla_ventas.rows.clear()
        conn = sqlite3.connect("ventas.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT productos.nombre, ventas.cantidad, ventas.total, ventas.fecha
            FROM ventas
            JOIN productos ON productos.id = ventas.producto_id
            ORDER BY ventas.fecha DESC
        """)
        for venta in cursor.fetchall():
            tabla_ventas.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(col))) for col in venta])
            )
        conn.close()
        page.update()

    actualizar_dropdown()
    actualizar_tabla_ventas()

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Agregar Producto", size=20),
                        nombre, precio, stock,
                        ft.ElevatedButton("Agregar", on_click=on_agregar_producto),
                    ]
                ),
                 ft.Column(
                    controls=[
                        ft.Text("Agregar cliente", size=20),
                        nombre_cliente, dni_cliente, tel_cliente, dir_cliente,
                        ft.ElevatedButton("Registrar", on_click=on_registrar_cliente),
                    ]
                )
            ]
        ),
        

        ft.Divider(),

        ft.Text("Registrar Venta", size=20),
        producto_dropdown, cantidad_input,
        ft.ElevatedButton("Vender", on_click=on_realizar_venta),

        ft.Divider(),

        mensaje,

        ft.Text("Historial de Ventas", size=20),
        tabla_ventas
    )

if __name__ == "__main__":
    init_db()
    ft.app(target=main)