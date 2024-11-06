from flask import Flask, session, render_template
from modelo.conexion import crear_conexion
from modelo.usuario import crear_tabla_usuario, insertar_usuario
from modelo.cancha import crear_tabla_cancha, insertar_cancha
from modelo.reserva import crear_tabla_reserva, insertar_reserva
from controlador.autenticador import auth_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def index():

    user_id = session.get('user_id')  # Obtener el ID del usuario si está en la sesión
    return render_template("index.html", user_id=user_id)

    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/comoalquilar')
def comoalquilar():
    return render_template('comoalquilar.html')

@app.route('/sobrenosotros')
def sobrenosotros():
    return render_template('sobrenosotros.html')
    
@app.route('/admin/dashboard')
def admin_dashboard():
    return "Panel de Administración"

@app.route('/reservar/<tipo_cancha>')
def reservar(tipo_cancha):
    return f"Reserva para cancha de {tipo_cancha}."


if __name__ == "__main__":
    conn = crear_conexion("reserva_canchas.db")
    if conn is not None:
        crear_tabla_usuario(conn)
        crear_tabla_cancha(conn)
        crear_tabla_reserva(conn)
        insertar_usuario(conn, "Cliente", "juan@example.com", "contrasena123", "cliente")
        insertar_usuario(conn, "Admin", "admin@example.com", "admin123", "administrador")
        insertar_cancha(conn, "padel", "Cancha Padel 1")
        insertar_reserva(conn, 1, 1, "2023-04-15", 16, "Por Confirmar")
        conn.close()
    app.run(debug=True)
