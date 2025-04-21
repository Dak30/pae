
from iniciasesion import login_required, session, role_required, registrar_auditoria
from flask import  Blueprint, render_template, request, jsonify, redirect, url_for,session, flash, make_response, send_file, current_app
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from reportlab.lib.units import inch
import os
from werkzeug.utils import secure_filename

from base_datos.database import get_db_connection

# logging.basicConfig(level=logging.DEBUG)

verificacion_bp = Blueprint('verificacion_bp', __name__, template_folder='templates/verificacion')


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Función para validar archivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
def fetch_tiporacion():
    conn = get_db_connection('visitas')
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_tipo_racion, descripcion FROM tiporacion")    
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
        
def fetch_operador():
    conn = get_db_connection('visitas')
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_operador, nombre, numero_contrato FROM operadores ORDER BY id_operador ASC")
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

@verificacion_bp.route('/instituciones/<int:id_operador>')
def get_instituciones(id_operador):
    instituciones = fetch_instituciones(id_operador)
    return jsonify(instituciones)


def fetch_instituciones(id_operador):
    conn = get_db_connection('visitas')
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_institucion, sede_educativa FROM instituciones WHERE id_operador = %s", (id_operador,))
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
        
@verificacion_bp.route('/sedes/<int:id_institucion>', methods=['GET'])
def get_sedes_by_institucion(id_institucion):
    conn = get_db_connection('visitas')
    if conn is None:
        return jsonify([]), 500
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_sede, nombre_sede FROM sedes WHERE id_institucion = %s", (id_institucion,))
        sedes = cursor.fetchall()
        return jsonify(sedes)
    except Error as err:
        print(f"Error: {err}")
        return jsonify([]), 500
    finally:
        cursor.close()
        conn.close()
        
@verificacion_bp.route('/verificacion_menu', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador', 'nutricionista')
def verificacion_menu():
    
    id_operador = None
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    if request.method == 'POST':
        try:
            # Obtener los valores básicos
            fecha_visita = request.form.get('fecha_visita')
            hora_visita = request.form.get('hora_visita')
            zona = request.form.get('zona')
            jornada = request.form.get('jornada')
            contrato = request.form.get('numero_contrato')
            

            # Verificar si viene de GET, POST o sesión
            if 'id_operador' in request.args:
                id_operador = request.args.get('id_operador')
            elif 'id_operador' in request.form:
                id_operador = request.form.get('id_operador')
            elif 'id_operador' in session:
                id_operador = session.get('id_operador')
                
            instituciones = fetch_instituciones(id_operador) if id_operador else []

            institucion_id = request.form.getlist('instituciones[]')[0] if request.form.getlist('instituciones[]') else None
            sede_id = request.form.get(f'sede_{institucion_id}')

            if not sede_id:
                raise ValueError("Debe seleccionar una sede obligatoriamente.")
            
            tipo_racion_id = request.form.get('tipo_racion_id')
            numero_menu_oficial = request.form.get('numero_menu_oficial')
            numero_menu_intercambio = request.form.get("numero_menu_intercambio", "").strip()

            # Si el valor es una cadena vacía, cambia a None (para que MySQL use el valor por defecto)
            if numero_menu_intercambio == "":
                numero_menu_intercambio = None
            else:
                numero_menu_intercambio = int(numero_menu_intercambio)  # Convierte a entero
                
            nivel_1 = int(request.form.get('nivel_1') or 0)
            nivel_2 = int(request.form.get('nivel_2') or 0)
            nivel_3 = int(request.form.get('nivel_3') or 0)
            nivel_4 = int(request.form.get('nivel_4') or 0)
            nivel_5 = int(request.form.get('nivel_5') or 0)
            total = nivel_1 + nivel_2 + nivel_3 + nivel_4 + nivel_5
            observacion_general = request.form.get('observacion_general')
            hallazgo = request.form.get('hallazgo')

            # Imprimir para verificar datos básicos
            print("Datos básicos recibidos:", {
                "fecha_visita": fecha_visita,
                "hora_visita": hora_visita,
                "zona": zona,
                "jornada": jornada,
                "contrato": contrato,
                "id_operador": id_operador,
                "institucion_id": institucion_id,
                "sede_id": sede_id,
                "tipo_racion_id": tipo_racion_id,
                "numero_menu_oficial": numero_menu_oficial,
                "numero_menu_intercambio": numero_menu_intercambio,
                "total_niveles": total,
                "observacion_general": observacion_general,
                "hallazgo": hallazgo
            })

            conn = get_db_connection('visitas')
            conn.autocommit = True
            if conn:
                cursor = conn.cursor()

                # Inserción en la tabla `verificacion_menu`
                query_verificacion_menu = """
                    INSERT INTO verificacion_menu (
                        fecha_visita, hora_visita, zona, jornada, contrato,
                        id_operador, institucion_id, sede_id, tipo_racion_id,
                        numero_menu_oficial, numero_menu_intercambio,
                        nivel_1, nivel_2, nivel_3, nivel_4, nivel_5,
                        observacion_general, hallazgo
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values_verificacion_menu = (
                    fecha_visita, hora_visita, zona, jornada, contrato, 
                    id_operador, institucion_id, sede_id, tipo_racion_id, 
                    numero_menu_oficial, numero_menu_intercambio, 
                    nivel_1, nivel_2, nivel_3, nivel_4, nivel_5, 
                    observacion_general, hallazgo
                )
                cursor.execute(query_verificacion_menu, values_verificacion_menu)
                verificacion_menu_id = cursor.lastrowid

                # Capturar listas de detalles
                componentes = request.form.getlist('componentes[]')
                valor_cumplimiento = request.form.getlist('valor_cumplimiento[]')
                menu_oficial = request.form.getlist('menu_oficial[]')
                menu_intercambio = request.form.getlist('menu_intercambio[]') or None

                if tipo_racion_id == "1":  # Industrializado
                    # Código para Industrializado (ya incluido en la versión anterior)

                    fecha_vencimiento = request.form.getlist('fecha_vencimiento[]')
                    lote = request.form.getlist('lote[]')
                    peso_nivel_escolar_1 = request.form.getlist('peso_nivel_escolar_1[]')
                    peso_nivel_escolar_2 = request.form.getlist('peso_nivel_escolar_2[]')
                    peso_nivel_escolar_3 = request.form.getlist('peso_nivel_escolar_3[]')
                    peso_nivel_escolar_4 = request.form.getlist('peso_nivel_escolar_4[]')
                    peso_nivel_escolar_5 = request.form.getlist('peso_nivel_escolar_5[]')

                    # Imprimir datos de detalle para Industrializado
                    print("Datos de detalle para Industrializado:", {
                        "componentes": componentes,
                        "valor_cumplimiento": valor_cumplimiento,
                        "menu_oficial": menu_oficial,
                        "menu_intercambio": menu_intercambio,
                        "fecha_vencimiento": fecha_vencimiento,
                        "lote": lote,
                        "peso_nivel_escolar_1": peso_nivel_escolar_1,
                        "peso_nivel_escolar_2": peso_nivel_escolar_2,
                        "peso_nivel_escolar_3": peso_nivel_escolar_3,
                        "peso_nivel_escolar_4": peso_nivel_escolar_4,
                        "peso_nivel_escolar_5": peso_nivel_escolar_5
                    })

                    query_detalle = """
                        INSERT INTO verificacion_menu_detalles (
                            verificacion_menu_id, componentes, valor_cumplimiento,
                            menu_oficial, menu_intercambio, fecha_vencimiento, lote,
                            peso_nivel_escolar_1, peso_nivel_escolar_2, peso_nivel_escolar_3,
                            peso_nivel_escolar_4, peso_nivel_escolar_5
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    for i in range(len(componentes)):
                        values_detalle = (
                            verificacion_menu_id, componentes[i], int(valor_cumplimiento[i]),
                            menu_oficial[i], menu_intercambio[i] or None, fecha_vencimiento[i] or None,
                            lote[i] or None, peso_nivel_escolar_1[i] or 0, peso_nivel_escolar_2[i] or 0,
                            peso_nivel_escolar_3[i] or 0, peso_nivel_escolar_4[i] or 0,
                            peso_nivel_escolar_5[i] or 0
                        )
                        cursor.execute(query_detalle, values_detalle)

                else:  # Otros tipos de ración
                    propiedades_organolepticas = request.form.getlist('propiedades_organolepticas[]')
                    observaciones = request.form.getlist('observacion[]')

                    # Imprimir datos de detalle para otros tipos de ración
                    print("Datos de detalle para otros tipos de ración:", {
                        "componentes": componentes,
                        "valor_cumplimiento": valor_cumplimiento,
                        "menu_oficial": menu_oficial,
                        "menu_intercambio": menu_intercambio,
                        "propiedades_organolepticas": propiedades_organolepticas,
                        "observaciones": observaciones
                    })

                    query_detalle = """
                        INSERT INTO verificacion_menu_detalles (
                            verificacion_menu_id, componentes, valor_cumplimiento,
                            menu_oficial, menu_intercambio, propiedades_organolepticas, observacion
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    for i in range(len(componentes)):
                        values_detalle = (
                            verificacion_menu_id, componentes[i], int(valor_cumplimiento[i]),
                            menu_oficial[i], menu_intercambio[i], 
                            int(propiedades_organolepticas[i]) if propiedades_organolepticas else None, 
                            observaciones[i] or None
                        )
                        cursor.execute(query_detalle, values_detalle)
                        
                # Calcular el puntaje de cumplimiento
                cumple_count = 0  # Contador para los valores que cumplen (1)
                total_validos = 0  # Contador para los valores que cuentan (1 y 0, excluyendo 2)

                for valor in valor_cumplimiento:
                    if valor != '2':  # Excluir "No Aplica"
                        total_validos += 1
                        cumple_count += int(valor)  # Sumar solo si cumple (1)

                puntaje_cumplimiento = (cumple_count / total_validos) * 100 if total_validos > 0 else 0

                # Clasificación del puntaje de cumplimiento
                if puntaje_cumplimiento >= 80:
                    clasificacion = "Adecuado"
                elif 61 <= puntaje_cumplimiento <= 79:
                    clasificacion = "Regular"
                else:
                    clasificacion = "Malo"

                # Insertar puntaje y clasificación en la tabla de puntaje de cumplimiento
                puntaje_query = """
                    INSERT INTO puntaje_cumplimiento (verificacion_menu_id, puntaje, clasificacion)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(puntaje_query, (verificacion_menu_id, puntaje_cumplimiento, clasificacion))
                
                # rol_usuario = session.get('rol')
                
                # Guardar archivos adjuntos
                archivos = request.files.getlist('archivos[]')

                print(f"Archivos recibidos: {[archivo.filename for archivo in archivos]}")  # Ver lista de archivos

                if archivos:  # Verifica que se haya subido al menos un archivo
                    upload_folder = os.path.join(current_app.root_path, 'static/uploads/verificacion')  

                    # Asegurar que la carpeta de destino existe
                    os.makedirs(upload_folder, exist_ok=True)

                    for archivo in archivos:
                        if archivo and allowed_file(archivo.filename):
                            filename = secure_filename(archivo.filename.lower())  # Convertir a minúsculas por compatibilidad
                            filepath = os.path.join(upload_folder, filename)

                            print(f"Guardando archivo en: {filepath}")  # Ver ruta completa

                            archivo.save(filepath)

                            # Verificar si el archivo realmente se guardó
                            if os.path.exists(filepath):
                                print(f"Archivo guardado exitosamente: {filename}")
                            else:
                                print(f"Error: El archivo {filename} no se guardó.")

                            # Guardar solo la ruta relativa en la BD
                            ruta_relativa = f"static/uploads/verificacion/{filename}"

                            # Insertar en la base de datos
                            file_query = """
                                INSERT INTO archivos_verificacion (verificacion_id, nombre_archivo, ruta_archivo)
                                VALUES (%s, %s, %s)
                            """
                            cursor.execute(file_query, (verificacion_menu_id, filename, ruta_relativa))
                            print(f"Archivo {filename} registrado en la BD con ruta {ruta_relativa}")
                
                flash("Verificación de menú guardada con éxito.", "success")
                
                # Obtener el ID recién insertado
                print(f"ID Verificacion de Menu Guardado es: {verificacion_menu_id}")
                
                registrar_auditoria(
                    usuario_id=usuario_sesion,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="INSERT",
                    modulo="Gestión de Verificación de Menú",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los datos en el formulario de verificación de menú."
                )
            
                # Redirigir a la página de detalles de verificación con el ID obtenido
                return redirect(url_for('verificacion_bp.detalles_verificacion', id=verificacion_menu_id))
                
            else:
                registrar_auditoria(
                    usuario_id=usuario_sesion,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="ERROR",
                    modulo="Gestión de Verificación de Menú",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó erroneamente los datos en el formulario de verificación de menú."
                )
                 # Redirigir a la página de detalles de verificación con el ID obtenido
                return redirect(url_for('verificacion_bp.detalles_verificacion', id=verificacion_menu_id))

        except Exception as e:
            print(f"Error al procesar el formulario: {repr(e)}")
            registrar_auditoria(
                usuario_id=usuario_sesion,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="ERROR",
                modulo="Gestión de Verificación de Menú",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó erroneamente los datos en el formulario de verificación de menú. Detalles de error: {repr(e)}"
            )
            flash(f"Ocurrió un error en el procesamiento del formulario: {e}", "danger")
            return f"Error en el procesamiento del formulario: {e}"

        finally:
            if conn:
                cursor.close()
                conn.close()

    # Obtener datos para el formulario en caso de GET
    # instituciones = fetch_instituciones(id_operador)
    # Si no hay operador, inicializar instituciones como lista vacía
    instituciones = fetch_instituciones(id_operador) if id_operador else []
    tiporacion = fetch_tiporacion()
    operadores = fetch_operador()
    today_date = datetime.today().strftime('%Y-%m-%d')

    return render_template(
        'verificacion_menu.html', instituciones=instituciones, tiporacion=tiporacion, operadores=operadores, today_date=today_date, rol=session.get('rol'), usuario=session.get('nombre'))


@verificacion_bp.route('/eliminar_verificacion/<int:id>', methods=['DELETE'])
def eliminar_verificacion(id):
    conexion = get_db_connection('visitas')  # Usar la función ya existente
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    if conexion is None:
        return jsonify({'success': False, 'message': 'Error de conexión con la base de datos'}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM verificacion_menu WHERE id = %s", (id,))
        conexion.commit()
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="DELETE",
            modulo="Gestión de Verificación de Menúa",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó el numero de ID {id} verificación de menú."
        )
        return jsonify({'success': True, 'message': 'Verificación eliminada correctamente'}), 200

    except mysql.connector.Error as e:
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR",
            modulo="Gestión de Verificación de Menú",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó erroneamente el numero de ID {id} verificación de menú. Error: {str(e)}"
        )
        return jsonify({'success': False, 'message': f'Error al eliminar la verificación: {e}'}), 500

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


import pandas as pd
from io import BytesIO

def exportar_verificacion_menu(id_verificacion=None, institucion_id=None, fecha_inicio=None, fecha_fin=None):
    conexion = get_db_connection('visitas')
    cursor = conexion.cursor()

    query = """
        SELECT 
            vm.id, vm.fecha_visita, vm.hora_visita, vm.zona, vm.jornada, vm.contrato, 
            o.nombre AS nombre_operador, i.sede_educativa AS nombre_institucion, s.nombre_sede AS nombre_sede,
            tr.descripcion AS descripcion_tipo_racion, vm.numero_menu_oficial, 
            vm.numero_menu_intercambio, vm.observacion_general, vm.hallazgo, 
            vm.nivel_1, vm.nivel_2, vm.nivel_3, vm.nivel_4, vm.nivel_5, vm.total,
            p.puntaje, p.clasificacion,
            d.componentes, d.valor_cumplimiento, d.menu_oficial, d.menu_intercambio,
            d.propiedades_organolepticas, d.observacion, d.fecha_vencimiento, 
            d.lote, d.peso_nivel_escolar_1, d.peso_nivel_escolar_2, 
            d.peso_nivel_escolar_3, d.peso_nivel_escolar_4, d.peso_nivel_escolar_5, 
            f.nombre_representante, f.cargo_representante,
            f.nombre_funcionario, f.nombre_operador, f.cargo_operador
        FROM verificacion_menu vm
        LEFT JOIN operadores o ON vm.id_operador = o.id_operador
        LEFT JOIN instituciones i ON vm.institucion_id = i.id_institucion
        LEFT JOIN tiporacion tr ON vm.tipo_racion_id = tr.id_tipo_racion
        LEFT JOIN sedes s ON vm.sede_id = s.id_sede
        LEFT JOIN puntaje_cumplimiento p ON vm.id = p.verificacion_menu_id
        LEFT JOIN firmas_verificacion f ON vm.id = f.id_verificacion
        LEFT JOIN verificacion_menu_detalles d ON vm.id = d.verificacion_menu_id
    """

    filtros = []
    params = []

    # Filtros opcionales
    if id_verificacion:
        filtros.append("vm.id = %s")
        params.append(id_verificacion)
    if institucion_id:
        filtros.append("i.id_institucion = %s")
        params.append(institucion_id)
    if fecha_inicio and fecha_fin:
        filtros.append("vm.fecha_visita BETWEEN %s AND %s")
        params.extend([fecha_inicio, fecha_fin])

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    cursor.execute(query, params)
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not datos:
        return None, "No se encontraron detalles para la consulta."

    columnas = [
        "ID", "Fecha Visita", "Hora Visita", "Zona", "Jornada", "Contrato", "Operador",
        "Institución", "Sede", "Tipo Ración", "Menú Oficial", "Menú Intercambio", "Novedades", "Hallazgo",
        "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5", "Total",
        "Puntaje Cumplimiento", "Clasificación Cumplimiento",
        "Componentes", "Valor Cumplimiento", "Menú Oficial Detalle", "Menú Intercambio Detalle", "Propiedades Organolépticas", 
        "Observación Detalle", "Fecha Vencimiento", "Lote", "Peso Nivel 1", "Peso Nivel 2", "Peso Nivel 3", "Peso Nivel 4", "Peso Nivel 5",
        "Nombre Representante", "Cargo Representante", "Nombre Funcionario", "Nombre Operador", "Cargo Operador"
    ]

    df = pd.DataFrame(datos, columns=columnas)

    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)

    return output, "verificacion_menu.xlsx"


@verificacion_bp.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    id_verificacion = request.args.get('id_verificacion')
    institucion_id = request.args.get('institucion_id')
    fecha_inicio = request.args.get('fecha_inicio')  # Formato: 'YYYY-MM-DD'
    fecha_fin = request.args.get('fecha_fin')
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

    output, filename = exportar_verificacion_menu(id_verificacion, institucion_id, fecha_inicio, fecha_fin)
    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="DOWNLOAD",
        modulo="Gestión de Verificación de Menú",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) descargó el archivo Excel el numero de ID {id} verificación de menú."
    )

    if output is None:
        return jsonify({"error": "No se encontraron datos para exportar"}), 404

    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@verificacion_bp.route('/lista_verificacion', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador', 'nutricionista')
def lista_verificacion():
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    try:
        conn = get_db_connection('visitas')
        cursor = conn.cursor()
        
        # Consulta para obtener la lista de verificación
        query = """
            SELECT 
                vm.id, 
                vm.fecha_visita, 
                vm.hora_visita, 
                vm.zona, 
                vm.jornada, 
                vm.contrato, 
                operadores.nombre
            FROM 
                verificacion_menu vm
            JOIN 
                operadores ON vm.id_operador = operadores.id_operador
        """
        cursor.execute(query)
        verificacion_items = cursor.fetchall()  # Obtener todos los resultados

        # Mapeo de los resultados a un formato de diccionario
        verificacion_items = [
            {
                'id': item[0],
                'fecha_visita': item[1],
                'hora_visita': item[2],
                'contrato': item[5],
                'nombre': item[6]
            }
            for item in verificacion_items
        ]
        
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="SELECT",
            modulo="Gestión de Verificación de Menú",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) acessó la lista de verificación de menú."
        )


        return render_template('lista_verificacion.html', verificacion_items=verificacion_items, rol = session.get("rol"))

    except Exception as e:
        print(f"Error al obtener la lista de verificación: {e}")
        flash("Ocurrió un error al obtener la lista de verificación.", "danger")
        return redirect(url_for('iniciasesion_bp.dashboard_supervisor'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
from flask import send_from_directory



@verificacion_bp.route('/uploads/verificacion/<path:filename>', methods=['GET'])
@login_required
def upload_file(filename):
    upload_folder = os.path.join(current_app.root_path, 'static/uploads/verificacion')
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="SELECT",
        modulo="Gestión de Verificación de Menú",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) descargó los archivos {filename} de verificación de menú."
    )

    if not os.path.isfile(os.path.join(upload_folder, filename)):
        return "Archivo no encontrado.", 404

    return send_from_directory(upload_folder, filename)


from reportlab.graphics.barcode import code128
from io import BytesIO
from reportlab.lib.pagesizes import letter, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepInFrame,  Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import date
from reportlab.graphics.shapes import Drawing

@verificacion_bp.route('/detalles_verificacion/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador', 'nutricionista')
def detalles_verificacion(id):
    conn = None
    cursor = None
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    try:
        # Establecer conexión
        conn = get_db_connection('visitas')
        cursor = conn.cursor()

        # Consulta principal con JOIN para obtener nombres en lugar de IDs
        query = """
            SELECT 
                vm.id, 
                vm.fecha_visita, 
                vm.hora_visita, 
                vm.zona, 
                vm.jornada, 
                vm.contrato, 
                o.nombre AS nombre_operador, 
                i.sede_educativa AS nombre_institucion, 
                tr.descripcion AS descripcion_tipo_racion,
                vm.numero_menu_oficial, 
                vm.numero_menu_intercambio, 
                vm.observacion_general,                 
                s.nombre_sede AS nombre_sede,
                vm.nivel_1, 
                vm.nivel_2, 
                vm.nivel_3, 
                vm.nivel_4, 
                vm.nivel_5,
                vm.total,
                vm.hallazgo
            FROM verificacion_menu vm
            LEFT JOIN operadores o ON vm.id_operador = o.id_operador
            LEFT JOIN instituciones i ON vm.institucion_id = i.id_institucion
            LEFT JOIN tiporacion tr ON vm.tipo_racion_id = tr.id_tipo_racion
            LEFT JOIN sedes s ON vm.sede_id = s.id_sede
            WHERE vm.id = %s
        """
        cursor.execute(query, (id,))
        verificacion = cursor.fetchone()

        if not verificacion:
            flash("No se encontraron detalles para esta verificación.", "danger")
            return redirect(url_for('iniciasesion_bp.dashboard_supervisor'))

        niveles = {
            "nivel_1": verificacion[13],
            "nivel_2": verificacion[14],
            "nivel_3": verificacion[15],
            "nivel_4": verificacion[16],
            "nivel_5": verificacion[17],
            "total": verificacion[18],
        }

        # Verificar si el tipo de ración es industrializado
        es_racion_industrializado = str(verificacion[8]).lower() == "industrializado"

        # Consulta de detalles
        detalles_query = """
            SELECT 
                componentes, 
                valor_cumplimiento, 
                menu_oficial, 
                menu_intercambio,
                propiedades_organolepticas, 
                observacion,
                fecha_vencimiento, 
                lote, 
                peso_nivel_escolar_1, 
                peso_nivel_escolar_2, 
                peso_nivel_escolar_3, 
                peso_nivel_escolar_4, 
                peso_nivel_escolar_5
            FROM verificacion_menu_detalles
            WHERE verificacion_menu_id = %s
        """
        cursor.execute(detalles_query, (id,))
        detalles = cursor.fetchall()

        # Reemplazar valores None con "N/A"
        detalles_limpios = [
            tuple("N/A" if col is None else col for col in fila)
            for fila in detalles
        ]

        # Obtener puntaje de cumplimiento y clasificación
        cursor.execute("""
            SELECT puntaje, clasificacion 
            FROM puntaje_cumplimiento 
            WHERE verificacion_menu_id = %s
        """, (id,))
        puntaje_data = cursor.fetchone()
        puntaje_cumplimiento = puntaje_data[0] if puntaje_data else "N/A"
        clasificacion_cumplimiento = puntaje_data[1] if puntaje_data else "N/A"
        
        # Primera consulta
        archivos_query ="""
            SELECT nombre_archivo 
            FROM archivos_verificacion 
            WHERE verificacion_id = %s
        """
        cursor.execute(archivos_query, (id,))
        archivos_verificacion = [fila[0] for fila in cursor.fetchall()]  # Lista con nombres de archivos

        print("Archivos encontrados:", archivos_verificacion)  # Verifica qué archivos se obtienen

        if not archivos_verificacion:
            print("No hay archivos disponibles.")  # Debugging: Verifica si la lista está vacía


        detalles_firmas = """
            SELECT 
                nombre_representante,
                cargo_representante,
                nombre_funcionario, 
                nombre_operador,
                cargo_operador,
                cedula_operador
            FROM firmas_verificacion
            WHERE id_verificacion = %s
        """
        cursor.execute(detalles_firmas, (id,))
        firmas = cursor.fetchone()
        
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="SELECT",
            modulo="Gestión de Verificación de Menú",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó con el numero ID {id} de verificación de menú."
        )


        # Manejo para la generación del PDF en POST
        if request.method == 'POST':
            accion = request.form.get('accion')
            nombre_representante = request.form.get('nombre_representante', 'No especificado')
            cargo_representante = request.form.get('cargo_representante', 'No especificado')
            nombre_funcionario = request.form.get('nombre_funcionario', 'No especificado')
            nombre_operador = request.form.get('nombre_operador', 'No especificado')
            cargo_operador = request.form.get('cargo_operador', 'No especificado')
            cedula_operador = request.form.get('cedula_operador', 'No especificado')
            
            if accion == 'guardar':
                                
                try:
                    conn = get_db_connection('visitas')
                    
                    if conn.is_connected():
                        cursor = conn.cursor()

                        try:
                            # Verificar si ya existe una firma para el mismo id_verificacion
                            sql_check = """
                                SELECT COUNT(*) FROM firmas_verificacion 
                                WHERE id_verificacion = %s
                            """
                            cursor.execute(sql_check, (id,))
                            firma_existe = cursor.fetchone()[0]  # Obtener el número de firmas existentes

                            if firma_existe == 0:  # Si no existe, insertarla
                                sql_insert_firma = """
                                    INSERT INTO firmas_verificacion 
                                    (id_verificacion, nombre_representante, cargo_representante, nombre_funcionario, nombre_operador, cargo_operador, cedula_operador)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(sql_insert_firma, (
                                    id, 
                                    nombre_representante, 
                                    cargo_representante, 
                                    nombre_funcionario, 
                                    nombre_operador, 
                                    cargo_operador,
                                    cedula_operador
                                ))
                                conn.commit()
                                
                                registrar_auditoria(
                                    usuario_id=usuario_sesion,
                                    nombre_usuario=nombre_sesion,
                                    correo=correo_sesion,
                                    accion="INSERT",
                                    modulo="Gestión de Verificación de Menú",
                                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los datos con el numero ID {id} de verificación de menú."
                                )
                                flash('Firma registrada exitosamente.', 'success')
                            else:
                                registrar_auditoria(
                                    usuario_id=usuario_sesion,
                                    nombre_usuario=nombre_sesion,
                                    correo=correo_sesion,
                                    accion="INSERT EXISTS",
                                    modulo="Gestión de Verificación de Menú",
                                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres exisstentes con el numero ID {id} de verificación de menú."
                                )
                                flash('⚠️ Ya existe una firma para esta verificación. No se puede registrar nuevamente.', 'warning')

                        except Error as e:
                            registrar_auditoria(
                                usuario_id=usuario_sesion,
                                nombre_usuario=nombre_sesion,
                                correo=correo_sesion,
                                accion="ERROR",
                                modulo="Gestión de Verificación de Menú",
                                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó erroneamente los nombres exisstentes con el numero ID {id} de verificación de menú. Deatlles de Error:  {e}"
                            )
                            print(f"Error al ejecutar la consulta: {e}")
                            
                            flash(f'Error al insertar las firmas: {e}', 'danger')
                        finally:
                            cursor.close()  # Cerrar el cursor
                            conn.close()  # Cerrar la conexión

                    else:
                        registrar_auditoria(
                            usuario_id=usuario_sesion,
                            nombre_usuario=nombre_sesion,
                            correo=correo_sesion,
                            accion="ERROR",
                            modulo="Gestión de Verificación de Menú",
                            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) cayó la conexion"
                        )
                        flash('No se pudo conectar a la base de datos.', 'danger')

                except Error as e:
                    registrar_auditoria(
                        usuario_id=usuario_sesion,
                        nombre_usuario=nombre_sesion,
                        correo=correo_sesion,
                        accion="ERROR",
                        modulo="Gestión de Verificación de Menú",
                        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) tuvo el error general: {e}"
                    )
                    print(f"Error de conexión a la base de datos: {e}")
                    flash(f'Error de conexión a la base de datos: {e}', 'danger')
                    
                return redirect(url_for('verificacion_bp.detalles_verificacion', id=id))

            elif accion == 'pdf':
                
                try:
                    conn = get_db_connection('visitas')
                    
                    if conn.is_connected():
                        cursor = conn.cursor()

                        try:
                            # Verificar si ya existe una firma para el mismo id_verificacion
                            sql_check = """
                                SELECT COUNT(*) FROM firmas_verificacion 
                                WHERE id_verificacion = %s
                            """
                            cursor.execute(sql_check, (id,))
                            firma_existe = cursor.fetchone()[0]  # Obtener el número de firmas existentes

                            if firma_existe == 0:  # Si no existe, insertarla
                                sql_insert_firma = """
                                    INSERT INTO firmas_verificacion 
                                    (id_verificacion, nombre_representante, cargo_representante, nombre_funcionario, nombre_operador, cargo_operador, cedula_operador)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(sql_insert_firma, (
                                    id, 
                                    nombre_representante, 
                                    cargo_representante, 
                                    nombre_funcionario, 
                                    nombre_operador, 
                                    cargo_operador,
                                    cedula_operador
                                ))
                                conn.commit()
                                
                                registrar_auditoria(
                                    usuario_id=usuario_sesion,
                                    nombre_usuario=nombre_sesion,
                                    correo=correo_sesion,
                                    accion="INSERT",
                                    modulo="Gestión de Verificación de Menú",
                                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los datos con el numero ID {id} de verificación de menú."
                                )
                                flash('Firma registrada exitosamente.', 'success')
                            else:
                                registrar_auditoria(
                                    usuario_id=usuario_sesion,
                                    nombre_usuario=nombre_sesion,
                                    correo=correo_sesion,
                                    accion="INSERT EXISTS",
                                    modulo="Gestión de Verificación de Menú",
                                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres exisstentes con el numero ID {id} de verificación de menú."
                                )
                                flash('⚠️ Ya existe una firma para esta verificación. No se puede registrar nuevamente.', 'warning')

                        except Error as e:
                            registrar_auditoria(
                                usuario_id=usuario_sesion,
                                nombre_usuario=nombre_sesion,
                                correo=correo_sesion,
                                accion="ERROR",
                                modulo="Gestión de Verificación de Menú",
                                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó erroneamente los nombres exisstentes con el numero ID {id} de verificación de menú. Deatlles de Error:  {e}"
                            )
                            print(f"Error al ejecutar la consulta: {e}")
                            
                            flash(f'Error al insertar las firmas: {e}', 'danger')
                        finally:
                            cursor.close()  # Cerrar el cursor
                            conn.close()  # Cerrar la conexión
                except Error as e:
                    registrar_auditoria(
                        usuario_id=usuario_sesion,
                        nombre_usuario=nombre_sesion,
                        correo=correo_sesion,
                        accion="ERROR",
                        modulo="Gestión de Verificación de Menú",
                        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) tuvo el error general: {e}"
                    )
                    print(f"Error de conexión a la base de datos: {e}")
                    flash(f'Error de conexión a la base de datos: {e}', 'danger')
                # Crear PDF
                buffer = BytesIO()
                pdf = SimpleDocTemplate(
                    buffer,
                    pagesize=portrait(letter),
                    rightMargin=30,
                    leftMargin=30,
                    topMargin=30,
                    bottomMargin=30
                )
                styles = getSampleStyleSheet()
                elements = []

                # Generar el código de barras
                barcode_data = f"V{verificacion[0]}_{verificacion[1].strftime('%Y%m%d') if isinstance(verificacion[1], date) else verificacion[1]}"
                barcode = code128.Code128(barcode_data, barWidth=0.02 * inch, barHeight=0.5 * inch)  # Ajuste de tamaño

                # Texto debajo del código de barras
                barcode_text = f"V{verificacion[0]}_{verificacion[1].strftime('%Y-%m-%d')}"

                # Crear un estilo centrado para el texto
                styles = getSampleStyleSheet()
                barcode_text_style = ParagraphStyle(
                    'BarcodeText',
                    parent=styles['Normal'],
                    fontSize=10,
                    alignment=1,  # Centrado
                    textColor=colors.black
                )

                # Crear un contenedor con el código de barras y el texto
                barcode_frame = [
                    barcode,
                    Spacer(1, 4),  # Espaciado pequeño entre el código de barras y el texto
                    Paragraph(barcode_text, barcode_text_style)
                ]

                # Dimensiones del marco
                frame_width, frame_height = 220, 100

                # Crear el documento PDF
                doc = SimpleDocTemplate("barcode_output.pdf", pagesize=letter)
                elements = [KeepInFrame(frame_width, frame_height, barcode_frame, mode='shrink')]
                
                
            # Crear la imagen del logo
                logo = Image("static/images/cali.png", width=70, height=50)  # Tamaño ajustado

                # Crear una tabla con dos columnas: Título (centro) y Logo (derecha)
                header_table = Table([[Paragraph("Acta de Verificación de Menú", styles['Title']), logo]], colWidths=[400, 60])

                # Aplicar estilos a la tabla para alinear correctamente
                header_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Título centrado
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Logo alineado a la derecha
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')  # Alineación vertical en el centro
                ]))

                # Agregar la tabla al PDF
                elements.append(header_table)
                elements.append(Spacer(1, 12))

            # Crear un estilo para los textos
                info_style = ParagraphStyle(
                    'InfoStyle',
                    fontName='Helvetica',
                    fontSize=10,
                    leading=12
                )

                # Convertir la información en texto con formato "Etiqueta: Valor"
                info_text = [
                    f"Hora de Visita: {verificacion[2]}",
                    f"Zona: {verificacion[3]}",
                    f"Jornada: {verificacion[4]}",
                    f"Operador: {verificacion[6]}",
                    f"Tipo de Ración: {verificacion[8]}",
                    f"Institución: {verificacion[7]}",
                    f"Sede: {verificacion[12]}"
                ]

                # Crear bloques de párrafos en tres columnas (distribuir uniformemente)
                column1 = info_text[0::3]  # Primera columna (cada 3 elementos)
                column2 = info_text[1::3]  # Segunda columna
                column3 = info_text[2::3]  # Tercera columna

                # Construcción del contenido
                elements.append(Spacer(1, 12))
                elements.append(Paragraph("<b>Información</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))

                # Añadir cada columna
                for i in range(len(column1)):  # Iterar hasta la cantidad de elementos en la columna más corta
                    row = []
                    if i < len(column1):
                        row.append(Paragraph(column1[i], info_style))
                    if i < len(column2):
                        row.append(Paragraph(column2[i], info_style))
                    if i < len(column3):
                        row.append(Paragraph(column3[i], info_style))

                    elements.extend(row)  # Agregar fila al PDF

                elements.append(Spacer(1, 12))
                
                # **Tabla de Focalización por Niveles Escolares**
                elements.append(Paragraph("Focalización por Niveles Escolares", styles['Heading2']))
                elements.append(Spacer(1, 6))

                focalizacion_data = [
                    ["Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5", "Total"],
                    [verificacion[13], verificacion[14], verificacion[15], verificacion[16], verificacion[17], verificacion[18]]
                ]

                focalizacion_table = Table(focalizacion_data, colWidths=[80, 80, 80, 80, 80, 80])
                focalizacion_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]))

                elements.append(focalizacion_table)
                elements.append(Spacer(1, 12))
                    
                elements.append(Paragraph("Cumplimeinto de Menú", styles['Heading2']))
                elements.append(Spacer(1, 6))
            # Estilo para las celdas
                styles = getSampleStyleSheet()
                cell_style = ParagraphStyle(name="cell_style", fontSize=8, leading=10, alignment=1)

                # Condición para industrializado
                if es_racion_industrializado:
                    headers = [
                        "Componentes", "Cumplimiento", "Menú Oficial", "Menú Intercambio",
                        "Fecha Venc.", "Lote", "Peso N1", "Peso N2", "Peso N3", "Peso N4", "Peso N5"
                    ]

                    # Reducimos los nombres largos y organizamos la tabla
                    col_widths = [90, 50, 80, 80, 60, 40, 40, 40, 40, 40, 40]

                    data = [headers] + [
                        [
                            Paragraph(detalle[0], cell_style),  # Componentes
                            detalle[1],  # Cumplimiento
                            Paragraph(detalle[2], cell_style),  # Menú Oficial
                            Paragraph(detalle[3], cell_style),  # Menú Intercambio
                            detalle[6] if detalle[6] != "N/A" else "-",  # Fecha de Vencimiento
                            detalle[7] if detalle[7] != "N/A" else "-",  # Lote
                            detalle[8] if detalle[8] != "N/A" else "-",  # Peso N1
                            detalle[9] if detalle[9] != "N/A" else "-",  # Peso N2
                            detalle[10] if detalle[10] != "N/A" else "-",  # Peso N3
                            detalle[11] if detalle[11] != "N/A" else "-",  # Peso N4
                            detalle[12] if detalle[12] != "N/A" else "-",  # Peso N5
                        ]
                        for detalle in detalles_limpios
                    ]
                else:
                    headers = [
                        "Componentes", "Cumplimiento", "Menú Oficial", "Menú Intercambio",
                        "Propiedades Organolépticas", "Observación"
                    ]

                    col_widths = [100, 50, 90, 90, 100, 120]

                    data = [headers] + [
                        [
                            Paragraph(detalle[0], cell_style),  # Componentes
                            str(detalle[1]),  # Cumplimiento
                            Paragraph(detalle[2], cell_style),  # Menú Oficial
                            Paragraph(detalle[3], cell_style),  # Menú Intercambio
                            Paragraph(str(detalle[4]), cell_style) if detalle[4] != "N/A" else "-",  # Prop. Organolépticas
                            Paragraph(str(detalle[5]), cell_style) if detalle[5] != "N/A" else "-"   # Observación
                        ]
                        for detalle in detalles_limpios
                    ]

                # Crear la tabla
                table = Table(data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),  # Texto reducido
                    ('WORDWRAP', (0, 0), (-1, -1), 'CJK')  # Ajuste automático del texto
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
                
                
                # Puntaje de Cumplimiento
                elements.append(Spacer(1, 12))
                elements.append(Paragraph("Puntaje de Cumplimiento", styles['Heading2']))
                elements.append(Spacer(1, 6))

                puntaje_data_table = [
                    ["Puntaje Obtenido", "Clasificación"],
                    [str(puntaje_cumplimiento), str(clasificacion_cumplimiento)]
                ]

                puntaje_table = Table(puntaje_data_table, colWidths=[200, 200])

                # Eliminar los bordes (no usar 'GRID' ni definir bordes en la tabla)
                puntaje_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Sin fondo para las celdas
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                ]))

                elements.append(puntaje_table)
                elements.append(Spacer(1, 12))
                
                
                
                
                if verificacion[11] and verificacion[11] != "N/A":
                    elements.append(Spacer(1, 12))
                    elements.append(Paragraph("Observación General", styles['Heading2']))
                    elements.append(Spacer(1, 2))
                    elements.append(Paragraph(str(verificacion[11]), styles['Normal']))
                
                normal_style = styles['Normal']
                
                elements.append(Spacer(1, 12))
                
                elements.append(Paragraph(
                    'El valor de cumplimiento se utiliza para evaluar la conformidad de los alimentos y puede tomar tres valores: '
                    '<b>"1" (cumple)</b>, que indica que el alimento satisface los estándares establecidos; '
                    '<b>"0" (no cumple)</b>, que señala que el alimento no cumple con dichos estándares; y '
                    '<b>"No aplica"</b>, para los casos donde la evaluación de ciertos criterios no sea relevante para el alimento inspeccionado.<br/><br/>'
                    
                    '<b>Preparados y Almuerzos:</b> El cumplimiento debe evaluarse según las propiedades organolépticas (olor, color y textura) '
                    'en las diferentes preparaciones del ciclo de menú. Si cumplen con los estándares, se marcará como <b>"1" (favorable)</b>; '
                    'de lo contrario, se marcará como <b>"0" (desfavorable)</b>. En caso de marcar "0", el supervisor debe especificar en la casilla de '
                    '<b>"Novedades encontradas en la visita"</b> las inconformidades observadas en el alimento.<br/><br/>'
                    
                    '<b>Industrializados:</b> Si se detecta un incumplimiento en la fecha de vencimiento, este deberá registrarse en la misma casilla de '
                    '<b>"Novedades encontradas en la visita"</b>, describiendo el problema encontrado.',
                    styles['Normal']
                ))



                # Firmas sin bordes
                elements.append(Spacer(1, 24))
                elements.append(Paragraph(f"Nombre del Representante de la Institución: {nombre_representante}", normal_style))
                elements.append(Paragraph(f"Cargo del Representante: {cargo_representante}", normal_style))
                elements.append(Spacer(1, 8))
                elements.append(Paragraph(f"Nombre del Funcionario que realiza la visita: {nombre_funcionario}", normal_style))
                elements.append(Paragraph(f"Nombre del Operador que recibe la visita: {nombre_operador}", normal_style))
                elements.append(Paragraph(f"Cargo del Operador: {cargo_operador}", normal_style))
                elements.append(Paragraph(f"Cargo del Cedula: {cedula_operador}", normal_style))
                elements.append(Spacer(1, 12))
                
                elements.append(Spacer(1, 12))
                
                # **Tabla de Focalización por Niveles Escolares**
                elements.append(Paragraph("Anexo", styles['Heading2']))

                if archivos_verificacion:
                    for nombre_archivo in archivos_verificacion:
                        foto_path = f"static/uploads/verificacion/{nombre_archivo}"  # Ruta correcta

                        # Comprobar si el archivo existe y no es un PDF antes de agregarlo
                        if os.path.exists(foto_path) and not nombre_archivo.lower().endswith(".pdf"):
                            img = Image(foto_path, width=300, height=200)
                            elements.append(img)
                        elif nombre_archivo.lower().endswith(".pdf"):
                            continue  # Omite los PDFs sin mostrar mensaje
                        else:
                            elements.append(Paragraph("No se encontró la imagen.", normal_style))
                else:
                    elements.append(Paragraph("No se adjuntó una foto.", normal_style))

                registrar_auditoria(
                    usuario_id=usuario_sesion,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="DOWNLOAD",
                    modulo="Gestión de Verificación de Menú",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) descargó el archivo Excel con el numero ID {id} de verificación de menú."
                )
                # Generar PDF
                pdf.build(elements)

                buffer.seek(0)

                response = make_response(buffer.getvalue())
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = f'inline; filename=verificacion_menu_V{id}.pdf'
                return response

            # Renderizar HTML si es GET
        return render_template(
            'detalles_verificacion.html',
            verificacion=verificacion,
            detalles=detalles_limpios,
            es_racion_industrializado=es_racion_industrializado,
            puntaje_cumplimiento=puntaje_cumplimiento,
            clasificacion_cumplimiento=clasificacion_cumplimiento,
            niveles=niveles,
            firmas=firmas,
            archivos_verificacion=archivos_verificacion,
            rol=session.get('rol')
        )

    except Exception as e:
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR",
            modulo="Gestión de Verificación de Menú",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) tuvo el error general con el numero ID {id} de verificación de menú. Detalles de Error: {str(e)}"
        )
        rol_usuario = session.get('rol')
        print(f"Error al obtener los detalles de verificación: {e}")
        flash("Ocurrió un error al obtener los detalles de verificación.", "danger")
        if rol_usuario == 'administrador':
            return redirect(url_for('iniciasesion_bp.dashboard_administrador'))
        elif rol_usuario == 'supervisor':
            return redirect(url_for('iniciasesion_bp.dashboard_supervisor'))
        else:
            flash("Rol no reconocido. Redirigiendo al inicio de sesión.", "danger")
            return redirect(url_for('iniciasesion_bp.login'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@verificacion_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_verificacion(id):
    connection = get_db_connection('visitas')
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    
    if connection is None:
        flash('Error al conectar con la base de datos', 'danger')
        return "Error al conectar con la base de datos", 500  # Devuelve un mensaje de error con código HTTP 500


    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # Datos generales de la verificación
        fecha_visita = request.form['fecha_visita']
        hora_visita = request.form['hora_visita']
        zona = request.form['zona']
        jornada = request.form['jornada']
        contrato = request.form['contrato']
        numero_menu_oficial = request.form['numero_menu_oficial']
        numero_menu_intercambio = request.form['numero_menu_intercambio']
        numero_menu_intercambio = int(numero_menu_intercambio) if numero_menu_intercambio else 0
        observacion_general = request.form['observacion_general']
        hallazgo = request.form['hallazgo']
        nivel_1 = request.form['nivel_1']
        nivel_2 = request.form['nivel_2']
        nivel_3 = request.form['nivel_3']
        nivel_4 = request.form['nivel_4']
        nivel_5 = request.form['nivel_5']

        print(f"Intentando actualizar verificacion_menu con ID {id}")
        print(f"Datos recibidos: {fecha_visita}, {hora_visita}, {zona}, {jornada}, {contrato}, {observacion_general}, {hallazgo}, {nivel_1}, {nivel_2}, {nivel_3}, {nivel_4}, {nivel_5}")

        cursor.execute("""
            UPDATE verificacion_menu 
            SET fecha_visita=%s, hora_visita=%s, zona=%s, jornada=%s, contrato=%s, 
                observacion_general=%s, hallazgo=%s, 
                nivel_1=%s, nivel_2=%s, nivel_3=%s, nivel_4=%s, nivel_5=%s,
                numero_menu_oficial=%s, numero_menu_intercambio=%s
            WHERE id=%s
        """, (fecha_visita, hora_visita, zona, jornada, contrato, 
              observacion_general, hallazgo, nivel_1, nivel_2, 
              nivel_3, nivel_4, nivel_5, numero_menu_oficial, numero_menu_intercambio, id))

        if cursor.rowcount > 0:
            print("Actualización exitosa en verificacion_menu")
        else:
            print("No se actualizó ningún registro en verificacion_menu")

        cursor.execute("SELECT id FROM verificacion_menu_detalles WHERE verificacion_menu_id = %s", (id,))
        detalles_existentes = [detalle['id'] for detalle in cursor.fetchall()]


        index = 1
        while f"componentes_{index}" in request.form:
            componentes = request.form[f"componentes_{index}"]
            valor_cumplimiento = request.form[f"valor_cumplimiento_{index}"]
            menu_oficial = request.form[f"menu_oficial_{index}"]
            menu_intercambio = request.form[f"menu_intercambio_{index}"]
            fecha_vencimiento = request.form.get(f"fecha_vencimiento_{index}") or None
            lote = request.form.get(f"lote_{index}", "")
            peso_nivel_1 = request.form.get(f"peso_nivel_1_{index}", 0)
            peso_nivel_2 = request.form.get(f"peso_nivel_2_{index}", 0)
            peso_nivel_3 = request.form.get(f"peso_nivel_3_{index}", 0)
            peso_nivel_4 = request.form.get(f"peso_nivel_4_{index}", 0)
            peso_nivel_5 = request.form.get(f"peso_nivel_5_{index}", 0)
            propiedades_organolepticas = request.form.get(f"propiedades_organolepticas_{index}") or None
            observacion = request.form.get(f"observacion_{index}", "")

            print(f"Procesando detalle {index} para verificacion_menu_id {id}: {componentes}, {valor_cumplimiento}, {menu_oficial}, {menu_intercambio}, {fecha_vencimiento}, {lote}")

            if index <= len(detalles_existentes):
                detalle_id = detalles_existentes[index - 1]
                print(f"Actualizando detalle con ID {detalle_id}")

                cursor.execute("""
                    UPDATE verificacion_menu_detalles
                    SET componentes=%s, valor_cumplimiento=%s, menu_oficial=%s, menu_intercambio=%s, 
                        fecha_vencimiento=%s, lote=%s, peso_nivel_escolar_1=%s, peso_nivel_escolar_2=%s, 
                        peso_nivel_escolar_3=%s, peso_nivel_escolar_4=%s, peso_nivel_escolar_5=%s, 
                        propiedades_organolepticas=%s, observacion=%s
                    WHERE id=%s
                """, (componentes, valor_cumplimiento, menu_oficial, menu_intercambio,
                      fecha_vencimiento, lote, peso_nivel_1, peso_nivel_2, peso_nivel_3, 
                      peso_nivel_4, peso_nivel_5, propiedades_organolepticas, observacion, detalle_id))

                if cursor.rowcount > 0:
                    print(f"Detalle {detalle_id} actualizado correctamente")
                else:
                    print(f"No se actualizó el detalle {detalle_id}")

            else:
                print(f"Insertando nuevo detalle para verificacion_menu_id {id}")

                cursor.execute("""
                    INSERT INTO verificacion_menu_detalles 
                    (verificacion_menu_id, componentes, valor_cumplimiento, menu_oficial, menu_intercambio, 
                     fecha_vencimiento, lote, peso_nivel_escolar_1, peso_nivel_escolar_2, peso_nivel_escolar_3, 
                     peso_nivel_escolar_4, peso_nivel_escolar_5, propiedades_organolepticas, observacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id, componentes, valor_cumplimiento, menu_oficial, menu_intercambio,
                      fecha_vencimiento, lote, peso_nivel_1, peso_nivel_2, peso_nivel_3, 
                      peso_nivel_4, peso_nivel_5, propiedades_organolepticas, observacion))

                if cursor.rowcount > 0:
                    print("Nuevo detalle insertado correctamente")
                else:
                    print("Error al insertar el nuevo detalle")

            index += 1
        
        # Obtener los valores de cumplimiento excluyendo "No Aplica" (2)
        cursor.execute("SELECT valor_cumplimiento FROM verificacion_menu_detalles WHERE verificacion_menu_id = %s", (id,))
        valores_cumplimiento = [
            int(fila["valor_cumplimiento"]) for fila in cursor.fetchall() 
            if fila["valor_cumplimiento"] is not None and int(fila["valor_cumplimiento"]) != 2
        ]


        # Verificar si hay valores para calcular el puntaje
        if valores_cumplimiento:
            total_items = len(valores_cumplimiento)  # Total de ítems sin contar los "No Aplica"
            suma_cumplimiento = sum(valores_cumplimiento)  # Sumar solo los 1 y 0
            puntaje = (suma_cumplimiento / total_items) * 100

            # Determinar clasificación según puntaje
            if puntaje >= 80:
                clasificacion = "Adecuado"
            elif puntaje >= 61:
                clasificacion = "Regular"
            else:
                clasificacion = "Malo"
        else:
            puntaje = 0
            clasificacion = "Malo"  # Si no hay datos válidos, se clasifica como "Malo"

        # Actualizar puntaje y clasificación en la BD si el registro ya existe
        cursor.execute("""
            UPDATE puntaje_cumplimiento 
            SET puntaje = %s, clasificacion = %s 
            WHERE verificacion_menu_id = %s
        """, (puntaje, clasificacion, id))

        print(f"Puntaje actualizado: {puntaje}, Clasificación: {clasificacion}")

        connection.commit()
        
        registrar_auditoria(
            usuario_id=usuario_sesion,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="UPDATE",
            modulo="Gestión de Verificación de Menú",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó los datos con el numero ID {id} de verificación de menú."
        )
        
        print("Cambios confirmados en la base de datos")

        return redirect(url_for('verificacion_bp.detalles_verificacion', id=id))

    # Si es un GET, cargar los datos actuales
    cursor.execute("SELECT * FROM verificacion_menu WHERE id = %s", (id,))
    verificacion = cursor.fetchone()

    cursor.execute("SELECT * FROM verificacion_menu_detalles WHERE verificacion_menu_id = %s", (id,))
    detalles = cursor.fetchall()
    
    cursor.execute("SELECT * FROM firmas_verificacion WHERE id_verificacion = %s", (id,))
    firmas = cursor.fetchone()
    
    cursor.execute("SELECT * FROM puntaje_cumplimiento WHERE verificacion_menu_id = %s", (id,))
    cumplimiento = cursor.fetchone()
    
    # Obtener listas desplegables
    operadores = fetch_operador()
    tiporaciones = fetch_tiporacion()
    instituciones = fetch_instituciones(verificacion['id_operador'])
    print(instituciones)
    
    sedes = fetch_sedes(verificacion['institucion_id']) if verificacion['institucion_id'] else []
    print(sedes)  # Comprueba si la lista está vacía

    
    print(verificacion)  # Verifica qué datos tiene el diccionario

    
    cursor.close()
    connection.close()
    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="UPDATE",
        modulo="Gestión de Verificación de Menú",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó para los datos con el numero ID {id} de verificación de menú."
    )

    return render_template('editar_verificacion.html', verificacion=verificacion, detalles=detalles, operadores=operadores, tiporaciones=tiporaciones, instituciones=instituciones, sedes=sedes, cumplimiento=cumplimiento, firmas=firmas)


def fetch_sedes(id_institucion):
    conn = get_db_connection('visitas')
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_sede, nombre_sede FROM sedes WHERE id_institucion = %s", (id_institucion,))
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
