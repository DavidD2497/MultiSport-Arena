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
            FOREIGN KEY (id_usuario) REFERENCES Usuarios (id_usuario),
            FOREIGN KEY (id_cancha) REFERENCES Canchas (id_cancha)
        );
        """
        cursor.execute(sql_crear_tabla_reservas)
        print("Tabla 'Reservas' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_reserva(conn, id_usuario, id_cancha, fecha, hora):
    try:
        cursor = conn.cursor()
        sql_insertar_reserva = """
        INSERT INTO Reservas (id_usuario, id_cancha, fecha, hora)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql_insertar_reserva, (id_usuario, id_cancha, fecha, hora))
        conn.commit()
        print("Reserva insertada exitosamente.")
    except Error as e:
        print(f"Error al insertar reserva: {e}")

def obtener_todas_las_reservas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id_reserva, u.nombre AS usuario, c.nombre AS cancha, r.fecha, r.hora
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

def eliminar_reserva(conn, id_reserva):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reservas WHERE id_reserva = ?", (id_reserva,))
    conn.commit()

def obtener_reservas(conn, fecha):
    query = """
        SELECT id_cancha, hora
        FROM Reservas
        WHERE fecha = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (fecha,))
    reservas = cursor.fetchall()
    print("Reservas obtenidas:", reservas)
    return reservas

def obtener_reservas_por_usuario(conn, id_usuario):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id_reserva, c.nombre AS cancha, r.fecha, r.hora
        FROM Reservas r
        JOIN Canchas c ON r.id_cancha = c.id_cancha
        WHERE r.id_usuario = ?
    """, (id_usuario,))
    return cursor.fetchall()
