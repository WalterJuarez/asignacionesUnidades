from database import Database

def validar_usuario(usuario, contra):
    conexion = Database.get_connection()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT NOMBRE, APELLIDO, USUARIO, PERMISO_DIESEL
            FROM USUARIOS_DIESEL
            WHERE USUARIO = %s
              AND PASS = %s
        """, (usuario, contra))

        return cursor.fetchone()

    except Exception as error:
        print(f"Error al validar usuario: {error}")
        return None

    finally:
        if cursor:
            cursor.close()
        conexion.close()