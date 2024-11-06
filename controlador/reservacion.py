from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modelo.reserva import insertar_reserva, obtener_reservas
from modelo.cancha import obtener_canchas
from modelo.conexion import crear_conexion
from datetime import datetime

# Crear el blueprint para el manejo de reservas
reserva_bp = Blueprint('reserva', __name__, url_prefix='/reserva')

DATABASE = 'reserva_canchas.db'

# Ruta para mostrar el calendario de reservas
@reserva_bp.route('/reserva', methods=['GET', 'POST'])
def calendario():
    try:
        conn = crear_conexion(DATABASE)
        
        # Aquí obtenemos las canchas filtradas por tipo de cancha si se pasa el parámetro 'tipo_cancha'
        tipo_cancha = request.args.get('tipo_cancha')  # Obtener tipo_cancha de la URL si está presente
        canchas = obtener_canchas(conn, tipo_cancha)  # Filtrar por tipo_cancha
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
        return redirect(url_for('auth.login'))

    # Definir las horas de apertura y cierre en formato de 24 horas
    HORA_APERTURA = 8  # 08:00
    HORA_CIERRE = 22   # 22:00 (10:00 PM)

    # Obtener las horas disponibles (en formato 24 horas)
    horas_disponibles = []
    for hour in range(HORA_APERTURA, HORA_CIERRE):
        # Genera las horas en formato 24 horas
        horas_disponibles.append(f"{hour:02d}:00")  # Ejemplo: '08:00', '09:00', ..., '21:00'

    if request.method == 'POST':
        # Recibir datos del formulario
        cancha_id = request.form['cancha_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        estado = "Por confirmar"  # Estado inicial de la reserva

        # Convertir la fecha y hora del formulario a un objeto datetime
        try:
            fecha_reserva = datetime.strptime(fecha + ' ' + hora, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Error en el formato de fecha o hora.', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

        # Obtener la fecha y hora actuales
        ahora = datetime.now()

        # Verificar si la fecha y hora de la reserva son en el futuro
        if fecha_reserva <= ahora:
            flash('No puedes hacer una reserva para una fecha y hora pasada.', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

        # Verificar que la hora seleccionada esté dentro del rango permitido
        if fecha_reserva.hour < HORA_APERTURA or fecha_reserva.hour >= HORA_CIERRE:
            flash(f'La hora seleccionada está fuera del horario de apertura ({HORA_APERTURA}:00 - {HORA_CIERRE}:00)', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

        # Conectar a la base de datos
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
        return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

    # Mostrar las canchas disponibles al hacer una nueva reserva, filtradas por tipo
    conn = crear_conexion(DATABASE)
    canchas = obtener_canchas(conn, tipo_cancha)  # Filtrado por tipo de cancha
    conn.close()

    return render_template('hacer_reserva.html', canchas=canchas, tipo_cancha=tipo_cancha, horas_disponibles=horas_disponibles)
