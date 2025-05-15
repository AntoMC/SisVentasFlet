import sqlite3
from db.bd_ventas import registrar_cliente

def obtener_clientes():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, dni, telefono, direccion FROM clientes")
    return cursor.fetchall()

def registrar_nuevo_cliente(nombre, dni, telefono, direccion):
    registrar_cliente(nombre, dni, telefono, direccion)
