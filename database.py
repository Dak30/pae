
from flask import request
import pymysql
import mysql.connector
from mysql.connector import Error as MySQLConnectorError
from pymysql.err import MySQLError as PyMySQLError
import pymysql.cursors

def get_db_connection(database_name, driver="mysql.connector"):
    try:
        if database_name != 'visitas':
            raise ValueError(f"Base de datos desconocida: {database_name}")

        if driver == "mysql.connector":
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="Pae",
                password="Pae_educacion",
                database=database_name
            )
        elif driver == "pymysql":
            conn = pymysql.connect(
                host="127.0.0.1",
                user="Pae",
                password="Pae_educacion",
                database=database_name,
                cursorclass=pymysql.cursors.DictCursor  # Agregado
            )
        else:
            raise ValueError(f"Driver desconocido: {driver}")

        return conn
    except (MySQLConnectorError, PyMySQLError) as e:
        print(f"Error al conectar con la base de datos '{database_name}' usando {driver}: {e}")
        return None

