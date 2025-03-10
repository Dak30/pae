from flask import Blueprint, render_template, request, redirect, url_for, flash
from iniciasesion import login_required, role_required, session
from database import get_db_connection

# Blueprint para instituciones
instituciones_bp = Blueprint('instituciones_bp', __name__, template_folder='institucionesysedes')

def obtener_instituciones():
    try:
        conn = get_db_connection("visitas")
        cursor = conn.cursor()  # ← No usar "with"
        cursor.execute("SELECT id_institucion, sede_educativa, direccion, id_operador FROM instituciones")
        instituciones = cursor.fetchall()
        cursor.close()  # ← Cerrar el cursor manualmente
        return instituciones
    except Exception as e:
        print(f"Error al recuperar instituciones: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()


@instituciones_bp.route('/instituciones', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def gestionar_instituciones():
    if request.method == 'POST':
        action = request.form.get('action')  # Acción (agregar, actualizar, eliminar)
        id_institucion = request.form.get('id_institucion')  # ID de la institución a editar/eliminar
        sede_educativa = request.form.get('sede_educativa')  # Nuevo nombre de la sede
        direccion = request.form.get('direccion')  # Nueva dirección
        id_operador = request.form.get('id_operador')  # Nuevo ID del operador

        # Consulta SQL para cada acción (agregar, actualizar, eliminar)
        queries = {
            'add': "INSERT INTO instituciones (sede_educativa, direccion, id_operador) VALUES (%s, %s, %s)",
            'update': "UPDATE instituciones SET sede_educativa = %s, direccion = %s, id_operador = %s WHERE id_institucion = %s",
            'delete': "DELETE FROM instituciones WHERE id_institucion = %s"
        }

        # Parámetros para cada tipo de acción
        if action == 'add':
            params = (sede_educativa, direccion, id_operador)
        elif action == 'update':
            params = (sede_educativa, direccion, id_operador, id_institucion)
        elif action == 'delete':
            params = (id_institucion,)

        try:
            conn = get_db_connection("visitas")
            with conn.cursor() as cursor:
                cursor.execute(queries[action], params)  # Ejecutar la consulta SQL
                conn.commit()
            flash("Operación realizada correctamente.", 'success')
        except Exception as e:
            flash(f"Error en la operación: {e}", 'error')
        finally:
            if 'conn' in locals():
                conn.close()
        return redirect(url_for('instituciones_bp.gestionar_instituciones'))

    # Obtener todas las instituciones para mostrarlas en la tabla
    instituciones = obtener_instituciones()
    rol = session.get('rol')  # Obtiene el rol del usuario desde la sesión
    return render_template('gestionar_instituciones.html', instituciones=instituciones, rol=rol)
