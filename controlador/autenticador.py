from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from modelo.usuario import insertar_usuario, obtener_usuario_por_email, verificar_contraseña
from modelo.conexion import crear_conexion

auth_bp = Blueprint('auth', __name__)

DATABASE = 'reserva_canchas.db'

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']

        # Crear conexión a la base de datos
        conn = crear_conexion(DATABASE)
        
        # Verificar si el usuario ya existe
        if obtener_usuario_por_email(conn, email):
            flash('El correo ya está registrado. Intenta con otro.')
            conn.close()
            return redirect(url_for('auth.registro'))

        # Insertar nuevo usuario en la base de datos
        insertar_usuario(conn, nombre, email, contraseña)
        conn.close()

        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']

        conn = crear_conexion(DATABASE)

        if verificar_contraseña(conn, email, contraseña):
            
            usuario = obtener_usuario_por_email(conn, email)
            session['user_id'] = usuario[0]  
            flash('Inicio de sesión exitoso.')
            conn.close()
            return redirect(url_for('index'))

        flash('Usuario o contraseña incorrectos.')
        conn.close()
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Cerraste sesión exitosamente.')
    return redirect(url_for('auth.login'))
