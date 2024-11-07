import sqlite3
from sqlite3 import Error

def crear_tabla_reserva(conn):
    try:
        cursor = conn.cursor()
        sql_crear_tabla_reservas = """
        CREATE TABLE IF NOT EXISTS Reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_cancha INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Por Confirmar',  -- 'Por Confirmar' o 'Confirmada'
            FOREIGN KEY (id_usuario) REFERENCES Usuarios (id_usuario),
            FOREIGN KEY (id_cancha) REFERENCES Canchas (id_cancha)
        );
        """
        cursor.execute(sql_crear_tabla_reservas)
        print("Tabla 'Reservas' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")


def insertar_reserva(conn, id_usuario, id_cancha, fecha, hora, estado='Por Confirmar'):
    try:
        cursor = conn.cursor()
        sql_insertar_reserva = """
        INSERT INTO Reservas (id_usuario, id_cancha, fecha, hora, estado)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_insertar_reserva, (id_usuario, id_cancha, fecha, hora, estado))
        conn.commit()
        print("Reserva insertada exitosamente.")
    except Error as e:
        print(f"Error al insertar reserva: {e}")

def obtener_todas_las_reservas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id_reserva, u.nombre AS usuario, c.nombre AS cancha, r.fecha, r.hora, r.estado
        FROM Reservas r
        JOIN Usuarios u ON r.id_usuario = u.id_usuario
        JOIN Canchas c ON r.id_cancha = c.id_cancha
    """)
    return cursor.fetchall()

def obtener_reserva_por_id(conn, id_reserva):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Reservas WHERE id_reserva = ?
    """, (id_reserva,))
    return cursor.fetchone()

def actualizar_estado_reserva(conn, id_reserva, nuevo_estado):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Reservas SET estado = ? WHERE id_reserva = ?
    """, (nuevo_estado, id_reserva))
    conn.commit()

def eliminar_reserva(conn, id_reserva):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reservas WHERE id_reserva = ?", (id_reserva,))
    conn.commit()

def obtener_reservas(conn):
    query = """
        SELECT reservas.id_reserva, canchas.nombre AS cancha_nombre, reservas.fecha, 
               reservas.hora, reservas.estado
        FROM reservas
        JOIN canchas ON reservas.id_cancha = canchas.id_cancha
    """
    cursor = conn.cursor()
    cursor.execute(query)
    reservas = cursor.fetchall()
    print("Reservas obtenidas:", reservas)
    return reservas