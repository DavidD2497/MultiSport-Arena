from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modelo.reserva import insertar_reserva, obtener_reservas
from modelo.cancha import obtener_canchas
from modelo.conexion import crear_conexion
from datetime import datetime

reserva_bp = Blueprint('reserva', __name__, url_prefix='/reserva')

DATABASE = 'reserva_canchas.db'

@reserva_bp.route('/reserva', methods=['GET', 'POST'])
def calendario():
    try:
        conn = crear_conexion(DATABASE)
        
       
        tipo_cancha = request.args.get('tipo_cancha')  
        canchas = obtener_canchas(conn, tipo_cancha)  
        reservas = obtener_reservas(conn)
        
        conn.close()

    except Exception as e:
        flash(f'Error al obtener datos: {str(e)}', 'danger')
        return redirect(url_for('index'))  
    
    return render_template('reserva.html', canchas=canchas, reservas=reservas, tipo_cancha=tipo_cancha)



@reserva_bp.route('/hacer_reserva/<tipo_cancha>', methods=['GET', 'POST'])
def hacer_reserva(tipo_cancha):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para hacer una reserva', 'danger')
        return redirect(url_for('auth.login'))

    HORA_APERTURA = 8 
    HORA_CIERRE = 22   

    horas_disponibles = []
    for hour in range(HORA_APERTURA, HORA_CIERRE):
        # Genera las horas en formato 24 horas
        horas_disponibles.append(f"{hour:02d}:00")  

    if request.method == 'POST':
        # Recibir datos del formulario
        cancha_id = request.form['cancha_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        estado = "Por confirmar"  

        try:
            fecha_reserva = datetime.strptime(fecha + ' ' + hora, '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Error en el formato de fecha o hora.', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

       
        ahora = datetime.now()

      
        if fecha_reserva <= ahora:
            flash('No puedes hacer una reserva para una fecha y hora pasada.', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

        if fecha_reserva.hour < HORA_APERTURA or fecha_reserva.hour >= HORA_CIERRE:
            flash(f'La hora seleccionada está fuera del horario de apertura ({HORA_APERTURA}:00 - {HORA_CIERRE}:00)', 'danger')
            return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

 
        conn = crear_conexion(DATABASE)

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

        insertar_reserva(conn, session['user_id'], cancha_id, fecha, hora, estado)
        conn.close()

        flash('Reserva realizada con éxito.', 'success')
        return redirect(url_for('reserva.hacer_reserva', tipo_cancha=tipo_cancha))

    conn = crear_conexion(DATABASE)
    canchas = obtener_canchas(conn, tipo_cancha) 
    conn.close()

    return render_template('hacer_reserva.html', canchas=canchas, tipo_cancha=tipo_cancha, horas_disponibles=horas_disponibles)
