from flask import Blueprint, render_template, request
from iniciasesion import login_required, role_required, session, registrar_auditoria
from base_datos.database import get_db_connection

# Blueprint
actualizar_bp = Blueprint('actualizar_bp', __name__, template_folder='templates/operador')

@actualizar_bp.route('/gestionar_datos', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def gestionar_datos():
    db_name = "visitas"  # Base de datos a usar
    operadores = {}  # Lista de operadores por base de datos

    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

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
        detalle_accion = ""
        if action == 'add' and nombre:
            params = (nombre,)
            detalle_accion = f"El usuario '{nombre_sesion}' ({correo_sesion}) agregó un nuevo operador con nombre '{nombre}'."
        elif action == 'update' and id_operador and nombre and numero_contrato:
            params = (nombre, numero_contrato, id_operador)
            detalle_accion = f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó los datos del operador ID {id_operador}, asignándole el nombre '{nombre}' y número de contrato '{numero_contrato}'."
        elif action == 'delete' and id_operador:
            params = (id_operador,)
            detalle_accion = f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó el operador con ID {id_operador}."
        else:
            return render_template('gestionar_datos.html', message="Datos insuficientes para realizar la acción.", success=False, operadores=operadores)

        # Ejecutar la consulta
        try:
            conn = get_db_connection(db_name)
            with conn.cursor() as cursor:
                cursor.execute(queries[action], params)
                conn.commit()

            registrar_auditoria(
                usuario_id=usuario_sesion,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion=action.upper(),
                modulo="Gestión de Operadores",
                detalle_accion=detalle_accion
            )

            message = "Operación realizada correctamente."
            success = True
        except Exception as e:
            print(f"Error en operación {action}: {e}")
            message = f"Error al realizar la operación: {e}"
            success = False

            # Registrar en auditoría el error
            registrar_auditoria(
                usuario_id=usuario_sesion,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="ERROR",
                modulo="Gestión de Operadores",
                detalle_accion=f"Error al realizar la operación '{action}' para el operador. Detalles: {e}"
            )
        finally:
            if 'conn' in locals():
                conn.close()

        # Refrescar operadores y mostrar mensaje
        operadores = obtener_operadores(db_name)
        return render_template('gestionar_datos.html', message=message, success=success, operadores=operadores)

    # Si es GET, cargar operadores
    operadores = obtener_operadores(db_name)
    
    # Registrar en auditoría el acceso a la página
    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="ACCESS",
        modulo="Gestión de Operadores",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) accedió a la gestión de operadores."
    )

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
