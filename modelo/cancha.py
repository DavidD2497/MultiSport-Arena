import sqlite3
from sqlite3 import Error

def crear_tabla_cancha(conn):
    try:
        cursor = conn.cursor()
        sql_crear_tabla_canchas = """
        CREATE TABLE IF NOT EXISTS Canchas (
            id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nombre TEXT NOT NULL
        );
        """
        cursor.execute(sql_crear_tabla_canchas)
        print("Tabla 'Canchas' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_cancha(conn, tipo, nombre):
    try:
        cursor = conn.cursor()
        sql_insertar_cancha = """
        INSERT INTO Canchas (tipo, nombre)
        VALUES (?, ?)
        """
        cursor.execute(sql_insertar_cancha, (tipo, nombre))
        conn.commit()
        print("Cancha insertada exitosamente.")
    except Error as e:
        print(f"Error al insertar cancha: {e}")
