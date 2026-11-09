from database import Database
from mysql.connector import Error

def obtener_asignacionUnidad():
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            a.COD_EMPLEADO ,
            p.NOMBRE ,
            u.UNIDAD,
            d.CANAL ,
            a.FECHA_ASIGNACION 
        FROM ASIGNAR_UNIDAD_DIESEL a
        INNER JOIN DVN_PILOTO p
            ON a.COD_EMPLEADO = p.COD_EMPLEADO
        INNER JOIN UNIDAD_DVN u
            ON a.UNIDAD_ASIGNADA = u.CONSECUTIVO
        INNER JOIN DVN_CANAL_DISTRIBUCION d
            ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        ORDER BY a.FECHA_ASIGNACION DESC
        LIMIT 150          
    """)

    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def buscar_asigUnidad_por_codigo(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            a.COD_EMPLEADO ,
            p.NOMBRE ,
            u.UNIDAD,
            d.CANAL ,
            a.FECHA_ASIGNACION 
        FROM ASIGNAR_UNIDAD_DIESEL a
        INNER JOIN DVN_PILOTO p
            ON a.COD_EMPLEADO = p.COD_EMPLEADO
        INNER JOIN UNIDAD_DVN u
            ON a.UNIDAD_ASIGNADA = u.CONSECUTIVO
        INNER JOIN DVN_CANAL_DISTRIBUCION d
            ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        WHERE a.COD_EMPLEADO LIKE %s
        ORDER BY a.FECHA_ASIGNACION DESC;
    """, (f"%{codigo}%",))
        
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def buscarAsigUnidadName(unidad):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            a.COD_EMPLEADO ,
            p.NOMBRE ,
            u.UNIDAD,
            d.CANAL ,
            a.FECHA_ASIGNACION 
        FROM ASIGNAR_UNIDAD_DIESEL a
        INNER JOIN DVN_PILOTO p
            ON a.COD_EMPLEADO = p.COD_EMPLEADO
        INNER JOIN UNIDAD_DVN u
            ON a.UNIDAD_ASIGNADA = u.CONSECUTIVO
        INNER JOIN DVN_CANAL_DISTRIBUCION d
            ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        WHERE u.UNIDAD LIKE %s
        ORDER BY
            u.UNIDAD LIKE 'GN-%' DESC, 
            a.FECHA_ASIGNACION DESC;
    """, (f"%{unidad}%",))
        
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def obtener_unidadAsig():
    conexion = Database.get_connection() 
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            UNIDAD
        FROM UNIDAD_DVN
        ORDER BY FECHA_REGISTRO DESC
    """) 
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def obtener_codigoPiloto():
    conexion = Database.get_connection() 
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            COD_EMPLEADO
        FROM DVN_PILOTO
        ORDER BY FECHA_REGISTRO DESC
    """) 
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def obtener_nombrePiloto(codigo):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            NOMBRE
        FROM DVN_PILOTO
        WHERE COD_EMPLEADO = %s
    """, (codigo,))

    dato = cursor.fetchone()

    cursor.close()
    conexion.close()

    if dato:
        return dato[0]

    return ""           

def obtener_consecutivoUnidad(unidad):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            CONSECUTIVO
        FROM UNIDAD_DVN
        WHERE UNIDAD = %s
    """, (unidad,))

    dato = cursor.fetchone()

    cursor.close()
    conexion.close()

    if dato:
        return dato[0]

    return None


def crear_asignacionUnidad(codigo_empleado, unidad_asignada, usuario):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO ASIGNAR_UNIDAD_DIESEL (
            COD_EMPLEADO,
            UNIDAD_ASIGNADA,
            USUARIO
        ) VALUES (%s, %s, %s)
    """, (codigo_empleado, unidad_asignada, usuario))

    conexion.commit()

    cursor.close()
    conexion.close()

def buscarAsigGeneral(texto):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            a.COD_EMPLEADO,
            p.NOMBRE,
            u.UNIDAD,
            d.CANAL,
            a.FECHA_ASIGNACION
        FROM ASIGNAR_UNIDAD_DIESEL a
        INNER JOIN DVN_PILOTO p
            ON a.COD_EMPLEADO = p.COD_EMPLEADO
        INNER JOIN UNIDAD_DVN u
            ON a.UNIDAD_ASIGNADA = u.CONSECUTIVO
        INNER JOIN DVN_CANAL_DISTRIBUCION d
            ON u.CONSECUTIVO_CANAL = d.CONSECUTIVO
        WHERE a.COD_EMPLEADO LIKE %s
           OR u.UNIDAD LIKE %s
        ORDER BY a.FECHA_ASIGNACION DESC
        LIMIT 150           
    """, (f"{texto}%", f"{texto}%"))

    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos    

