import sqlite3

def controller_registrar_rol(nombre, descripcion, estado):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO roles (nombre, descripcion, estado) VALUES (?, ?, ?)",
                   (nombre, descripcion, estado))
    conn.commit()
    conn.close()

def controller_obtener_rol():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, descripcion, estado FROM roles")
    return cursor.fetchall()

def controller_actualizar_rol(nombre, descripcion, estado):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE roles
        SET descripcion = ?, estado = ?
        WHERE nombre = ?
    """, (descripcion, estado, nombre))
    conn.commit()
    conn.close()
    
def controller_eliminar_rol(id):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM roles WHERE id = ?", (id))
    conn.commit()
    conn.close()

def controller_buscar_rol(nombre, id):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("""
                SELECT id, nombre, descripcion, estado FROM roles
                WHERE LOWER(nombre) LIKE ? OR id LIKE ?
            """, (f"%{nombre}%", f"%{id}%"))
    return cursor.fetchall()