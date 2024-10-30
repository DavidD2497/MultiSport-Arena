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

