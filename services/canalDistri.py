from database import Database

def obtener_canalDistribucion():
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            CONSECUTIVO,
            CANAL,
            DESCRIPCION,
            FECHA_REGISTRO
        FROM DVN_CANAL_DISTRIBUCION
        ORDER BY FECHA_REGISTRO DESC
    """)

    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return datos

def existe_canal(canal):
    conexion = Database.get_connection() 
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            CONSECUTIVO,
            CANAL
        FROM DVN_CANAL_DISTRIBUCION
        WHERE CANAL = %s
    """, (canal,))

    dato = cursor.fetchone()
    cursor.close()
    conexion.close()

    return dato

def crear_canalDistribucion(canal, descripcion):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO DVN_CANAL_DISTRIBUCION (CANAL, DESCRIPCION)
        VALUES (%s, %s)
    """, (canal, descripcion))

    conexion.commit()
    cursor.close()
    conexion.close()

    
