from flask import Blueprint, render_template, request, redirect, url_for, flash
from iniciasesion import login_required, role_required, session, registrar_auditoria
from database import get_db_connection

# Blueprint para instituciones
instituciones_bp = Blueprint('instituciones_bp', __name__, template_folder='institucionesysedes')

def obtener_instituciones():
    try:
        conn = get_db_connection("visitas")
        cursor = conn.cursor()  # ← No usar "with"
        cursor.execute("SELECT id_institucion, sede_educativa, direccion, id_operador FROM instituciones")
        instituciones = cursor.fetchall()
        cursor.close() 
        # ← Cerrar el cursor manualmente
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="SELECT",
            modulo="Gestión de Instituciones",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) acceso la ventana de Instituciones ",
        )
        return instituciones
    except Exception as e:
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR",
            modulo="Gestión de Instituciones",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) acceso erroneamente la ventana de Instituciones ",
        )
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
        action = request.form.get('action')  # Acción (add, update, delete)
        id_institucion = request.form.get('id_institucion')  # ID de la institución (si aplica)
        sede_educativa = request.form.get('sede_educativa')  # Nombre de la sede
        direccion = request.form.get('direccion')  # Dirección
        id_operador = request.form.get('id_operador')  # ID del operador

        queries = {
            'add': "INSERT INTO instituciones (sede_educativa, direccion, id_operador) VALUES (%s, %s, %s)",
            'update': "UPDATE instituciones SET sede_educativa = %s, direccion = %s, id_operador = %s WHERE id_institucion = %s",
            'delete': "DELETE FROM instituciones WHERE id_institucion = %s"
        }

        if action == 'add':
            params = (sede_educativa, direccion, id_operador)
            accion_auditoria = "INSERT"
            detalle = f"Agregó la institución '{sede_educativa}' con dirección '{direccion}' y operador ID {id_operador}."
        elif action == 'update':
            params = (sede_educativa, direccion, id_operador, id_institucion)
            accion_auditoria = "UPDATE"
            detalle = f"Actualizó la institución ID {id_institucion} a '{sede_educativa}', dirección '{direccion}', operador ID {id_operador}."
        elif action == 'delete':
            params = (id_institucion,)
            accion_auditoria = "DELETE"
            detalle = f"Eliminó la institución con ID {id_institucion}."
        else:
            flash("Acción no válida.", 'error')
            return redirect(url_for('instituciones_bp.gestionar_instituciones'))

        try:
            conn = get_db_connection("visitas")
            with conn.cursor() as cursor:
                cursor.execute(queries[action], params)
                conn.commit()

                # Obtener datos del usuario en sesión
                usuario_sesion = session.get('usuario_id', 0)
                nombre_sesion = session.get('nombre', 'Desconocido')
                correo_sesion = session.get('correo', 'Sin correo')

                # Registrar auditoría con la acción real
                registrar_auditoria(
                    usuario_id=usuario_sesion,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion=accion_auditoria,  # INSERT, UPDATE o DELETE
                    modulo="Gestión de Instituciones",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) {detalle}",
                )

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

