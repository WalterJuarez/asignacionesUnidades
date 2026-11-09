from database import Database

def obtener_unidades():
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            u.UNIDAD,
            d.CANAL,
            u.FECHA_REGISTRO
        FROM unidad_dvn u
        INNER JOIN dvn_canal_distribucion d
        ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        ORDER BY u.FECHA_REGISTRO DESC;
    """)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def buscar_unidades_por_codigo(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            u.UNIDAD,
            d.CANAL,
            u.FECHA_REGISTRO
        FROM unidad_dvn u
        INNER JOIN dvn_canal_distribucion d
        ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        WHERE u.UNIDAD LIKE %s
        ORDER BY 
            u.UNIDAD LIKE 'GN-%' DESC,       
            u.FECHA_REGISTRO DESC
    """, (f"%{codigo}%",))

    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def obtener_canales():
    conexion = Database.get_connection() 
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            CANAL
        FROM DVN_CANAL_DISTRIBUCION     
        ORDER BY FECHA_REGISTRO DESC
    """) 
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def existe_unidad(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            u.UNIDAD,
            d.CANAL
        FROM unidad_dvn u
        INNER JOIN dvn_canal_distribucion d
        ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        WHERE u.UNIDAD = %s
    """, (codigo,))

    unidad = cursor.fetchone()
    cursor.close()
    conexion.close()

    return unidad

def obtener_consecutivo_canal(canal):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            CONSECUTIVO
        FROM DVN_CANAL_DISTRIBUCION
        WHERE CANAL = %s
    """, (canal,))

    dato = cursor.fetchone()

    cursor.close()
    conexion.close()

    if dato:
        return dato[0]

    return None


def crear_unidad(unidad, consecutivo_canal):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO UNIDAD_DVN (
            UNIDAD,
            CONSECUTIVO_CANAL
        ) VALUES (%s, %s)
    """, (unidad, consecutivo_canal))

    conexion.commit()

    cursor.close()
    conexion.close()


