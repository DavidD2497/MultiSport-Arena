from flask import Flask, flash, jsonify, session, render_template, redirect, url_for, request
from modelo.conexion import crear_conexion
from modelo.usuario import crear_tabla_usuario, insertar_usuario, obtener_todos_los_usuarios, actualizar_nivel
from modelo.cancha import crear_tabla_cancha, insertar_cancha, obtener_canchas, obtener_todas_las_canchas, actualizar_cancha, eliminar_cancha, obtener_cancha_por_id
from modelo.reserva import crear_tabla_reserva, insertar_reserva, obtener_reservas, obtener_todas_las_reservas, eliminar_reserva, obtener_reservas_por_usuario
from controlador.autenticador import auth_bp
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def index():
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
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

@app.route('/admin/usuarios')
def admin_usuarios():
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    usuarios = obtener_todos_los_usuarios(conn)
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/hacer_admin/<int:id>')
def hacer_admin(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    actualizar_nivel(conn, id, 'administrador')
    conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/hacer_cliente/<int:id>')
def hacer_cliente(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    actualizar_nivel(conn, id, 'cliente')
    conn.close()
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/canchas')
def admin_canchas():
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    canchas = obtener_todas_las_canchas(conn)
    conn.close()
    return render_template('admin_canchas.html', canchas=canchas)

@app.route('/admin/canchas/agregar', methods=['POST'])
def agregar_cancha():
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    insertar_cancha(conn, tipo, nombre)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/canchas/modificar/<int:id>')
def modificar_cancha(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    cancha = obtener_cancha_por_id(conn, id)
    conn.close()
    return render_template('admin_modificar_cancha.html', cancha=cancha)

@app.route('/admin/canchas/actualizar/<int:id>', methods=['POST'])
def actualizar_cancha_route(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    actualizar_cancha(conn, id, tipo, nombre)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/canchas/eliminar/<int:id>', methods=['GET'])
def eliminar_cancha_route(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    eliminar_cancha(conn, id)
    conn.close()
    return redirect(url_for('admin_canchas'))

@app.route('/admin/reservas')
def admin_reservas():
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    reservas = obtener_todas_las_reservas(conn)
    conn.close()
    return render_template('admin_reservas.html', reservas=reservas)

@app.route('/admin/reservas/eliminar/<int:id>', methods=['GET'])
def eliminar_reserva_route(id):
    if session.get('user_role') != "administrador":
        flash("No puedes ingresar, no eres admin.")
        return redirect(url_for('index'))
    conn = crear_conexion("reserva_canchas.db")
    eliminar_reserva(conn, id)
    conn.close()
    return redirect(url_for('admin_reservas'))

@app.route('/reserva/hacer_reserva/<deporte>', methods=['GET'])
def hacer_reserva(deporte):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = crear_conexion("reserva_canchas.db")
    fecha_actual = datetime.now().date()
    canchas = obtener_canchas(conn, deporte)
    conn.close()
    return render_template('hacer_reserva.html', fecha_actual=fecha_actual, canchas=canchas, deporte=deporte)

@app.route('/reserva/obtener_horarios')
def obtener_horarios():
    fecha = request.args.get('fecha')
    conn = crear_conexion("reserva_canchas.db")
    reservas = obtener_reservas(conn, fecha)
    conn.close()
    return jsonify([{'id_cancha': r[0], 'hora': r[1]} for r in reservas])

@app.route('/reserva/procesar_reserva', methods=['POST'])
def procesar_reserva():
    id_usuario = session.get('user_id')
    id_cancha = request.form.get('id_cancha')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    
    conn = crear_conexion("reserva_canchas.db")
    try:
        insertar_reserva(conn, id_usuario, id_cancha, fecha, int(hora))
        conn.close()
        return jsonify({'success': True, 'message': 'Reserva realizada con éxito'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/mis_reservas')
def mis_reservas():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = crear_conexion("reserva_canchas.db")
    reservas = obtener_reservas_por_usuario(conn, session['user_id'])
    conn.close()
    return render_template('mis_reservas.html', reservas=reservas)

if __name__ == "__main__":
    conn = crear_conexion("reserva_canchas.db")
    if conn is not None:
        crear_tabla_usuario(conn)
        crear_tabla_cancha(conn)
        crear_tabla_reserva(conn)
        insertar_usuario(conn, "Cliente", "juan@example.com", "contrasena123", "cliente")
        insertar_usuario(conn, "Admin", "admin@example.com", "admin123", "administrador")
        insertar_cancha(conn, "padel", "Cancha Padel 1")
        insertar_cancha(conn, "padel", "Cancha Padel 2")
        insertar_cancha(conn, "padel", "Cancha Padel 3")
        insertar_cancha(conn, "tenis", "Cancha Tenis 1")
        insertar_cancha(conn, "tenis", "Cancha Tenis 2")
        insertar_cancha(conn, "tenis", "Cancha Tenis 3")
        insertar_cancha(conn, "futbol", "Cancha 5v5")
        insertar_cancha(conn, "futbol", "Cancha 6v6")
        insertar_cancha(conn, "futbol", "Cancha 7v7")
        conn.close()
    app.run(debug=True)