import sqlite3

# Inicializa la base de datos
def init_db():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            descripcion TEXT,
            estado INTEGER NOT NULL DEFAULT 1 
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            tipo_documento TEXT,
            num_documento TEXT,
            direccion TEXT,
            telefono TEXT,
            email TEXT NOT NULL,
            clave TEXT NOT NULL,
            activo TEXT NOT NULL,
            FOREIGN KEY(rol_id) REFERENCES rol(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            dni TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            total REAL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    """)
    conn.commit()
    conn.close()
    
# Agrega un producto a la base de datos
def agregar_producto(nombre, precio, stock):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                   (nombre, precio, stock))
    conn.commit()
    conn.close()

# Devuelve todos los productos
def obtener_productos():
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# Registra una venta
def registrar_venta(producto_id, cantidad):
    conn = sqlite3.connect("ventas.db")
    cursor = conn.cursor()

    # Obtiene el producto y verifica stock
    cursor.execute("SELECT precio, stock FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()
    if producto:
        precio, stock = producto
        if cantidad <= stock:
            total = precio * cantidad
            cursor.execute("INSERT INTO ventas (producto_id, cantidad, total) VALUES (?, ?, ?)",
                           (producto_id, cantidad, total))
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?",
                           (cantidad, producto_id))
            conn.commit()
            conn.close()
            return f"Venta registrada: total = S/ {total:.2f}"
        else:
            conn.close()
            return "Stock insuficiente"
    conn.close()
    return "Producto no encontrado"