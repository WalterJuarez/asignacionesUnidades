from database import Database

#def obtener_despachos(fecha_inicio, fecha_fin):
#    conexion = Database.get_connection()
#    cursor = conexion.cursor()

#    cursor.execute("""
#        SELECT
#            t.*,
#            (t.KILOMETRAJE_ACTUAL - t.`KILOMETRAJE ANTERIOR`) AS DIFERENCIA
#        FROM (
#            SELECT
#                d1.CONSECUTIVO AS `NO DESPACHO`,
#                d1.UNIDAD,
#                d1.PILOTO AS `PILOTO / RESPONSABLE`,
#                d1.GALONES_MODBUS AS `GALONES DESPACHADOS`,
#                d1.GALONES_PULSOS AS `TOTAL DESPACHADO`,
#                d1.FECHA_REGISTRO AS `FECHA DESPACHO`,
#                d1.COD_EMPLEADO,
#                d1.KILOMETRAJE_ACTUAL,
#                IFNULL(
#                    (
#                        SELECT d2.KILOMETRAJE_ACTUAL
#                        FROM dvn1_despachos d2
#                        WHERE d2.UNIDAD = d1.UNIDAD
#                          AND d2.FECHA_REGISTRO < d1.FECHA_REGISTRO
#                        ORDER BY d2.FECHA_REGISTRO DESC
#                        LIMIT 1
#                    ),
#                    0
#                ) AS `KILOMETRAJE ANTERIOR`
#            FROM dvn1_despachos d1
#            WHERE d1.FECHA >= %s
#              AND d1.FECHA <= %s
#        ) t
#        ORDER BY t.`FECHA DESPACHO` DESC
#    """, (fecha_inicio, fecha_fin))

#    datos = cursor.fetchall()
#    columnas = [columna[0] for columna in cursor.description]

#    cursor.close()
#    conexion.close()

#    return columnas, datos

def obtener_despachoUnidad(unidad, fecha_inicio, fecha_fin):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                t.*,
                (t.KILOMETRAJE_ACTUAL - t.`KILOMETRAJE ANTERIOR`) AS DIFERENCIA
            FROM (
                SELECT
                    d1.CONSECUTIVO AS `No. DESPACHO`,
                    d1.UNIDAD,
                    d1.PILOTO AS `PILOTO / RESPONSABLE`,
                    d1.GALONES_MODBUS AS `GALONES DESPACHADOS`,
                    d1.GALONES_PULSOS AS `TOTAL DESPACHADO`,
                    d1.FECHA_REGISTRO AS `FECHA DESPACHO`,
                    d1.COD_EMPLEADO,
                    d1.KILOMETRAJE_ACTUAL,
                    IFNULL(
                        (
                            SELECT d2.KILOMETRAJE_ACTUAL
                            FROM dvn1_despachos d2
                            WHERE d2.UNIDAD = d1.UNIDAD
                              AND d2.FECHA_REGISTRO < d1.FECHA_REGISTRO
                            ORDER BY d2.FECHA_REGISTRO DESC
                            LIMIT 1
                        ),
                        0
                    ) AS `KILOMETRAJE ANTERIOR`
                FROM dvn1_despachos d1
                WHERE d1.UNIDAD LIKE %s
                  AND d1.FECHA BETWEEN %s AND %s
            ) t
            ORDER BY t.`FECHA DESPACHO` DESC
            LIMIT 100
        """, (f"{unidad}%", fecha_inicio, fecha_fin))

        datos = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        return columnas, datos

    finally:
        cursor.close()
        conexion.close()


#def obtener_despachos(fecha_inicio, fecha_fin):
#    conexion = Database.get_connection()
#    cursor = conexion.cursor()
#
#    try:
#        cursor.execute("""
#            WITH historial AS (
#                SELECT
#                    CONSECUTIVO,
#                    UNIDAD,
#                    PILOTO,
#                    GALONES_MODBUS,
#                    GALONES_PULSOS,
#                    FECHA,
#                    FECHA_REGISTRO,
#                    COD_EMPLEADO,
#                    KILOMETRAJE_ACTUAL,
#                    LAG(KILOMETRAJE_ACTUAL, 1, 0) OVER (
#                        PARTITION BY UNIDAD
#                        ORDER BY FECHA_REGISTRO
#                    ) AS KILOMETRAJE_ANTERIOR
#                FROM dvn1_despachos
#                WHERE FECHA <= %s
#            )
#            SELECT
#                CONSECUTIVO AS `NO DESPACHO`,
#                UNIDAD,
#                PILOTO AS `PILOTO / RESPONSABLE`,
#                GALONES_MODBUS AS `GALONES DESPACHADOS`,
#                GALONES_PULSOS AS `TOTAL DESPACHADO`,
#                FECHA_REGISTRO AS `FECHA DESPACHO`,
#                COD_EMPLEADO,
#                KILOMETRAJE_ACTUAL,
#                KILOMETRAJE_ANTERIOR AS `KILOMETRAJE ANTERIOR`,
#                KILOMETRAJE_ACTUAL - KILOMETRAJE_ANTERIOR AS DIFERENCIA
#            FROM historial
#            WHERE FECHA BETWEEN %s AND %s
#            ORDER BY FECHA_REGISTRO DESC
#        """, (fecha_fin, fecha_inicio, fecha_fin))
#
#        datos = cursor.fetchall()
#        columnas = [columna[0] for columna in cursor.description]
#
#        return columnas, datos
#
#    finally:
#        cursor.close()
#        conexion.close()

def obtener_despachos(fecha_inicio, fecha_fin):
    conexion = Database.get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                t.*,
                (t.KILOMETRAJE_ACTUAL - t.`KILOMETRAJE ANTERIOR`) AS DIFERENCIA
            FROM (
                SELECT
                    d1.CONSECUTIVO AS `NO DESPACHO`,
                    d1.UNIDAD,
                    d1.PILOTO AS `PILOTO / RESPONSABLE`,
                    d1.GALONES_MODBUS AS `GALONES DESPACHADOS`,
                    d1.GALONES_PULSOS AS `TOTAL DESPACHADO`,
                    d1.FECHA_REGISTRO AS `FECHA DESPACHO`,
                    d1.COD_EMPLEADO,
                    d1.KILOMETRAJE_ACTUAL,
                    IFNULL(
                        (
                            SELECT d2.KILOMETRAJE_ACTUAL
                            FROM dvn1_despachos d2
                            WHERE d2.UNIDAD = d1.UNIDAD
                              AND d2.FECHA_REGISTRO < d1.FECHA_REGISTRO
                            ORDER BY d2.FECHA_REGISTRO DESC
                            LIMIT 1
                        ),
                        0
                    ) AS `KILOMETRAJE ANTERIOR`
                FROM dvn1_despachos d1
                WHERE d1.FECHA >= %s
                  AND d1.FECHA <= %s
            ) t
            ORDER BY t.`FECHA DESPACHO` DESC
        """, (fecha_inicio, fecha_fin))

        datos = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        return columnas, datos

    finally:
        cursor.close()
        conexion.close()
