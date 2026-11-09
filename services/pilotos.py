from database import Database


def obtener_pilotos():
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                COD_EMPLEADO,
                NOMBRE,
                FECHA_REGISTRO
            FROM DVN_PILOTO
            ORDER BY FECHA_REGISTRO DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()


def buscar_pilotos_por_codigo(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                COD_EMPLEADO,
                NOMBRE,
                FECHA_REGISTRO
            FROM DVN_PILOTO
            WHERE COD_EMPLEADO LIKE %s
            ORDER BY FECHA_REGISTRO DESC
        """, (f"%{codigo}%",))

        return cursor.fetchall()

    finally:
        cursor.close()
        conexion.close()


def existe_piloto(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                COD_EMPLEADO,
                NOMBRE
            FROM DVN_PILOTO
            WHERE COD_EMPLEADO = %s
        """, (codigo,))

        return cursor.fetchone()

    finally:
        cursor.close()
        conexion.close()


def crear_piloto(codigo, nombre):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO DVN_PILOTO (
                COD_EMPLEADO,
                NOMBRE
            ) VALUES (%s, %s)
        """, (codigo, nombre))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()