from flask import Flask
from modelo.conexion import crear_conexion
from modelo.usuario import crear_tabla_usuario, insertar_usuario
from modelo.administrador import crear_tabla_administrador, insertar_administrador
from modelo.cancha import crear_tabla_cancha, insertar_cancha
from modelo.reserva import crear_tabla_reserva, insertar_reserva

app = Flask(__name__)

@app.route('/')
def index():
    return "Bienvenido a PicResizer"

if __name__ == "__main__":
    conn = crear_conexion("reserva_canchas.db")
    if conn is not None:
        crear_tabla_usuario(conn)
        crear_tabla_administrador(conn)
        crear_tabla_cancha(conn)
        crear_tabla_reserva(conn)
        insertar_usuario(conn, "Juan Pérez", "juan@example.com", "contrasena123")
        insertar_administrador(conn, "Admin Uno", "admin@example.com", "adminpass")
        insertar_cancha(conn, "padel", "Cancha Padel 1")
        insertar_reserva(conn, 1, 1, "2023-04-15", 16, "Por Confirmar")
        conn.close()
    app.run(debug=True)





