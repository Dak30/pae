
from flask import request
import pymysql
import mysql.connector
from mysql.connector import Error as MySQLConnectorError
from pymysql.err import MySQLError as PyMySQLError
import pymysql.cursors
import os
import subprocess
import datetime

def get_db_connection(database_name, driver="mysql.connector"):
    try:
        if database_name != 'visitas':
            raise ValueError(f"Base de datos desconocida: {database_name}")

        if driver == "mysql.connector":
            conn = mysql.connector.connect(
                host="mysql",
                user="Pae",
                password="Pae_educacion",
                database=database_name
            )
        elif driver == "pymysql":
            conn = pymysql.connect(
                host="mysql",
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

def backup_database():
    """Crea un respaldo de la base de datos y lo guarda en un archivo .sql dentro del contenedor."""
    DB_HOST = "172.18.0.4"
    DB_USER = "Pae"
    DB_PASSWORD = "Pae_educacion"
    DB_NAME = "visitas"

    # Directorio donde se guardará el backup
    backup_dir = "/backups"
    os.makedirs(backup_dir, exist_ok=True)

    # Nombre del archivo con fecha y hora
    fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/backup_{DB_NAME}_{fecha_hora}.sql"

    # Comando para generar el respaldo (corrigiendo errores comunes)
    command = [
        "mysqldump",
        "-h", DB_HOST,
        "-u", DB_USER,
        f"-p{DB_PASSWORD}",
        "--databases", DB_NAME
    ]

    # Ejecutar el comando con mejor manejo de errores
    with open(backup_file, "w") as output_file:
        result = subprocess.run(command, stdout=output_file, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0 and os.path.getsize(backup_file) > 0:
        print(f"✅ Respaldo creado en: {backup_file}")
        return backup_file
    else:
        print(f"❌ Error en mysqldump: {result.stderr}")
        return None
