import sqlite3
from sqlite3 import Error

def crear_conexion(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado a la base de datos {db_file}")
        return conn
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    return conn
