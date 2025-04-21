from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from iniciasesion import  login_required, session, role_required, registrar_auditoria
import pymysql
from base_datos.database import get_db_connection

# Crear un Blueprint llamado 'bodega_bp'
bodega_bp = Blueprint('bodega', __name__, template_folder='templates/bodega')

  
# Obtener operadores desde la base de datos
def get_operators():
    conn = get_db_connection('visitas', driver="pymysql")
    if conn is None:
        return []
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT id_operador, nombre FROM operadores')
            operators = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error al obtener operadores: {e}")
        operators = []
    finally:
        conn.close()
    return operators

# Obtener preguntas agrupadas por categoría desde la base de datos
def obtener_preguntas_por_categoria():
    preguntas_por_categoria = {}
    conn = get_db_connection('visitas', driver="pymysql")
    if conn is None:
        return preguntas_por_categoria

    try:
        with conn.cursor() as cursor:
            # Obtener las categorías únicas
            cursor.execute("SELECT DISTINCT categoria FROM preguntas_bodega")
            categorias = [row['categoria'] for row in cursor.fetchall()]

            # Consultar preguntas para cada categoría
            for categoria in categorias:
                cursor.execute("SELECT id_pregunta, numero, descripcion FROM preguntas_bodega WHERE categoria = %s", (categoria,))
                preguntas_por_categoria[categoria] = [{'id': row['id_pregunta'], 'numero': row['numero'], 'descripcion': row['descripcion']} for row in cursor.fetchall()]

    except pymysql.MySQLError as e:
        print(f"Error al obtener preguntas: {e}")
    finally:
        conn.close()

    return preguntas_por_categoria

@bodega_bp.route('/get_numero_visita', methods=['GET', 'POST'])
@login_required
def get_numero_visita():
    tipo_visita = request.args.get('tipo_visita') if request.method == 'GET' else request.json.get('tipo_visita')

    if not tipo_visita:
        return jsonify({'error': 'Falta el tipo de visita.'}), 400  

    conn = get_db_connection('visitas', driver="pymysql")
    try:
        with conn.cursor() as cursor:
            cursor.execute("START TRANSACTION")

            # Consulta sin filtro de operador, respetando la numeración globalmente
            cursor.execute("""
                SELECT tipo_visita, numero_visita 
                FROM visitas_bodega 
                ORDER BY id_visita DESC 
                LIMIT 1 
                FOR UPDATE
            """)
            ultima_visita = cursor.fetchone()

            if tipo_visita == "Visita Inicio":
                if ultima_visita and ultima_visita['tipo_visita'] != "Visita Cierre":
                    return jsonify({'error': 'No se puede registrar una nueva Visita de Inicio hasta que haya un Cierre.'}), 400
                numero_visita = 1  

            elif tipo_visita == "Visita Seguimiento":
                if not ultima_visita or ultima_visita['tipo_visita'] == "Visita Cierre":
                    return jsonify({'error': 'Debe registrar primero una Visita de Inicio antes de un Seguimiento.'}), 400
                numero_visita = ultima_visita['numero_visita'] + 1  

            elif tipo_visita == "Visita Cierre":
                if not ultima_visita or ultima_visita['tipo_visita'] != "Visita Seguimiento":
                    return jsonify({'error': 'Solo se puede registrar una Visita de Cierre después de un Seguimiento.'}), 400
                numero_visita = ultima_visita['numero_visita'] + 1  

            else:
                return jsonify({'error': 'Tipo de visita no válido.'}), 400

            conn.commit()

        return jsonify({'numero_visita': numero_visita})

    except Exception as e:
        conn.rollback()
        print("Error en el backend:", e)
        return jsonify({'error': str(e)}), 500

    finally:
        conn.close()

        
from flask import request, redirect, url_for, flash, current_app, session, render_template
import os
import time
import pymysql
from werkzeug.utils import secure_filename

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración de la carpeta de subida
UPLOAD_FOLDER = "static/uploads/bodega/"

# Asegurar que el directorio existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bodega_bp.route('/bodega', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def bodega():
    if request.method == 'POST':
        # Obtener los datos del formulario
        operador = request.form.get('operador')
        tipo_visita = request.form.get('tipo_visita')
        fecha_visita = request.form.get('fecha_visita')
        numero_visita = request.form.getlist('numero_visita_info')  # Tomar solo el último valors
        observacion_general = request.form.get('observacion_general')

        # Validación de campos requeridos
        if not operador or not tipo_visita or not fecha_visita:
            flash('Por favor, complete todos los campos obligatorios.', 'danger')
            return redirect(url_for('bodega.bodega'))

        # Conectar a la base de datos
        conn = get_db_connection('visitas', driver="pymysql")
        if conn is None:
            flash('Error al conectar a la base de datos.', 'danger')
            return redirect(url_for('bodega.bodega'))

        try:
            with conn.cursor() as cursor:
                # Insertar datos generales de la visita
                sql_visita = """
                INSERT INTO visitas_bodega (operador, tipo_visita, fecha_visita, numero_visita, observacion_general)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_visita, (operador, tipo_visita, fecha_visita, numero_visita, observacion_general))
                id_visita = conn.insert_id()

                # Guardar respuestas de preguntas
                respuestas_preguntas = []
                preguntas_por_categoria = obtener_preguntas_por_categoria()
                for categoria, preguntas in preguntas_por_categoria.items():
                    for pregunta in preguntas:
                        respuesta = request.form.get(f'pregunta_{pregunta["id"]}')
                        observacion = request.form.get(f'observacion_{pregunta["id"]}')
                        respuestas_preguntas.append({
                            'id_pregunta': pregunta['id'],
                            'respuesta': respuesta,
                            'observacion': observacion
                        })

                sql_preguntas = """
                INSERT INTO respuestas_bodega (id_visita, id_pregunta, respuesta, observacion)
                VALUES (%s, %s, %s, %s)
                """
                for respuesta in respuestas_preguntas:
                    cursor.execute(sql_preguntas, (id_visita, respuesta['id_pregunta'], respuesta['respuesta'], respuesta['observacion']))

                for categoria, preguntas in preguntas_por_categoria.items():
                    for pregunta in preguntas:
                        archivos = request.files.getlist(f'foto_{pregunta["id"]}')
                        
                        if not archivos or archivos == [None]:  # Verificar si se reciben archivos
                            print(f"❌ No se recibieron archivos para pregunta {pregunta['id']}")
                            continue
                        
                        print(f"📸 Pregunta {pregunta['id']}: Archivos recibidos -> {[archivo.filename for archivo in archivos]}")

                        for archivo in archivos:
                            if archivo and allowed_file(archivo.filename):
                                filename = secure_filename(f"{int(time.time())}_{archivo.filename}")
                                archivo_path = os.path.join(UPLOAD_FOLDER, filename)

                                print(f"📂 Guardando archivo en: {archivo_path}")
                                archivo.save(archivo_path)

                                # Guardar en base de datos
                                try:
                                    sql_foto = "INSERT INTO fotos_bodega (id_visita, id_pregunta, nombre_archivo) VALUES (%s, %s, %s)"
                                    cursor.execute(sql_foto, (id_visita, pregunta['id'], filename))
                                    print(f"✅ Foto guardada en BD: {filename}")
                                except pymysql.MySQLError as e:
                                    print(f"❌ Error al guardar en BD: {e}")

                            else:
                                print(f"⚠️ Archivo inválido o no permitido: {archivo.filename}")

                                
                # Confirmar los cambios
                conn.commit()
                
                usuario_sesion = session.get('usuario_id')
                nombre_sesion = session.get('nombre', 'Desconocido')
                correo_sesion = session.get('correo', 'Sin correo')

                registrar_auditoria(
                    usuario_id=usuario_sesion if usuario_sesion else 0,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="INSERT",
                    modulo="Gestión de Visitas a la Bodega",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los datos en el formulario de Bodega.",
                )

                
                flash(f'Datos guardados exitosamente. Número de visita asignado: {numero_visita}', 'success')

        except pymysql.MySQLError as e:
            conn.rollback()
            usuario_sesion = session.get('usuario_id')
            nombre_sesion = session.get('nombre', 'Desconocido')
            correo_sesion = session.get('correo', 'Sin correo')

            registrar_auditoria(
                usuario_id=usuario_sesion if usuario_sesion else 0,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="ERROR",
                modulo="Gestión de Visitas a la Bodega",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó erroneamente en los datos en el formulario de Bodega.: Dettalles de error: {e}",
            )
            flash(f'Error al guardar los datos: {e}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('bodega.detalles_bodega', id_visita=id_visita))

    # Si el método es GET, renderizar la plantilla normalmente
    operators = get_operators()
    preguntas_por_categoria = obtener_preguntas_por_categoria()
    return render_template('bodega.html', operators=operators, preguntas=preguntas_por_categoria, rol=session.get('rol'), usuario=session.get('nombre'))



@bodega_bp.route('/eliminar_bodega/<int:id_visita>', methods=['DELETE'])
def eliminar_bodega(id_visita):
    conexion = get_db_connection('visitas', driver="pymysql")
    if conexion is None:
        return jsonify({'error': 'Error de conexión con la base de datos'}), 500

    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM visitas_bodega WHERE id_visita = %s", (id_visita,))
        conexion.commit()
        
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="DELETE",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó con el id {id_visita} en el formulario de Bodega.",
        )

        return jsonify({'message': 'Visita eliminada correctamente'}), 200
    except pymysql.MySQLError as e:
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó enorreamente con el id {id_visita} en el formulario de Bodega.: Detalle de error: {e}",
        )
        return jsonify({'error': f'Error al eliminar la visita: {e}'}), 500
    finally:
        conexion.close()




@bodega_bp.route('/lista_bodega', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def lista_bodega():
    # Conectar a la base de datos
    conn = get_db_connection('visitas', driver="pymysql")
    if conn is None:
        flash('Error al conectar a la base de datos.', 'danger')
        return redirect(url_for('bodega.bodega'))

    try:
        with conn.cursor() as cursor:
            # Consultar todos los registros de la tabla visitas_bodega
            sql = "SELECT * FROM visitas_bodega ORDER BY id_visita ASC"  
            cursor.execute(sql)
            datos_bodega = cursor.fetchall()
            
            usuario_sesion = session.get('usuario_id')
            nombre_sesion = session.get('nombre', 'Desconocido')
            correo_sesion = session.get('correo', 'Sin correo')

            registrar_auditoria(
                usuario_id=usuario_sesion if usuario_sesion else 0,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="READ",
                modulo="Gestión de Visitas a la Bodega",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó la lista de Bodega.",
            )
    except pymysql.MySQLError as e:
        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó erroneamente la lista de Bodega: Detalle de error: {e}",
        )
        flash(f'Error al obtener los datos: {e}', 'danger')
        return redirect(url_for('bodega.bodega'))
    finally:
        conn.close()

    # Renderizar la plantilla con los datos
    return render_template('lista_bodega.html', datos_bodega=datos_bodega, rol=session.get('rol'), usuario=session.get('nombre'))


from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from flask import make_response
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm

@bodega_bp.route('/detalles_bodega/<int:id_visita>', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def detalles_bodega(id_visita):
    # Conectar a la base de datos
    conn = get_db_connection('visitas', driver="pymysql")
    if conn is None:
        flash('Error al conectar a la base de datos.', 'danger')
        return redirect(url_for('bodega.lista_bodega'))

    try:
        with conn.cursor() as cursor:
            # Obtener información general de la visita
            sql_visita = """
                SELECT vb.id_visita, o.nombre AS operador, vb.tipo_visita, vb.fecha_visita, vb.numero_visita, vb.observacion_general
                FROM visitas_bodega vb
                JOIN operadores o ON vb.operador = o.id_operador
                WHERE vb.id_visita = %s
            """
            cursor.execute(sql_visita, (id_visita,))
            visita = cursor.fetchone()

            # Verificar que la visita exista
            if not visita:
                flash('Visita no encontrada.', 'warning')
                return redirect(url_for('bodega.lista_bodega'))

            # Obtener preguntas y respuestas asociadas a la visita
            sql_preguntas_respuestas = """
                SELECT pb.numero, pb.descripcion, rb.respuesta, rb.observacion, fb.nombre_archivo
                FROM preguntas_bodega pb
                JOIN respuestas_bodega rb ON pb.id_pregunta = rb.id_pregunta
                LEFT JOIN fotos_bodega fb ON rb.id_pregunta = fb.id_pregunta AND rb.id_visita = fb.id_visita
                WHERE rb.id_visita = %s
            """

            cursor.execute(sql_preguntas_respuestas, (id_visita,))
            preguntas_respuestas = cursor.fetchall()
            
            sql_firmas_bodega = """
                SELECT nombre_recibe, cargo_recibe, nombre_realiza, cargo_realiza
                FROM firmas_bodega
                WHERE id_visita = %s
            """
            cursor.execute(sql_firmas_bodega, (id_visita,))
            firma = cursor.fetchone()  
            
            sql_fotos_bodega = """
                SELECT fb.id_pregunta, fb.nombre_archivo
                FROM fotos_bodega fb
                WHERE fb.id_visita = %s
            """
            cursor.execute(sql_fotos_bodega, (id_visita,))
            fotos_bodega = cursor.fetchall()
            
            usuario_sesion = session.get('usuario_id')
            nombre_sesion = session.get('nombre', 'Desconocido')
            correo_sesion = session.get('correo', 'Sin correo')

            registrar_auditoria(
                usuario_id=usuario_sesion if usuario_sesion else 0,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="READ",
                modulo="Gestión de Visitas a la Bodega",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) ingresó de detalles de Bodega con el ID {id_visita} ",
            ) 
            
            
    except pymysql.MySQLError as e:
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="ERROR READ",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) ingresó erroneamente de detalles de Bodega con el ID {id_visita}. Detalles de error: {e}",
        ) 
        flash(f'Error al obtener los datos: {e}', 'danger')
        return redirect(url_for('bodega.lista_bodega'))
    finally:
        conn.close()

    if request.method == 'POST':
        # Capturar datos del formulario
        nombre_recibe = request.form.get('nombre_recibe', 'No especificado')
        cargo_recibe = request.form.get('cargo_recibe', 'No especificado')
        nombre_realiza = request.form.get('nombre_realiza', 'No especificado')
        cargo_realiza = request.form.get('cargo_realiza', 'No especificado')
        action = request.form.get('action')
        
        if action == "guardar":

            # Depuración: Imprimir los datos capturados
            print(f"Datos capturados del formulario: {nombre_recibe}, {cargo_recibe}, {nombre_realiza}, {cargo_realiza}")

            # Verificar si los campos tienen valores
            if nombre_recibe == '' or cargo_recibe == '' or nombre_realiza == '' or cargo_realiza == '':
                flash('Todos los campos son obligatorios.', 'warning')
                print('Error: Uno o más campos están vacíos')
                return render_template('detalle_bodega.html', visita=visita, preguntas_respuestas=preguntas_respuestas, firma=firma)

            try:
                # Crear una nueva conexión a la base de datos
                conn = get_db_connection('visitas', driver="pymysql")

                if conn.open:
                    with conn.cursor() as cursor:
                        # Verificar si ya existen firmas para la id_visita
                        sql_check_firmas = "SELECT COUNT(*) as total FROM firmas_bodega WHERE id_visita = %s"
                        cursor.execute(sql_check_firmas, (id_visita,))
                        resultado = cursor.fetchone()

                        if resultado and resultado['total'] > 0:
                            print(f"Las firmas para la visita {id_visita} ya existen. No se insertará nuevamente.")
                            flash('Las firmas ya fueron registradas previamente.', 'warning')
                        else:
                            # Insertar las firmas si no existen
                            sql_insert_firmas = """
                                INSERT INTO firmas_bodega (id_visita, nombre_recibe, cargo_recibe, nombre_realiza, cargo_realiza)
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(sql_insert_firmas, (id_visita, nombre_recibe, cargo_recibe, nombre_realiza, cargo_realiza))
                            conn.commit()
                            
                            usuario_sesion = session.get('usuario_id')
                            nombre_sesion = session.get('nombre', 'Desconocido')
                            correo_sesion = session.get('correo', 'Sin correo')

                            registrar_auditoria(
                                usuario_id=usuario_sesion if usuario_sesion else 0,
                                nombre_usuario=nombre_sesion,
                                correo=correo_sesion,
                                accion="INSERT",
                                modulo="Gestión de Visitas a la Bodega",
                                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres en detalles de Bodega con el ID {id_visita} ",
                            ) 
                            print("Transacción confirmada (commit) exitosamente.")
                            flash('Firmas registradas exitosamente.', 'success')
                else:
                    print("Error: La conexión no está abierta.")
                    flash('Error en la conexión a la base de datos.', 'danger')

            except pymysql.MySQLError as e:
                usuario_sesion = session.get('usuario_id')
                nombre_sesion = session.get('nombre', 'Desconocido')
                correo_sesion = session.get('correo', 'Sin correo')

                registrar_auditoria(
                    usuario_id=usuario_sesion if usuario_sesion else 0,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="INSERT",
                    modulo="Gestión de Visitas a la Bodega",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó enorreamente los nombres en detalles de Bodega con el ID {id_visita}. Detalle de Error: {str(e)} ",
                ) 
                print(f"Error al ejecutar la consulta: {e.args}")
                flash(f'Error al insertar las firmas: {e}', 'danger')

            return redirect(url_for('bodega.detalles_bodega', id_visita=id_visita))

        elif action == "pdf":
            
            if nombre_recibe == '' or cargo_recibe == '' or nombre_realiza == '' or cargo_realiza == '':
                flash('Todos los campos son obligatorios.', 'warning')
                print('Error: Uno o más campos están vacíos')
                return render_template('detalle_bodega.html', visita=visita, preguntas_respuestas=preguntas_respuestas, firma=firma)

            try:
                # Crear una nueva conexión a la base de datos
                conn = get_db_connection('visitas', driver="pymysql")

                if conn.open:
                    with conn.cursor() as cursor:
                        # Verificar si ya existen firmas para la id_visita
                        sql_check_firmas = "SELECT COUNT(*) as total FROM firmas_bodega WHERE id_visita = %s"
                        cursor.execute(sql_check_firmas, (id_visita,))
                        resultado = cursor.fetchone()

                        if resultado and resultado['total'] > 0:
                            usuario_sesion = session.get('usuario_id')
                            nombre_sesion = session.get('nombre', 'Desconocido')
                            correo_sesion = session.get('correo', 'Sin correo')

                            registrar_auditoria(
                                usuario_id=usuario_sesion if usuario_sesion else 0,
                                nombre_usuario=nombre_sesion,
                                correo=correo_sesion,
                                accion="INSERT EXISTENTE",
                                modulo="Gestión de Visitas a la Bodega",
                                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres existentes en detalles de Bodega con el ID {id_visita}.",
                            ) 
                            print(f"Las firmas para la visita {id_visita} ya existen. No se insertará nuevamente.")
                            flash('Las firmas ya fueron registradas previamente.', 'warning')
                        else:
                            # Insertar las firmas si no existen
                            sql_insert_firmas = """
                                INSERT INTO firmas_bodega (id_visita, nombre_recibe, cargo_recibe, nombre_realiza, cargo_realiza)
                                VALUES (%s, %s, %s, %s, %s)
                            """
                            cursor.execute(sql_insert_firmas, (id_visita, nombre_recibe, cargo_recibe, nombre_realiza, cargo_realiza))
                            conn.commit()
                            
                            usuario_sesion = session.get('usuario_id')
                            nombre_sesion = session.get('nombre', 'Desconocido')
                            correo_sesion = session.get('correo', 'Sin correo')

                            registrar_auditoria(
                                usuario_id=usuario_sesion if usuario_sesion else 0,
                                nombre_usuario=nombre_sesion,
                                correo=correo_sesion,
                                accion="INSERT AND ARCHIVO PDF",
                                modulo="Gestión de Visitas a la Bodega",
                                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres y descargó el archivo pdf en detalles de Bodega con el ID {id_visita}.",
                            ) 
                            print("Transacción confirmada (commit) exitosamente.")
                            flash('Firmas registradas exitosamente.', 'success')
                else:
                    print("Error: La conexión no está abierta.")
                    flash('Error en la conexión a la base de datos.', 'danger')

            except pymysql.MySQLError as e:
                usuario_sesion = session.get('usuario_id')
                nombre_sesion = session.get('nombre', 'Desconocido')
                correo_sesion = session.get('correo', 'Sin correo')

                registrar_auditoria(
                    usuario_id=usuario_sesion if usuario_sesion else 0,
                    nombre_usuario=nombre_sesion,
                    correo=correo_sesion,
                    accion="INSERT AND ARCHIVO PDF",
                    modulo="Gestión de Visitas a la Bodega",
                    detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) insertó los nombres y descargó  enorreanemente el archivo pdf en detalles de Bodega con el ID {id_visita}. Detalles de error: {e}",
                ) 
                print(f"Error al ejecutar la consulta: {e.args}")
                flash(f'Error al insertar las firmas: {e}', 'danger')
                
                
            # Generar PDF
            buffer = BytesIO()
            pdf = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Cargar la imagen de la Alcaldía de Cali
            logo_path = "static/images/cali.png"
            logo = Image(logo_path, width=40 * mm, height=30 * mm)

            # Generar el código de barras
            barcode_data = f"B{visita['id_visita']}_V_{visita['numero_visita']}_{visita['fecha_visita'].strftime('%Y%m%d')}"
            barcode = code128.Code128(barcode_data, barWidth=0.5 * mm, barHeight=12 * mm)

            # Texto para mostrar debajo del código de barras
            barcode_text = f"B{visita['id_visita']}_V_{visita['numero_visita']}_{visita['fecha_visita'].strftime('%Y-%m-%d')}"

            # Crear un estilo para el texto centrado
            styles = getSampleStyleSheet()
            barcode_text_style = styles['Normal']
            barcode_text_style.alignment = 1  # 1 = CENTRADO

            # Crear la tabla con el código de barras y el texto debajo
            barcode_table = Table(
                [[barcode], [Paragraph(barcode_text, barcode_text_style)]],
                colWidths=[80 * mm]  # Ajusta el ancho para centrar mejor
            )

            # Aplicar estilo a la tabla para centrar los elementos
            barcode_table.setStyle(
                TableStyle([
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Centrar elementos en la celda
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),  # Espaciado entre código y texto
                ])
            )

            # Crear tabla con la imagen a la izquierda y el código de barras a la derecha
            layout_table = Table(
                [[logo, barcode_table]],
                colWidths=[100 * mm, 100 * mm],  # Ancho de columnas para imagen y código de barras
            )

            # Aplicar estilo a la tabla para alinear a la esquina inferior derecha
            layout_table.setStyle(
                TableStyle([
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),  # Alinear imagen a la izquierda
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),  # Alinear código de barras a la derecha
                    ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),  # Alinear verticalmente abajo
                ])
            )

            # Agregar la tabla alineada a los elementos
            elements.append(Spacer(1, 5))  # Espacio para empujar todo hacia abajo
            elements.append(layout_table)  # Agregar la tabla con imagen y código de barras


            styles = getSampleStyleSheet()
            style_normal = styles['Normal']
            style_heading = styles['Heading2']

            # Encabezado
            elements.append(Paragraph("Visita a la Bodega", styles['Title']))
            elements.append(Spacer(1, 12))

            # Información General
            elements.append(Paragraph("Información General", style_heading))
            info_data = [
                ["ID Visita", f"B{visita['id_visita']}"],
                ["Operador", visita['operador']],
                ["Tipo de Visita", visita['tipo_visita']],
                ["Fecha de Visita", visita['fecha_visita']],
                ["Número de Visita", visita['numero_visita']],
            ]
            info_table = Table(info_data)
            info_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 12))
                

            # Preguntas y Respuestas
            elements.append(Paragraph("Preguntas y Respuestas", style_heading))

            # Encabezados de la tabla
            respuestas_data = [
                [
                    Paragraph("Número", style_normal),
                    Paragraph("Pregunta", style_normal),
                    Paragraph("Respuesta", style_normal),
                    Paragraph("Observación", style_normal),
                ]
            ]

            # Filas de datos
            for pregunta in preguntas_respuestas:
                respuestas_data.append([
                    Paragraph(str(pregunta['numero']), style_normal),  # Asegurar que 'numero' sea texto
                    Paragraph(pregunta['descripcion'], style_normal),
                    Paragraph(pregunta['respuesta'], style_normal),
                    Paragraph(pregunta['observacion'], style_normal),
                ])

            # Crear la tabla con anchos ajustados
            respuestas_table = Table(respuestas_data, colWidths=[60, 240, 60, 150])  # Ajusta los anchos según el contenido
            respuestas_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de las celdas
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Fondo gris para encabezados
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente estándar
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alineación vertical en la parte superior
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación horizontal a la izquierda
            ]))

            # Agregar la tabla al PDF
            elements.append(respuestas_table)
            elements.append(Spacer(1, 12))
                        
                                    
            # Lista de datos para las fotos
            fotos_data = []

            # Itera sobre los resultados de la consulta de fotos
            for id_pregunta, nombre_archivo in fotos_bodega:
                ext = os.path.splitext(nombre_archivo)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:  # Solo imágenes
                    ruta_imagen = os.path.join("static/uploads/bodega", nombre_archivo)  # Ruta completa de la imagen
                    if os.path.exists(ruta_imagen):  # Verifica que la imagen exista
                        # Agrega la imagen junto con la información de la pregunta
                        fotos_data.append([
                            f"Imagen asociada a la pregunta {id_pregunta}",
                            ruta_imagen
                        ])
                    else:
                        print(f"Advertencia: No se encontró la imagen en la ruta {ruta_imagen}")

            # Ahora agregamos las fotos al documento
            for foto in fotos_data:
                # Asegura que la ruta de la imagen y el texto se agreguen al PDF
                elements.append(Paragraph(foto[0], style_normal))  # Título de la imagen
                try:
                    elements.append(Image(foto[1], width=200, height=150))  # Imagen
                except Exception as e:
                    print(f"Error al agregar la imagen: {e}")
                elements.append(Spacer(1, 12))  # Espaciado entre las imágenes

            # Observación general
            elements.append(Paragraph(f"Observación: {visita['observacion_general']}", style_normal))
            elements.append(Spacer(1, 12))
            
            # Firmas
            elements.append(Paragraph("Firmas", style_heading))
            firmas_data = [
                ["Nombre (Recibe):", nombre_recibe, "Nombre (Realiza):", nombre_realiza],
                ["Cargo (Recibe):", cargo_recibe, "Cargo (Realiza):", cargo_realiza],
            ]

            # Crear la tabla de firmas con 4 columnas (2 por cada persona)
            firmas_table = Table(firmas_data, colWidths=[140, 140, 140, 140])

            # Estilo de la tabla
            firmas_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0, colors.white),  # Eliminar bordes de la tabla
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinear todo a la izquierda
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente Helvetica
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
            ]))

            # Añadir la tabla al documento
            elements.append(firmas_table)
            
            

            # Generar PDF
            pdf.build(elements)
            buffer.seek(0)

            response = make_response(buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'inline; filename=visita_bodega_B{id_visita}.pdf'
            return response

    # Renderizar la plantilla para GET
    return render_template(
        'detalles_bodega.html',
        visita=visita,
        preguntas_respuestas=preguntas_respuestas,
        firma=firma,
        fotos_bodega=fotos_bodega,
        rol=session.get('rol'),
        usuario=session.get('nombre')
    )


@bodega_bp.route('/editar_bodega/<int:id_visita>', methods=['GET', 'POST'])
def editar_bodega(id_visita):
    db = get_db_connection('visitas', driver="pymysql")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        tipo_visita = request.form['tipo_visita']
        fecha_visita = request.form['fecha_visita']
        numero_visita = request.form['numero_visita']
        observacion_general = request.form['observacion_general']
        
        # Actualizar la visita en la base de datos
        sql_update_visita = """
            UPDATE visitas_bodega 
            SET tipo_visita = %s, fecha_visita = %s, numero_visita = %s, observacion_general = %s
            WHERE id_visita = %s
        """
        cursor.execute(sql_update_visita, (tipo_visita, fecha_visita, numero_visita, observacion_general, id_visita))
        db.commit()

        # Actualizar preguntas y respuestas
        preguntas = request.form.getlist('pregunta_id')
        respuestas = request.form.getlist('respuesta')
        observaciones = request.form.getlist('observacion')
        
        for i in range(len(preguntas)):
            sql_update_respuesta = """
                UPDATE respuestas_bodega 
                SET respuesta = %s, observacion = %s
                WHERE id_visita = %s AND id_pregunta = %s
            """
            cursor.execute(sql_update_respuesta, (respuestas[i], observaciones[i], id_visita, preguntas[i]))
        db.commit()
        
        for i in range(len(preguntas)):
            id_pregunta = preguntas[i]
            field_name = f"archivo_{id_pregunta}"
            
            if field_name in request.files:
                file = request.files[field_name]
                if file and allowed_file(file.filename):
                    # Procesar nombre de archivo y guardar
                    filename = secure_filename(file.filename)
                    nombre_archivo = f"B_{id_visita}_pregunta_{id_pregunta}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, nombre_archivo)
                    file.save(filepath)

                    # Verificar si ya existe registro en fotos_bodega
                    sql_check = "SELECT COUNT(*) FROM fotos_bodega WHERE id_visita = %s AND id_pregunta = %s"
                    cursor.execute(sql_check, (id_visita, id_pregunta))
                    row = cursor.fetchone()
                    exists = row[0] if row and 0 in row else 0


                    if exists:
                        # Actualizar archivo existente
                        sql_update = """
                            UPDATE fotos_bodega 
                            SET nombre_archivo = %s 
                            WHERE id_visita = %s AND id_pregunta = %s
                        """
                        cursor.execute(sql_update, (nombre_archivo, id_visita, id_pregunta))
                    else:
                        # Insertar nuevo registro
                        sql_insert = """
                            INSERT INTO fotos_bodega (id_visita, id_pregunta, nombre_archivo) 
                            VALUES (%s, %s, %s)
                        """
                        cursor.execute(sql_insert, (id_visita, id_pregunta, nombre_archivo))

        db.commit()
        
        
        
        firmas = request.form.getlist('firma_id')
        nombres_recibe = request.form.getlist('nombre_recibe')
        cargos_recibe = request.form.getlist('cargo_recibe')
        nombres_realiza = request.form.getlist('nombre_realiza')
        cargos_realiza = request.form.getlist('cargo_realiza')
        
        for i in range(len(firmas)):
            sql_update = """
                UPDATE firmas_bodega
                SET nombre_recibe = %s, cargo_recibe = %s, nombre_realiza = %s, cargo_realiza = %s
                WHERE id_firma_bodega = %s AND id_visita = %s
            """
            cursor.execute(sql_update, (nombres_recibe[i], cargos_recibe[i], nombres_realiza[i], cargos_realiza[i], firmas[i], id_visita))
        db.commit()
        
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="UPDATE",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó los datos en los detalles de Bodega con el ID {id_visita}.",
        ) 

        flash('Visita actualizada correctamente.', 'success')
        return redirect(url_for('bodega.detalles_bodega', id_visita=id_visita))
    
    # Obtener datos de la visita
    sql_visita = """
        SELECT vb.id_visita, o.nombre AS operador, vb.tipo_visita, vb.fecha_visita, vb.numero_visita, vb.observacion_general
        FROM visitas_bodega vb
        JOIN operadores o ON vb.operador = o.id_operador
        WHERE vb.id_visita = %s
    """
    cursor.execute(sql_visita, (id_visita,))
    visita = cursor.fetchone()

    if not visita:
        flash('Visita no encontrada.', 'warning')
        return redirect(url_for('bodega.lista_bodega'))

    # Obtener preguntas y respuestas
    sql_preguntas_respuestas = """
        SELECT pb.id_pregunta, pb.descripcion, rb.respuesta, rb.observacion, pb.numero, pb.categoria
        FROM preguntas_bodega pb
        JOIN respuestas_bodega rb ON pb.id_pregunta = rb.id_pregunta
        WHERE rb.id_visita = %s
    """
    cursor.execute(sql_preguntas_respuestas, (id_visita,))
    preguntas_respuestas = cursor.fetchall()
    
    sql_firmas = """
        SELECT * FROM firmas_bodega
        WHERE id_visita = %s
    """
    cursor.execute(sql_firmas, (id_visita,))
    firmas = cursor.fetchone()
    
    usuario_sesion = session.get('usuario_id')
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

    registrar_auditoria(
        usuario_id=usuario_sesion if usuario_sesion else 0,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="SELECT",
        modulo="Gestión de Visitas a la Bodega",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó los datos en los detalles de Bodega con el ID {id_visita}.",
    ) 

    return render_template('editar_bodega.html', visita=visita, preguntas_respuestas=preguntas_respuestas, firmas=firmas)


import os
import zipfile
import io
import pandas as pd
from flask import Response, send_file, request, flash, redirect, url_for



@bodega_bp.route('/bodega/exportar', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def exportar_bodega():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    conn = get_db_connection('visitas', driver="pymysql")
    if not conn:
        flash('Error al conectar con la base de datos.', 'danger')
        return redirect(url_for('bodega.lista_bodega'))

    try:
        # Consulta SQL optimizada con DISTINCT y filtros de fecha
        query = """
        SELECT DISTINCT v.id_visita, v.operador, v.tipo_visita, v.fecha_visita, v.numero_visita, v.observacion_general,
                        r.id_pregunta, r.respuesta, r.observacion, f.nombre_archivo
        FROM visitas_bodega v
        LEFT JOIN respuestas_bodega r ON v.id_visita = r.id_visita
        LEFT JOIN fotos_bodega f ON v.id_visita = f.id_visita AND r.id_pregunta = f.id_pregunta
        WHERE 1=1
        """

        params = []
        if fecha_inicio:
            query += " AND v.fecha_visita >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND v.fecha_visita <= %s"
            params.append(fecha_fin)

        query += " ORDER BY v.id_visita DESC"

        # Ejecutar consulta
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            result = cursor.fetchall()

        # Convertir resultado en DataFrame
        df = pd.DataFrame(result)

        # Crear un archivo Excel en memoria
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Bodega')
        excel_buffer.seek(0)

        # Crear un archivo ZIP que contenga el Excel y las imágenes
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Agregar el archivo Excel al ZIP
            zipf.writestr("bodega_export.xlsx", excel_buffer.getvalue())

            # Agregar imágenes desde la carpeta correcta
            base_dir = 'static/uploads/bodega'  # Ruta de las imágenes
            if os.path.exists(base_dir):
                for root, _, files in os.walk(base_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, 'static/uploads'))

        zip_buffer.seek(0)
        
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo=correo_sesion,
            accion="DOWNLOAD",
            modulo="Gestión de Visitas a la Bodega",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) descargó el archivo Excel desde fecha inicio {fecha_inicio} a {fecha_fin}.",
        ) 

        # Enviar el archivo ZIP como descarga
        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name="bodega_archivos.zip"
        )

    except Exception as e:
        flash(f'Error al exportar: {e}', 'danger')
        return redirect(url_for('bodega.lista_bodega'))
