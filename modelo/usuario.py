import sqlite3
from sqlite3 import Error

def crear_tabla_usuario(conn):
    try:
        cursor = conn.cursor()
        sql_crear_tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        );
        """
        cursor.execute(sql_crear_tabla_usuarios)
        print("Tabla 'Usuarios' creada exitosamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_usuario(conn, nombre, email, contraseña):
    try:
        cursor = conn.cursor()
        sql_insertar_usuario = """
        INSERT INTO Usuarios (nombre, email, contraseña)
        VALUES (?, ?, ?)
        """
        cursor.execute(sql_insertar_usuario, (nombre, email, contraseña))
        conn.commit()
        print("Usuario insertado exitosamente.")
    except Error as e:
        print(f"Error al insertar usuario: {e}")


