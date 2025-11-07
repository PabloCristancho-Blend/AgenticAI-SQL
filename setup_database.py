import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

def crear_base_datos():
    """Crea la base de datos de ventas."""
    Path("data").mkdir(exist_ok=True)
    conn = sqlite3.connect("data/ventas.db")
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendedor TEXT NOT NULL,
        sede TEXT NOT NULL,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        fecha DATE NOT NULL
    )
    ''')
    
    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM ventas")
    if cursor.fetchone()[0] > 0:
        print("✓ La base de datos ya tiene datos")
        conn.close()
        return
    
    # Datos de ejemplo
    vendedores = ["Carlos Ruiz", "María López", "Juan Pérez", "Ana García", 
                  "Luis Martínez", "Sofia Torres", "Pedro Ramírez", "Laura Fernández"]
    sedes = ["Bogotá", "Medellín", "Cali", "Barranquilla"]
    productos = ["Laptop Dell", "Mouse Logitech", "Teclado Mecánico", "Monitor Samsung", 
                 "Audífonos Sony", "Webcam HD", "SSD 1TB", "RAM 16GB", "Impresora HP", "Router TP-Link"]
    
    fecha_inicio = datetime.now() - timedelta(days=180)
    datos = []
    
    for _ in range(500):
        vendedor = random.choice(vendedores)
        sede = random.choice(sedes)
        producto = random.choice(productos)
        cantidad = random.randint(1, 20)
        precio = round(random.uniform(50000, 2500000), 2)
        fecha = fecha_inicio + timedelta(days=random.randint(0, 180))
        datos.append((vendedor, sede, producto, cantidad, precio, fecha.strftime("%Y-%m-%d")))
    
    cursor.executemany('''
    INSERT INTO ventas (vendedor, sede, producto, cantidad, precio, fecha)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', datos)
    
    conn.commit()
    conn.close()
    print("✅ Base de datos creada con 500 registros")

if __name__ == "__main__":
    crear_base_datos()