import pyodbc
import config
from datetime import datetime

def get_conn():
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={config.SQL_SERVER};"
        f"DATABASE={config.SQL_DATABASE};"
        f"UID={config.SQL_USER};"
        f"PWD={config.SQL_PASSWORD};"
        f"Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)

# ── Guardar conversación ──
def guardar_conversacion(usuario, mensaje, intencion, confianza, respuesta):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Conversaciones
            (usuario, mensaje, intencion, confianza, respuesta)
        VALUES (?, ?, ?, ?, ?)
    """, usuario, mensaje, intencion, confianza, respuesta)
    conn.commit()
    conn.close()

# ── Obtener menú ──
def obtener_menu(categoria=None):
    conn = get_conn()
    cursor = conn.cursor()
    if categoria:
        cursor.execute("""
            SELECT nombre, precio FROM Platos
            WHERE disponible=1
            AND LOWER(categoria) LIKE LOWER(?)
        """, f"%{categoria}%")
    else:
        cursor.execute("""
            SELECT categoria, nombre, precio
            FROM Platos WHERE disponible=1
            ORDER BY categoria
        """)
    filas = cursor.fetchall()
    conn.close()
    return filas

# ── Crear reserva ──
def crear_reserva(nombre, fecha, hora, num_personas):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Reservas
            (nombre_cliente, fecha, hora, num_personas)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?)
    """, nombre, fecha, hora, num_personas)
    id_reserva = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_reserva

# ── Crear pedido ──
def crear_pedido(nombre, detalle):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Pedidos (nombre_cliente, detalle)
        OUTPUT INSERTED.id
        VALUES (?, ?)
    """, nombre, detalle)
    id_pedido = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id_pedido

# ── Estado pedido ──
def estado_pedido(id_pedido=None, nombre=None):
    conn = get_conn()
    cursor = conn.cursor()
    if id_pedido:
        cursor.execute("""
            SELECT id, detalle, estado, fecha_hora
            FROM Pedidos WHERE id=?
        """, id_pedido)
    else:
        cursor.execute("""
            SELECT TOP 1 id, detalle, estado, fecha_hora
            FROM Pedidos
            WHERE nombre_cliente=?
            ORDER BY fecha_hora DESC
        """, nombre)
    fila = cursor.fetchone()
    conn.close()
    return fila

# ── Historial por fechas ──
def historial(fecha_inicio, fecha_fin):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT usuario, mensaje, intencion, respuesta, fecha_hora
        FROM Conversaciones
        WHERE fecha_hora BETWEEN ? AND ?
        ORDER BY fecha_hora DESC
    """, fecha_inicio, fecha_fin)
    filas = cursor.fetchall()
    conn.close()
    return filas

# ── Estadísticas ──
def estadisticas():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT intencion, COUNT(*) as total
        FROM Conversaciones
        GROUP BY intencion
        ORDER BY total DESC
    """)
    filas = cursor.fetchall()
    conn.close()
    return filas