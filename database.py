import mysql.connector
from mysql.connector import Error, pooling

class Database:
    _pool = None

    @staticmethod
    def _get_pool():
        if Database._pool is None:
            Database._pool = pooling.MySQLConnectionPool(
                pool_name="zetatanques_pool",
                pool_size=5,
                pool_reset_session=False,
                #host="localhost",
                #user="root",
                #password="gasautoremoto",
                #database="zetatanques",
                host= "10.24.10.210",
                port= 3306,
                user="granel_fel",
                password="FEL.2019",
                database="zetatanques",
                use_pure=True,
                connection_timeout=10,
                autocommit=True,
                charset="utf8"
            )
        return Database._pool

    @staticmethod
    def get_connection():
        try:
            conexion = Database._get_pool().get_connection()

            cursor = conexion.cursor()
            cursor.execute("SET time_zone = '-06:00'")
            cursor.close()

            return conexion

        except Error as error:
            print(f"Error al conectar con MySQL: {error}")
            return None