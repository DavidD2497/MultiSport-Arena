from flask import Flask, session, render_template, redirect, url_for, request
from modelo.conexion import crear_conexion
from modelo.usuario import crear_tabla_usuario, insertar_usuario, obtener_todos_los_usuarios, actualizar_nivel
from modelo.cancha import crear_tabla_cancha, insertar_cancha, obtener_todas_las_canchas, actualizar_cancha, eliminar_cancha, obtener_cancha_por_id
from modelo.reserva import crear_tabla_reserva, insertar_reserva
from controlador.autenticador import auth_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

app.register_blueprint(auth_bp, url_prefix="/auth")

def es_admin():
    return session.get('rol') == 'admin'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/reservar/<tipo_cancha>')
def reservar(tipo_cancha):
    return f"Reserva para cancha de {tipo_cancha}."

@app.route('/admin/usuarios')
def admin_usuarios():
    conn = crear_conexion("reserva_canchas.db")
    usuarios = obtener_todos_los_usuarios(conn)
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/hacer_admin/<int:id>')
def hacer_admin(id):
    conn = crear_conexion("reserva_canchas.db")
    actualizar_nivel(conn, id, 'admin')
    conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/hacer_cliente/<int:id>')
def hacer_cliente(id):
    conn = crear_conexion("reserva_canchas.db")
    actualizar_nivel(conn, id, 'cliente')
    conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/canchas')
def admin_canchas():
    conn = crear_conexion("reserva_canchas.db")
    canchas = obtener_todas_las_canchas(conn)
    conn.close()
    return render_template('admin_canchas.html', canchas=canchas)

@app.route('/admin/canchas/agregar', methods=['POST'])
def agregar_cancha():
    conn = crear_conexion("reserva_canchas.db")
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    insertar_cancha(conn, tipo, nombre)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/canchas/modificar/<int:id>')
def modificar_cancha(id):
    conn = crear_conexion("reserva_canchas.db")
    cancha = obtener_cancha_por_id(conn, id)
    conn.close()
    return render_template('admin_modificar_cancha.html', cancha=cancha)

@app.route('/admin/canchas/actualizar/<int:id>', methods=['POST'])
def actualizar_cancha_route(id):
    conn = crear_conexion("reserva_canchas.db")
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    actualizar_cancha(conn, id, tipo, nombre)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/canchas/eliminar/<int:id>', methods=['GET'])
def eliminar_cancha_route(id):
    conn = crear_conexion("reserva_canchas.db")
    eliminar_cancha(conn, id)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/reservas')
def admin_reservas():
    if not es_admin():
        return render_template('index.html')
    return render_template('admin_reservas.html')

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






