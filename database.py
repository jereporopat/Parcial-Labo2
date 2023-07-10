import sqlite3

def crear_tabla():
    # Establecer la conexión con la base de datos
    conexion = sqlite3.connect("datos_jugadores.db")
    cursor = conexion.cursor()

    # Crear la tabla "jugadores" si no existe
    cursor.execute("CREATE TABLE IF NOT EXISTS jugadores (nombre TEXT, puntuacion INTEGER)")

    # Cerrar la conexión con la base de datos
    conexion.close()

def guardar_datos(nombre_jugador, score):
    # Establecer la conexión con la base de datos
    conexion = sqlite3.connect("datos_jugadores.db")
    cursor = conexion.cursor()

    # Insertar los datos del jugador en la tabla "jugadores"
    cursor.execute("INSERT INTO jugadores (nombre, puntuacion) VALUES (?, ?)", (nombre_jugador, score))

    # Guardar los cambios y cerrar la conexión con la base de datos
    conexion.commit()
    conexion.close()
