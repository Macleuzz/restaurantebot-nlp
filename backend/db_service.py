import pyodbc
import config
from datetime import datetime, timedelta

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
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Conversaciones
                (usuario, mensaje, intencion, confianza, respuesta)
            VALUES (?, ?, ?, ?, ?)
        """, usuario, mensaje, intencion, float(confianza), respuesta)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error guardando conversación: {e}")

# ── Obtener menú ──
def obtener_menu(categoria=None):
    try:
        conn   = get_conn()
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
    except Exception as e:
        print(f"Error obteniendo menú: {e}")
        return []

# ── Crear reserva ──
def crear_reserva(nombre, fecha, hora, num_personas):
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reservas
                (nombre_cliente, fecha, hora, num_personas)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?)
        """, nombre, str(fecha), str(hora), str(num_personas))
        id_reserva = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_reserva
    except Exception as e:
        print(f"Error creando reserva: {e}")
        return 0

# ── Crear pedido ──
def crear_pedido(nombre, detalle):
    try:
        conn   = get_conn()
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
    except Exception as e:
        print(f"Error creando pedido: {e}")
        return 0

# ── Estado pedido ──
def estado_pedido(id_pedido=None, nombre=None):
    try:
        conn   = get_conn()
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
    except Exception as e:
        print(f"Error obteniendo estado pedido: {e}")
        return None

# ── Historial por fechas ──
def historial(fecha_inicio, fecha_fin):
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT usuario, mensaje, intencion, respuesta, fecha_hora
            FROM Conversaciones
            ORDER BY fecha_hora DESC
        """)
        filas = cursor.fetchall()
        conn.close()

        resultado = []
        for f in filas:
            try:
                fecha_utc  = f[4]
                fecha_peru = fecha_utc - timedelta(hours=5)
                fecha_str  = fecha_peru.strftime("%d/%m/%Y %H:%M")
            except:
                fecha_str = str(f[4])

            resultado.append({
                "usuario":    str(f[0]) if f[0] else "Cliente",
                "mensaje":    str(f[1]) if f[1] else "",
                "intencion":  str(f[2]) if f[2] else "—",
                "respuesta":  str(f[3]) if f[3] else "",
                "fecha_hora": fecha_str
            })
        return resultado

    except Exception as e:
        print(f"Error obteniendo historial: {e}")
        return []
# ── Estadísticas ──
def estadisticas():
    try:
        conn   = get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT intencion, COUNT(*) as total
            FROM Conversaciones
            WHERE intencion IS NOT NULL
            AND intencion != 'None'
            GROUP BY intencion
            ORDER BY total DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return []