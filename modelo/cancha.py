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
        query_check = "SELECT COUNT(*) FROM Canchas WHERE nombre = ?"
        cursor.execute(query_check, (nombre,))
        if cursor.fetchone()[0] > 0:
            print(f"Error: Ya existe una cancha con el nombre '{nombre}'.")
            return False

        sql_insertar_cancha = """
        INSERT INTO Canchas (tipo, nombre)
        VALUES (?, ?)
        """
        cursor.execute(sql_insertar_cancha, (tipo, nombre))
        conn.commit()
        print(f"Cancha '{nombre}' insertada exitosamente.")
        return True
    except Error as e:
        print(f"Error al insertar cancha: {e}")
        return False

def obtener_todas_las_canchas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Canchas")
    return cursor.fetchall()

def obtener_cancha_por_id(conn, id_cancha):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Canchas WHERE id_cancha = ?", (id_cancha,))
    return cursor.fetchone()

def actualizar_cancha(conn, id_cancha, tipo, nombre):
    cursor = conn.cursor()
    cursor.execute("UPDATE Canchas SET tipo = ?, nombre = ? WHERE id_cancha = ?", (tipo, nombre, id_cancha))
    conn.commit()

def eliminar_cancha(conn, id_cancha):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Canchas WHERE id_cancha = ?", (id_cancha,))
        conn.commit()
        print(f"Cancha con id {id_cancha} eliminada exitosamente.")
    except Error as e:
        print(f"Error al eliminar cancha: {e}")


def obtener_canchas(conn, tipo_cancha):
    query = """
        SELECT id_cancha, nombre FROM Canchas WHERE tipo = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (tipo_cancha,))
    canchas = cursor.fetchall()
    return canchas




