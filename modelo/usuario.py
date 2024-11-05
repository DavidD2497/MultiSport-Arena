import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash

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
        contraseña_hash = generate_password_hash(contraseña)  # Cifra la contraseña
        sql_insertar_usuario = """
        INSERT INTO Usuarios (nombre, email, contraseña)
        VALUES (?, ?, ?)
        """
        cursor.execute(sql_insertar_usuario, (nombre, email, contraseña_hash))
        conn.commit()
        print("Usuario insertado exitosamente.")
    except Error as e:
        print(f"Error al insertar usuario: {e}")

def obtener_usuario_por_email(conn, email):
    cursor = conn.cursor()
    sql_obtener_usuario = "SELECT * FROM Usuarios WHERE email = ?"
    cursor.execute(sql_obtener_usuario, (email,))
    return cursor.fetchone()

def verificar_contraseña(conn, email, contraseña):
    usuario = obtener_usuario_por_email(conn, email)
    if usuario:
        contraseña_hash = usuario[3]
        return check_password_hash(contraseña_hash, contraseña)
    return False



