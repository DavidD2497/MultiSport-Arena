from flask import Flask, session, render_template
from modelo.conexion import crear_conexion
from modelo.usuario import crear_tabla_usuario, insertar_usuario
from modelo.administrador import crear_tabla_administrador, insertar_administrador
from modelo.cancha import crear_tabla_cancha, insertar_cancha
from modelo.reserva import crear_tabla_reserva, insertar_reserva
from controlador.autenticador import auth_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def index():

    if 'user_id' in session:
        return render_template('index.html', usuario=session['user_id'])  # pasa la información de usuario a la plantilla
    else:
        mensaje ="Bienvenido a MultiSport Arena. <a href='/auth/login'>Iniciar sesión</a> o <a href='/auth/registro'>Registrarse</a>"
        return render_template('index.html', mensaje=mensaje)


#     user_id = session.get('user_id')  # Obtener el ID del usuario si está en la sesión
#     return render_template("index.html", user_id=user_id)
# >>>>>>> origin/tomas

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
