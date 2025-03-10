from flask import Blueprint, render_template, request
from iniciasesion import login_required, role_required, session
from database import get_db_connection

# Blueprint
actualizar_bp = Blueprint('actualizar_bp', __name__, template_folder='templates/operador')

@actualizar_bp.route('/gestionar_datos', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def gestionar_datos():
    db_name = "visitas"  # Base de datos a usar
    operadores = {}  # Lista de operadores por base de datos

    # Procesar solicitud POST para acciones CRUD
    if request.method == 'POST':
        action = request.form.get('action')  # Acción: add, update, delete
        id_operador = request.form.get('id_entity')  # ID del operador (solo para update/delete)
        nombre = request.form.get('nombre')  # Nombre del operador (para add/update)
        numero_contrato = request.form.get('numero_contrato')
        # Consultas según la acción
        queries = {
            'add': "INSERT INTO operadores (nombre) VALUES (%s)",
            'update': "UPDATE operadores SET nombre = %s, numero_contrato = %s WHERE id_operador = %s",
            'delete': "DELETE FROM operadores WHERE id_operador = %s",
        }

        # Validar y construir parámetros
        params = None
        if action == 'add' and nombre:
            params = (nombre,)
        elif action == 'update' and id_operador and nombre and numero_contrato:
            params = (nombre, numero_contrato, id_operador)
        elif action == 'delete' and id_operador:
            params = (id_operador,)
        else:
            return render_template('gestionar_datos.html', message="Datos insuficientes para realizar la acción.", success=False, operadores=operadores)

        # Ejecutar la consulta
        try:
            conn = get_db_connection(db_name)
            with conn.cursor() as cursor:
                cursor.execute(queries[action], params)
                conn.commit()
            message = "Operación realizada correctamente."
            success = True
        except Exception as e:
            print(f"Error en operación {action}: {e}")
            message = f"Error al realizar la operación: {e}"
            success = False
        finally:
            if 'conn' in locals():
                conn.close()

        # Refrescar operadores y mostrar mensaje
        operadores = obtener_operadores(db_name)
        return render_template('gestionar_datos.html', message=message, success=success, operadores=operadores)

    # Si es GET, cargar operadores
    operadores = obtener_operadores(db_name)
    return render_template('gestionar_datos.html', operadores=operadores, rol=session.get('rol'))


# Función para obtener operadores de la base de datos
def obtener_operadores(db_name):
    operadores = {}
    try:
        conn = get_db_connection(db_name)
        cursor = conn.cursor()  # Crear cursor manualmente
        cursor.execute("SELECT id_operador, nombre, numero_contrato FROM operadores ORDER BY id_operador")
        operadores[db_name] = [{"id_operador": row[0], "nombre": row[1], "numero_contrato": row[2]} for row in cursor.fetchall()]
        cursor.close()  # Cerrar el cursor manualmente
    except Exception as e:
        print(f"Error al recuperar operadores: {e}")
        operadores[db_name] = []
    finally:
        if 'conn' in locals():
            conn.close()
    return operadores
