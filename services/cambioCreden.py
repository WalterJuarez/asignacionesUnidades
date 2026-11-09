from database import Database


def actualizarUsuario(nombre, apellido, usuario, contra, usuario_actual):
    conexion = Database.get_connection()

    if conexion is None:
        return 0

    try:
        cursor = conexion.cursor()

        query = """
            UPDATE USUARIOS_DIESEL
            SET NOMBRE = %s,
                APELLIDO = %s,
                USUARIO = %s,
                PASS = %s
            WHERE USUARIO = %s
        """

        cursor.execute(query, (nombre, apellido, usuario, contra, usuario_actual))
        conexion.commit()

        cursor.close()
        conexion.close()

        return 1

    except Exception as error:
        print(f"Error al actualizar usuario: {error}")
        return 0
