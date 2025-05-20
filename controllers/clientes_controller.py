import sqlite3

def controller_registrar_cliente(nombre, dni, telefono, direccion):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, dni, telefono, direccion) VALUES (?, ?, ?, ?)",
                   (nombre, dni, telefono, direccion))
    conn.commit()
    conn.close()

def controller_obtener_clientes():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, dni, telefono, direccion FROM clientes")
    return cursor.fetchall()

def controller_actualizar_cliente(nombre, dni, telefono, direccion):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, telefono = ?, direccion = ?
        WHERE dni = ?
    """, (nombre, telefono, direccion, dni))
    conn.commit()
    conn.close()
    
def controller_eliminar_cliente(dni):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE dni = ?", (dni))
    conn.commit()
    conn.close()

def controller_buscar_cliente(nombre, dni):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("""
                SELECT nombre, dni, telefono, direccion FROM clientes
                WHERE LOWER(nombre) LIKE ? OR dni LIKE ?
            """, (f"%{nombre}%", f"%{dni}%"))
    return cursor.fetchall()