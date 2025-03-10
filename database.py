import pymysql
import mysql.connector
from mysql.connector import Error

def get_db_connection(database_name):
    try:
        
        if database_name == 'visitas':
            # Configuración para visitas usando mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="Pae",
                password="Pae_educacion",
                database=database_name
            )
        else:
            raise ValueError(f"Base de datos desconocida: {database_name}")

        return conn
    except (pymysql.MySQLError, Error) as e:
        print(f"Error al conectar con la base de datos '{database_name}': {e}")
        return None
