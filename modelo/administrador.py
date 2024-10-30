import sqlite3
from sqlite3 import Error

def crear_tabla_administrador(conn):
    try:
        cursor = conn.cursor()
        sql_crear_tabla_administradores = """
        CREATE TABLE IF NOT EXISTS Administradores (
            id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        );
        """
        cursor.execute(sql_crear_tabla_administradores)
        print("Tabla 'Administradores' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_administrador(conn, nombre, email, contraseña):
    try:
        cursor = conn.cursor()
        sql_insertar_administrador = """
        INSERT INTO Administradores (nombre, email, contraseña)
        VALUES (?, ?, ?)
        """
        cursor.execute(sql_insertar_administrador, (nombre, email, contraseña))
        conn.commit()
        print("Administrador insertado exitosamente.")
    except Error as e:
        print(f"Error al insertar administrador: {e}")

