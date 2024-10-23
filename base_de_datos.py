import sqlite3

from sqlite3 import Error

def crear_conexion(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado a la base de datos {db_file}")
        return conn
    except Error as e:
        print(f"Error al conectar con la base de datos {e}")
        return conn
    
def crear_tablas(conn):
    try:
        cursor = conn.cursor()

        # Tabla Usuarios
        sql_crear_tabla_usuarios = """
        CREATE TABLE IF NOT EXISTS Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('admin', 'cliente')) NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(sql_crear_tabla_usuarios)

        # Tabla Canchas
        sql_crear_tabla_canchas = """
        CREATE TABLE IF NOT EXISTS Canchas (
            id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('futbol', 'tenis', 'padel')) NOT NULL,
            precio_por_hora REAL NOT NULL,
            estado TEXT CHECK(estado IN ('disponible', 'en mantenimiento')) DEFAULT 'disponible',
            descripcion TEXT
        );
        """
        cursor.execute(sql_crear_tabla_canchas)

        # Tabla Horarios (reservas siempre de una hora dentro del rango de 14:00 a 24:00)
        sql_crear_tabla_horarios = """
        CREATE TABLE IF NOT EXISTS Horarios (
            id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cancha INTEGER NOT NULL,
            hora_inicio TIME CHECK(hora_inicio >= '14:00' AND hora_inicio <= '23:00') NOT NULL,
            hora_fin TIME CHECK(hora_fin = TIME(hora_inicio, '+1 hour')) NOT NULL,
            FOREIGN KEY (id_cancha) REFERENCES Canchas(id_cancha)
        );
        """
        cursor.execute(sql_crear_tabla_horarios)

        # Tabla Reservas (con reserva del 20% y confirmación en 24 horas)
        sql_crear_tabla_reservas = """
        CREATE TABLE IF NOT EXISTS Reservas (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_cancha INTEGER NOT NULL,
            id_horario INTEGER NOT NULL,
            fecha_reserva DATE NOT NULL,
            monto_reserva REAL NOT NULL CHECK(monto_reserva = (SELECT precio_por_hora * 0.2 FROM Canchas WHERE Canchas.id_cancha = Reservas.id_cancha)),
            estado TEXT CHECK(estado IN ('pendiente', 'confirmada', 'rechazada')) DEFAULT 'pendiente',
            fecha_limite_confirmacion TIMESTAMP DEFAULT (DATETIME('now', '+1 day')),
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario),
            FOREIGN KEY (id_cancha) REFERENCES Canchas(id_cancha),
            FOREIGN KEY (id_horario) REFERENCES Horarios(id_horario)
        );
        """
        cursor.execute(sql_crear_tabla_reservas)

        print("Tablas creadas exitosamente.")
    
    except Error as e:
        print(f"Error al crear las tablas: {e}")

def insertar_datos_iniciales(conn):
    try:
        cursor = conn.cursor()

        # Insertar datos en la tabla Usuarios
        sql_insertar_usuarios = """
        INSERT INTO Usuarios (nombre, email, contraseña, rol)
        VALUES 
        ('Admin', 'admin@example.com', 'admin123', 'admin'),
        ('Juan Pérez', 'juan@example.com', 'juan123', 'cliente'),
        ('María López', 'maria@example.com', 'maria123', 'cliente');
        """
        cursor.execute(sql_insertar_usuarios)

        # Insertar datos en la tabla Canchas
        sql_insertar_canchas = """
        INSERT INTO Canchas (nombre, tipo, precio_por_hora, estado, descripcion)
        VALUES
        ('Cancha 1', 'futbol', 100.0, 'disponible', 'Cancha de fútbol con césped artificial'),
        ('Cancha 2', 'tenis', 80.0, 'disponible', 'Cancha de tenis de polvo de ladrillo'),
        ('Cancha 3', 'padel', 70.0, 'en mantenimiento', 'Cancha de pádel techada');
        """
        cursor.execute(sql_insertar_canchas)

        # Insertar datos en la tabla Horarios (horarios fijos de una hora entre 14:00 y 24:00)

        for id_cancha in range(1, 4):  
            for hora in range(14, 25):
                hora_inicio = f'{hora}:00'
                hora_fin = f'{hora + 1}:00'
                cursor.execute(
                    "INSERT INTO Horarios (id_cancha, hora_inicio, hora_fin) VALUES (?, ?, ?)",
                    (id_cancha, hora_inicio, hora_fin)
                )

        # Insertar datos en la tabla Reservas
        sql_insertar_reservas = """
        INSERT INTO Reservas (id_usuario, id_cancha, id_horario, fecha_reserva, monto_reserva, estado)
        VALUES
        (2, 1, 1, '2024-10-24', 20.0, 'pendiente'),
        (3, 2, 3, '2024-10-25', 16.0, 'pendiente');
        """
        cursor.execute(sql_insertar_reservas)

        # Confirmar cambios
        conn.commit()
        print("Datos insertados exitosamente.")
    
    except Error as e:
        print(f"Error al insertar los datos: {e}")

