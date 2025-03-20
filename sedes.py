from flask import Blueprint, render_template, request, redirect, url_for, flash
from iniciasesion import login_required, role_required, session, registrar_auditoria
from database import get_db_connection  # Importar la función de auditoría

# Blueprint para sedes
sedes_bp = Blueprint('sedes_bp', __name__, template_folder='templates/institucionesysedes')

def obtener_sedes():
    try:
        conn = get_db_connection("visitas")
        cursor = conn.cursor()
        cursor.execute("SELECT id_sede, nombre_sede, id_institucion, direccion, codigo, comuna, zona FROM sedes")
        sedes = cursor.fetchall()
        cursor.close()
        return sedes
    except Exception as e:
        print(f"Error al recuperar sedes: {e}")
        return []
    finally:
        if 'conn' in locals():
            conn.close()

@sedes_bp.route('/sedes', methods=['GET', 'POST'])
@login_required
@role_required('administrador')
def gestionar_sedes():
    if request.method == 'POST':
        action = request.form.get('action')
        id_sede = request.form.get('id_sede')
        nombre_sede = request.form.get('nombre_sede')
        id_institucion = request.form.get('id_institucion')
        direccion = request.form.get('direccion')
        codigo = request.form.get('codigo')
        comuna = request.form.get('comuna')
        zona = request.form.get('zona')

        queries = {
            'add': "INSERT INTO sedes (nombre_sede, id_institucion, direccion, codigo, comuna, zona) VALUES (%s, %s, %s, %s, %s, %s)",
            'update': "UPDATE sedes SET nombre_sede = %s, id_institucion = %s, direccion = %s, codigo = %s, comuna = %s, zona = %s WHERE id_sede = %s",
            'delete': "DELETE FROM sedes WHERE id_sede = %s"
        }

        params = (nombre_sede, id_institucion, direccion, codigo, comuna, zona) if action == 'add' else (nombre_sede, id_institucion, direccion, codigo, comuna, zona, id_sede) if action == 'update' else (id_sede,)

        try:
            conn = get_db_connection("visitas")
            with conn.cursor() as cursor:
                if action == 'update':
                    # Obtener datos antes de la actualización
                    cursor.execute("SELECT nombre_sede, id_institucion, direccion, codigo, comuna, zona FROM sedes WHERE id_sede = %s", (id_sede,))
                    sede_anterior = cursor.fetchone()

                cursor.execute(queries[action], params)
                conn.commit()

                # Registrar auditoría
                usuario_sesion = session.get('usuario_id', 0)
                nombre_sesion = session.get('nombre', 'Desconocido')
                correo_sesion = session.get('correo', 'Sin correo')

                if action == 'add':
                    registrar_auditoria(
                        usuario_id=usuario_sesion,
                        nombre_usuario=nombre_sesion,
                        correo=correo_sesion,
                        accion="INSERT",
                        modulo="Gestión de Sedes",
                        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) agregó la sede '{nombre_sede}' en la institución {id_institucion}."
                    )
                elif action == 'update':
                    cambios = []
                    campos = ["nombre_sede", "id_institucion", "direccion", "codigo", "comuna", "zona"]
                    valores_nuevos = [nombre_sede, id_institucion, direccion, codigo, comuna, zona]

                    for i, campo in enumerate(campos):
                        if sede_anterior[i] != valores_nuevos[i]:
                            cambios.append(f"{campo}: '{sede_anterior[i]}' → '{valores_nuevos[i]}'")

                    if cambios:
                        registrar_auditoria(
                            usuario_id=usuario_sesion,
                            nombre_usuario=nombre_sesion,
                            correo=correo_sesion,
                            accion="UPDATE",
                            modulo="Gestión de Sedes",
                            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó la sede '{nombre_sede}': {', '.join(cambios)}."
                        )
                elif action == 'delete':
                    registrar_auditoria(
                        usuario_id=usuario_sesion,
                        nombre_usuario=nombre_sesion,
                        correo=correo_sesion,
                        accion="DELETE",
                        modulo="Gestión de Sedes",
                        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó la sede con ID {id_sede}."
                    )

            flash("Operación realizada correctamente.", 'success')
        except Exception as e:
            flash(f"Error en la operación: {e}", 'error')
        finally:
            if 'conn' in locals():
                conn.close()
        return redirect(url_for('sedes_bp.gestionar_sedes'))

    sedes = obtener_sedes()
    rol = session.get('rol')
    return render_template('gestionar_sedes.html', sedes=sedes, rol=rol)
