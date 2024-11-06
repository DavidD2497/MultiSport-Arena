from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modelo.reserva import insertar_reserva, obtener_reservas
from modelo.cancha import obtener_canchas
from modelo.conexion import crear_conexion

# Crear el blueprint para el manejo de reservas
reserva_bp = Blueprint('reserva', __name__, url_prefix='/reserva')

DATABASE = 'reserva_canchas.db'

# Ruta para mostrar el calendario de reservas
@reserva_bp.route('/reserva')
def calendario():
    try:
        conn = crear_conexion(DATABASE)
        
        # Obtener canchas filtradas por el tipo de cancha
        canchas = obtener_canchas(conn)  # Asume que la función ahora recibe un parámetro de tipo
        reservas = obtener_reservas(conn)
        
        conn.close()

    except Exception as e:
        flash(f'Error al obtener datos: {str(e)}', 'danger')
        return redirect(url_for('index'))  # O redirigir a alguna página de error
    
    return render_template('reserva.html', canchas=canchas, reservas=reservas, tipo_cancha=tipo_cancha)


# Ruta para hacer una nueva reserva
@reserva_bp.route('/hacer_reserva/<tipo_cancha>', methods=['GET', 'POST'])
def hacer_reserva(tipo_cancha):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para hacer una reserva', 'danger')
        return redirect(url_for('auth.login'))  # Asegúrate de que el blueprint se llame 'auth_bp'

    if request.method == 'POST':
        # Recibir datos del formulario
        cancha_id = request.form['cancha_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        estado = "Por confirmar"  # Estado inicial de la reserva

        conn = crear_conexion(DATABASE)

        # Verificar si ya existe una reserva para la misma fecha y hora
        query_check = """
            SELECT COUNT(*) 
            FROM Reservas 
            WHERE id_cancha = ? AND fecha = ? AND hora = ?
        """
        cursor = conn.cursor()
        cursor.execute(query_check, (cancha_id, fecha, hora))
        count = cursor.fetchone()[0]

        if count > 0:
            flash('¡Error! Ya existe una reserva para esa cancha, fecha y hora. Por favor, elige otro horario.', 'danger')
            conn.close()
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

        # Si no existe, insertar la nueva reserva
        insertar_reserva(conn, session['user_id'], cancha_id, fecha, hora, estado)
        conn.close()

        flash('Reserva realizada con éxito.', 'success')
        return redirect(url_for('reserva.hacer_reserva'))

    # Mostrar las canchas disponibles al hacer una nueva reserva
    conn = crear_conexion(DATABASE)
    canchas = obtener_canchas(conn, tipo_cancha)
    conn.close()

    return render_template('hacer_reserva.html', canchas=canchas, tipo_cancha=tipo_cancha)
