from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file, flash
from iniciasesion import login_required, session, role_required
import pandas as pd
from io import BytesIO
import pymysql.cursors
import functools
from datetime import timedelta

# Crear un Blueprint llamado 'tecnica'
tecnica_bp = Blueprint('tecnica', __name__, template_folder='templates/tecnica')

# Cache para almacenar resultados estáticos
cache_operadores = None
cache_instituciones = None
cache_tipo_racion = None

# Función para obtener una conexión a la base de datos
def obtener_conexion():
    try:
        return pymysql.connect(
            host="127.0.0.1",
            user="Pae",
            password="Pae_educacion",
            db="visitas",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
    
def obtener_sedes_por_institucion(institucion_id):
    with obtener_conexion() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id_sede, nombre_sede FROM sedes WHERE id_institucion = %s", (institucion_id,))
            sedes = [{'id': row['id_sede'], 'nombre': row['nombre_sede']} for row in cursor.fetchall()]
    return sedes

@tecnica_bp.route('/get_sede/<int:institucion_id>', methods=['GET'])
def get_sede(institucion_id):
    try:
        sedes = obtener_sedes_por_institucion(institucion_id)
        return jsonify({'sedes': sedes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tecnica_bp.route('/get_sede_details/<int:sede_id>', methods=['GET'])
def get_sede_details(sede_id):
    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT codigo, direccion, comuna, zona FROM sedes WHERE id_sede = %s", (sede_id,))
                sede_details = cursor.fetchone()
                
                if not sede_details:
                    return jsonify({'error': 'Sede no encontrada'}), 404
                
                return jsonify({
                    'codigo': sede_details['codigo'],
                    'direccion': sede_details['direccion'],
                    'comuna': sede_details['comuna'],
                    'zona': sede_details['zona']
                })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def obtener_operador():
    global cache_operadores
    if cache_operadores is None:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_operador, nombre FROM operadores")
                cache_operadores = cursor.fetchall()  # ✅ Devuelve una lista de diccionarios
    return cache_operadores

# Función para obtener instituciones desde la base de datos
def obtener_institucion():
    global cache_instituciones
    if cache_instituciones is None:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT id_institucion, sede_educativa FROM instituciones")
                cache_instituciones = [{'id': row['id_institucion'], 'nombre': row['sede_educativa']} for row in cursor.fetchall()]
    return cache_instituciones

# Función para obtener tipo de ración desde la base de datos
def obtener_tipo_racion():
    global cache_tipo_racion
    if cache_tipo_racion is None:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT DISTINCT tipo_racion FROM preguntas_tecnica")
                cache_tipo_racion = [row['tipo_racion'] for row in cursor.fetchall()]
    return cache_tipo_racion

# Optimización de la consulta de preguntas por tipo de ración
def obtener_preguntas_por_tipo_racion(tipo_racion):
    tipo_racion = tipo_racion.strip()  # Eliminar espacios en blanco
    preguntas_por_categoria = {}

    try:
        with obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                query = """
                    SELECT DISTINCT id_tecnica, numero, preguntas, categorias 
                    FROM preguntas_tecnica 
                    WHERE tipo_racion LIKE %s
                    ORDER BY categorias, id_tecnica, numero
                """
                cursor.execute(query, (f'%{tipo_racion}%',))
                preguntas = cursor.fetchall()
                
                # Agrupar las preguntas por categoría
                for pregunta in preguntas:
                    categoria = pregunta['categorias']
                    if categoria not in preguntas_por_categoria:
                        preguntas_por_categoria[categoria] = []
                    preguntas_por_categoria[categoria].append(pregunta)
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")
    return preguntas_por_categoria


@tecnica_bp.route('/obtener_preguntas', methods=['GET'])
def obtener_preguntas():
    tipo_racion = request.args.get('tipo_racion')
       
    if tipo_racion:
        tipo_racion = tipo_racion.strip()  # Elimina espacios en blanco
        preguntas_por_categoria = obtener_preguntas_por_tipo_racion(tipo_racion)
        return jsonify(preguntas_por_categoria)
    
    return jsonify({"error": "El parámetro 'tipo_racion' es obligatorio"}), 400

@tecnica_bp.route('/tecnica', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def mostrar_tecnica():
    operadores = obtener_operador()
    instituciones = obtener_institucion()
    tipo_racion_tecnicas = obtener_tipo_racion()

    return render_template('tecnica.html', 
                           operadores=operadores, 
                           instituciones=instituciones, 
                           tipo_racion_tecnicas=tipo_racion_tecnicas, 
                           rol=session.get('rol'), 
                           usuario=session.get('nombre'))
    
    
import os
import time
import traceback
from flask import current_app, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@tecnica_bp.route('/guardar_tecnica', methods=['POST'])
def guardar_tecnica():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    try:
        # Recibe los datos del formulario
        
        data = request.form.to_dict()
        print("Datos recibidos:", data)
        
        fecha_visita = request.form.get('fecha_visita')
        hora_visita = request.form.get('hora_visita')
        operador = request.form.get('operador')
        institucion_id = request.form.get('institucion')
        sede_id = request.form.get('sede')
        focalizacion = request.form.get('focalizacion')
        tipo_racion_tecnica = request.form.get('tipo_racion_tecnica')
        codigo_sede = request.form.get('codigo_sede')
        direccion = request.form.get('direccion')
        zona = request.form.get('zona')
        observacion_general = request.form.get('observacion_general')


        # Imprime todos los datos del formulario para depuración
        print("Datos del formulario recibidos en el servidor:")
        for key, value in request.form.items():
            print(f"{key}: {value}")

        # Insertar la visita técnica en la base de datos
        sql_visita = """
            INSERT INTO visita_tecnica 
            (fecha_visita, hora_visita, operador, institucion_id, sede_id, focalizacion, tipo_racion_tecnica, codigo_sede, direccion, zona, observacion_general)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_visita, (fecha_visita, hora_visita, operador, institucion_id, sede_id, focalizacion, tipo_racion_tecnica, codigo_sede, direccion, zona, observacion_general))
        
        # Obtener el ID de la visita técnica insertada
        visita_tecnica_id = cursor.lastrowid
        print(f"ID de la visita técnica insertada: {visita_tecnica_id}")

        # Guardar las respuestas de las preguntas
        respuestas_data = []

        for key, value in request.form.items():
            if key.startswith('pregunta_'):
                pregunta_id = key.split('_')[1]  # Extrae el ID de la pregunta
                respuesta = value
                observacion = request.form.get(f'observacion_{pregunta_id}', '')

                try:
                    sql_respuesta = """
                        INSERT INTO respuestas_tecnica (visita_tecnica_id, pregunta_id, respuesta, observaciones)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql_respuesta, (visita_tecnica_id, pregunta_id, respuesta, observacion))
                    respuestas_data.append((pregunta_id, respuesta, observacion))
                    print(f"✅ Respuesta guardada: Pregunta {pregunta_id}.")
                except Exception as e:
                    print(f"❌ Error al guardar la respuesta de la pregunta {pregunta_id}: {e}")
                    traceback.print_exc()  # Muestra detalles del error

        # Ruta donde se guardarán los archivos generales
        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static/uploads/tecnica')
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Asegurar que la carpeta existe

        # Obtener archivos adjuntos generales
        archivos = request.files.getlist('archivo')  # Flask maneja `multiple` sin necesidad de `[]` en el nombre

        for archivo in archivos:
            if archivo and allowed_file(archivo.filename):
                filename = f"{int(time.time())}_{secure_filename(archivo.filename)}"
                archivo_path = os.path.join(UPLOAD_FOLDER, filename)

                try:
                    archivo.save(archivo_path)

                    # Guardar en la base de datos
                    sql_archivo = """
                        INSERT INTO archivos_visita_tecnica (visita_tecnica_id, nombre_archivo, ruta_archivo)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(sql_archivo, (visita_tecnica_id, filename, f"static/uploads/tecnica/{filename}"))

                    print(f"✅ Archivo guardado: {filename}")
                except Exception as e:
                    print(f"⚠️ Error guardando el archivo {filename}: {e}")

  
        print(f"Respuestas guardadas correctamente: {len(respuestas_data)}")
        # Confirmar los cambios en la base de datos
        conn.commit()
        print("Datos guardados exitosamente.")
        
        
        # rol_usuario = session.get('rol')
        
         # Verificar que el ID guardado sigue siendo el correcto
        print(f"ID tecnica antes de redirigir: {visita_tecnica_id}")  # ✅ Depuración final
        
        return redirect(url_for('tecnica.detalle_tecnica', id_visita_tecnica=visita_tecnica_id))
    
    

    except Exception as e:
        # Redirigir de nuevo al formulario o a otra página
        conn.rollback()  # ✅ Ahora sí se ejecutará en caso de error
        print("Error durante la ejecución:", str(e))  # ✅ Imprime error exacto en consola
        flash(f"Error al guardar: {str(e)}", "danger")

        # Redirigir de nuevo al formulario o a otra página
        return redirect(url_for('tecnica_bp.tecnica')) 
    
    finally:
        # Cerrar la conexión y el cursor
        cursor.close()
        conn.close()
        
        
@tecnica_bp.route('/eliminar_tecnica/<int:id_visita_tecnica>', methods=['DELETE'])
def eliminar_tecnica(id_visita_tecnica):
    conexion = obtener_conexion()  # Llamar a la función para obtener la conexión
    if conexion is None:
        return jsonify({'success': False, 'message': 'Error de conexión con la base de datos'}), 500

    try:
        with conexion.cursor() as cursor:  # Crear cursor dentro de un bloque 'with'
            cursor.execute("DELETE FROM visita_tecnica WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
        conexion.commit()
        return jsonify({'success': True, 'message': 'Visita técnica eliminada correctamente'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'success': False, 'message': f'Error al eliminar la visita técnica: {e}'}), 500
    finally:
        conexion.close()  # Cerrar la conexión después de la consulta

        
        
@tecnica_bp.route('/toma_peso', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def toma_peso():
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    vt.id_visita_tecnica, 
                    vt.tipo_racion_tecnica, 
                    sed.nombre_sede
                FROM visita_tecnica vt
                LEFT JOIN sedes sed ON vt.sede_id = sed.id_sede
            """)

            visitas = cursor.fetchall()

            
            if not visitas:
                flash("No hay visitas disponibles para seleccionar.", "warning")
            
            muestras = list(range(1, 11))  # Muestras del 1 al 10
            componentes = ["Bebida Láctea", "Alimento Proteico", "Cereal Acompañante", "Fruta"]
            return render_template('toma_peso.html', muestras=muestras, componentes=componentes, visitas=visitas)

        elif request.method == 'POST':
            visita_id = request.form.get('visita_id')
            desperdicio = request.form.get('desperdicio')
            menu_del_dia = request.form.get('menu_del_dia')
            nivel1 = request.form.get('nivel1')
            nivel2 = request.form.get('nivel2')
            nivel3 = request.form.get('nivel3')
            nivel4 = request.form.get('nivel4')
            nivel5 = request.form.get('nivel5')
            total = request.form.get('total')
            observacion = request.form.get('observacion')
            
            # Imprimir los valores para depuración
            print(f"Visita ID: {visita_id}")
            print(f"Desperdicio: {desperdicio}")
            print(f"Menú del Día: {menu_del_dia}")
            print(f"Nivel 1: {nivel1}")
            print(f"Nivel 2: {nivel2}")
            print(f"Nivel 3: {nivel3}")
            print(f"Nivel 4: {nivel4}")
            print(f"Nivel 5: {nivel5}")
            print(f"Total: {total}")
            print(f"Observación: {observacion}")

            if not all([visita_id, desperdicio, menu_del_dia, nivel1, nivel2, nivel3, nivel4, nivel5, total]):
                flash("Por favor completa todos los campos.", "warning")
                return redirect(url_for('tecnica.toma_peso'))

            total_calculado = sum(map(int, [nivel1, nivel2, nivel3, nivel4, nivel5]))
            if int(total) != total_calculado:
                flash("El total enviado no coincide con el cálculo.", "warning")
                return redirect(url_for('tecnica.toma_peso'))

            cursor.execute("""
                INSERT INTO toma_peso (
                    id_visita_tecnica, desperdicio, menu_del_dia, nivel1, nivel2, nivel3, nivel4, nivel5, total, observacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (visita_id, desperdicio, menu_del_dia, nivel1, nivel2, nivel3, nivel4, nivel5, total, observacion))
            

            # Datos de componentes alimentarios
            muestras = list(range(1, 11))
            componentes = ["Bebida Láctea", "Alimento Proteico", "Cereal Acompañante", "Fruta"]

            for muestra in muestras:
                for componente in componentes:
                    visita_id = request.form.get('visita_id')
                    nivel1 = request.form.get(f"peso_nivel1_{muestra}_{componente}", 0)
                    nivel2 = request.form.get(f"peso_nivel2_{muestra}_{componente}", 0)
                    nivel3 = request.form.get(f"peso_nivel3_{muestra}_{componente}", 0)
                    nivel4 = request.form.get(f"peso_nivel4_{muestra}_{componente}", 0)
                    nivel5 = request.form.get(f"peso_nivel5_{muestra}_{componente}", 0)

                    # Insertar cada componente alimentario
                    cursor.execute("""
                        INSERT INTO componente_alimentario_1 (
                            id_visita_tecnica, muestra, componente, nivel_1, nivel_2, nivel_3, nivel_4, nivel_5
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (visita_id, muestra, componente, nivel1, nivel2, nivel3, nivel4, nivel5))
                    
            for nivel in ["Nivel Escolar 1", "Nivel Escolar 2", "Nivel Escolar 3", "Nivel Escolar 4", "Nivel Escolar 5"]:
                visita_id = request.form.get('visita_id')
                # Recoger los datos de cada nivel escolar
                peso_patron_bebida = request.form.get(f'peso_patron_bebida_{nivel}')
                peso_patron_proteico = request.form.get(f'peso_patron_proteico_{nivel}')
                peso_patron_cereal = request.form.get(f'peso_patron_cereal_{nivel}')
                peso_patron_fruta = request.form.get(f'peso_patron_fruta_{nivel}')
                peso_obtenido_bebida = request.form.get(f'peso_obtenido_bebida_{nivel}')
                peso_obtenido_proteico = request.form.get(f'peso_obtenido_proteico_{nivel}')
                peso_obtenido_cereal = request.form.get(f'peso_obtenido_cereal_{nivel}')
                peso_obtenido_fruta = request.form.get(f'peso_obtenido_fruta_{nivel}')
                concepto_bebida = request.form.get(f'concepto_bebida_{nivel}')
                concepto_proteico = request.form.get(f'concepto_proteico_{nivel}')
                concepto_cereal = request.form.get(f'concepto_cereal_{nivel}')
                concepto_fruta = request.form.get(f'concepto_fruta_{nivel}')

                # Insertar los datos en la base de datos
                cursor.execute("""
                    INSERT INTO componente_alimentario_promedio (
                        id_visita_tecnica, nivel_escolar, peso_patron_bebida, peso_patron_proteico, peso_patron_cereal,
                        peso_patron_fruta, peso_obtenido_bebida, peso_obtenido_proteico, peso_obtenido_cereal,
                        peso_obtenido_fruta, concepto_bebida, concepto_proteico, concepto_cereal, concepto_fruta
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (visita_id, nivel, peso_patron_bebida, peso_patron_proteico, peso_patron_cereal, peso_patron_fruta,
                    peso_obtenido_bebida, peso_obtenido_proteico, peso_obtenido_cereal, peso_obtenido_fruta,
                    concepto_bebida, concepto_proteico, concepto_cereal, concepto_fruta))
                
            temp_bebida = request.form.get('temp_bebida')
            temp_proteico = request.form.get('temp_proteico')
            temp_cereal = request.form.get('temp_cereal')

            concepto_temp_bebida = request.form.get('concepto_temp_bebida')
            concepto_temp_proteico = request.form.get('concepto_temp_proteico')
            concepto_temp_cereal = request.form.get('concepto_temp_cereal')

            # Verificar que todos los campos estén completos
            if not all([temp_bebida, temp_proteico, temp_cereal, 
                        concepto_temp_bebida, concepto_temp_proteico, concepto_temp_cereal]):
                flash("Por favor completa todos los campos.", "warning")
                return redirect(url_for('tecnica.toma_peso'))

            # Insertar los datos en la base de datos
            cursor.execute("""
                INSERT INTO temperaturas (id_visita_tecnica, componente, temperatura, concepto)
                VALUES (%s, %s, %s, %s)
            """, (visita_id, 'Bebida', temp_bebida, concepto_temp_bebida))

            cursor.execute("""
                INSERT INTO temperaturas (id_visita_tecnica, componente, temperatura, concepto)
                VALUES (%s, %s, %s, %s)
            """, (visita_id, 'Proteico', temp_proteico, concepto_temp_proteico))

            cursor.execute("""
                INSERT INTO temperaturas (id_visita_tecnica, componente, temperatura, concepto)
                VALUES (%s, %s, %s, %s)
            """, (visita_id, 'Cereal', temp_cereal, concepto_temp_cereal))

            conn.commit()
            flash("Datos guardados exitosamente.", "success")
            
             # Verificar que el ID guardado sigue siendo el correcto
            print(f"ID tecnica antes de redirigir: {visita_id}")  # ✅ Depuración final

            return redirect(url_for('tecnica.detalle_tecnica', id_visita_tecnica=visita_id))


            # rol_usuario = session.get('rol')
            # if rol_usuario == 'administrador':
            #     return redirect(url_for('iniciasesion_bp.dashboard_administrador'))
            # elif rol_usuario == 'supervisor':
            #     return redirect(url_for('iniciasesion_bp.dashboard_supervisor'))
            # else:
            #     flash(f"Rol no reconocido: {rol_usuario}.", "danger")
            #     return redirect(url_for('iniciasesion_bp.login'))

    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
        return redirect(url_for('tecnica.toma_peso'))

    finally:
        cursor.close()
        conn.close()




@tecnica_bp.route('/lista_tecnica', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def lista_tecnica():
    conn = obtener_conexion()
    cursor = conn.cursor()

    try:
        # Consulta para obtener las visitas técnicas
        sql_visitas = """
            SELECT visita_tecnica.id_visita_tecnica, visita_tecnica.fecha_visita, visita_tecnica.hora_visita, operadores.nombre as operador,
                   instituciones.sede_educativa AS institucion, sedes.nombre_sede AS sede, 
                   visita_tecnica.focalizacion, visita_tecnica.tipo_racion_tecnica, 
                   visita_tecnica.codigo_sede, visita_tecnica.direccion, visita_tecnica.zona
            FROM visita_tecnica
            JOIN instituciones ON visita_tecnica.institucion_id = instituciones.id_institucion
            JOIN operadores ON visita_tecnica.operador = operadores.id_operador
            JOIN sedes ON visita_tecnica.sede_id = sedes.id_sede
            ORDER BY visita_tecnica.id_visita_tecnica ASC
        """
        cursor.execute(sql_visitas)
        visitas = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener visitas técnicas: {e}")
        visitas = []
    finally:
        cursor.close()
        conn.close()

    # Renderiza la plantilla con los datos de las visitas
    return render_template('lista_tecnica.html', visitas=visitas, rol=session.get('rol'), usuario=session.get('nombre'))

from flask import request, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame, KeepInFrame
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import pymysql
from reportlab.graphics.barcode import code128

@tecnica_bp.route('/detalle_tecnica/<int:id_visita_tecnica>', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def detalle_tecnica(id_visita_tecnica):
    conn = obtener_conexion()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Consulta para obtener detalles de la visita
        sql_visita = """
            SELECT vt.id_visita_tecnica, vt.fecha_visita, vt.hora_visita, operadores.nombre as operador , 
                   vt.focalizacion, vt.tipo_racion_tecnica, vt.codigo_sede, vt.direccion, 
                   vt.zona, instituciones.sede_educativa AS institucion, 
                   sedes.nombre_sede AS sede, vt.observacion_general
            FROM visita_tecnica vt
            JOIN instituciones ON vt.institucion_id = instituciones.id_institucion
            JOIN operadores ON vt.operador = operadores.id_operador
            JOIN sedes ON vt.sede_id = sedes.id_sede
            WHERE vt.id_visita_tecnica = %s
        """
        cursor.execute(sql_visita, (id_visita_tecnica,))
        visita = cursor.fetchone()

        if not visita:
            return "No se encontró la visita técnica especificada.", 404

        # Consulta para obtener preguntas y respuestas
        sql_preguntas_respuestas = """
            SELECT pt.categorias AS categoria, pt.numero, pt.preguntas, 
                   rt.respuesta, rt.observaciones
            FROM preguntas_tecnica pt
            LEFT JOIN respuestas_tecnica rt ON pt.id_tecnica = rt.pregunta_id
            WHERE rt.visita_tecnica_id = %s
            ORDER BY pt.numero
        """
        cursor.execute(sql_preguntas_respuestas, (id_visita_tecnica,))
        preguntas_respuestas = cursor.fetchall()

        # Validar si hay preguntas y respuestas
        if not preguntas_respuestas:
            preguntas_respuestas = []
            
        # Obtener los datos relacionados en otras tablas
        cursor.execute("""
            SELECT * FROM toma_peso
            WHERE id_visita_tecnica = %s
        """, (id_visita_tecnica,))
        toma_peso = cursor.fetchone()

        cursor.execute("""
            SELECT * FROM componente_alimentario_1
            WHERE id_visita_tecnica = %s
        """, (id_visita_tecnica,))
        componente_alimentario = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM componente_alimentario_promedio
            WHERE id_visita_tecnica = %s
        """, (id_visita_tecnica,))
        componente_alimentario_promedio = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM temperaturas
            WHERE id_visita_tecnica = %s
        """, (id_visita_tecnica,))
        temperaturas = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM firmas_tecnica
            WHERE id_visita_tecnica = %s
        """, (id_visita_tecnica,))
        firmas = cursor.fetchone()
        
        cursor.execute("""
            SELECT * FROM archivos_visita_tecnica
            WHERE visita_tecnica_id = %s
        """, (id_visita_tecnica,))
        archivos = cursor.fetchall()
        

    except Exception as e:
        print(f"Error al obtener detalles de la visita: {e}")
        visita = None
        preguntas_respuestas = []
    finally:
        cursor.close()
        conn.close()

    # Manejo del formulario de firmas y generación del PDF
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre_representante = request.form.get('nombre_representante')
        cedula_representante = request.form.get('cedula_representante')
        nombre_profesional = request.form.get('nombre_profesional')
        cedula_profesional = request.form.get('cedula_profesional')
        accion = request.form.get('accion') 

        # Validar que los datos no estén vacíos
        if not all([nombre_representante, cedula_representante, nombre_profesional, cedula_profesional]):
            return "Faltan datos en el formulario.", 400

        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                # Verificar si ya existe una firma para esta visita
                cursor.execute("SELECT COUNT(*) FROM firmas_tecnica WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
                resultado = cursor.fetchone()
                
                print("Resultado de la consulta:", resultado) 

                # Asegurar que resultado no sea None y acceder correctamente
                existe_firma = resultado['COUNT(*)'] if resultado else 0

                if existe_firma > 0:
                    flash("Ya existe una firma registrada para esta visita.", "warning")
                else:
                    sql = """
                        INSERT INTO firmas_tecnica (id_visita_tecnica, nombre_representante, cedula_representante, nombre_profesional, cedula_profesional)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (id_visita_tecnica, nombre_representante, cedula_representante, nombre_profesional, cedula_profesional))
                    conexion.commit()
                    flash("Firma registrada exitosamente.", "success")
        except pymysql.MySQLError as e:
            flash(f"Error al insertar la firma: {e}", "danger")
        finally:
            if conexion:
                conexion.close()

        if accion == "guardar_pdf":
            # Generar PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Estilo del documento
            styles = getSampleStyleSheet()
            estilo_titulo = styles['Title']
            estilo_normal = styles['Normal']


            # Contenido del PDF
            elementos = []
            
            # Generar el ID técnica y el código de barras
            id_tecnica = f"T{visita['id_visita_tecnica']}"
            fecha_visita = visita['fecha_visita'].strftime('%Y-%m-%d')  # Formato de fecha
            barcode_data = f"{id_tecnica} - {fecha_visita}"  # Datos clave para el código de barras
            barcode = code128.Code128(barcode_data, barWidth=0.015 * inch, barHeight=0.35 * inch)  # Más estrecho y compacto

            # Texto para mostrar debajo del código de barras
            barcode_text = f"{fecha_visita} - {id_tecnica}"

            # Crear un estilo para el texto
            styles = getSampleStyleSheet()
            barcode_text_style = styles['Normal']

            # Crear un contenedor para el código de barras y el texto
            barcode_frame = []
            barcode_frame.append(barcode)
            barcode_frame.append(Spacer(1, 6))  # Espaciado pequeño entre el código de barras y el texto
            barcode_frame.append(Paragraph(barcode_text, barcode_text_style))

            # Ajustar la posición del contenedor hacia la derecha
            frame = Frame(x1=300, y1=650, width=200, height=100, showBoundary=0)  # Ajustar `x1` y `y1` según tu necesidad
            elementos.append(KeepInFrame(200, 100, barcode_frame, mode='shrink'))

            # Título
            elementos.append(Paragraph("Visita Técnica", estilo_titulo))
            elementos.append(Spacer(1, 12))

            # Información General       
            elementos.append(Paragraph(f"ID Técnica: {id_tecnica}", estilo_normal))
            elementos.append(Paragraph(f"Fecha de Visita: {fecha_visita}", estilo_normal))
            elementos.append(Paragraph(f"Hora de Visita: {visita['hora_visita']}", estilo_normal))
            elementos.append(Paragraph(f"Operador: {visita['operador']}", estilo_normal))
            elementos.append(Paragraph(f"Institución: {visita['institucion']}", estilo_normal))
            elementos.append(Paragraph(f"Sede: {visita['sede']}", estilo_normal))
            elementos.append(Paragraph(f"Focalización: {visita['focalizacion']}", estilo_normal))
            elementos.append(Paragraph(f"Tipo de Ración Técnica: {visita['tipo_racion_tecnica']}", estilo_normal))
            elementos.append(Paragraph(f"Código Sede: {visita['codigo_sede']}", estilo_normal))
            elementos.append(Paragraph(f"Dirección: {visita['direccion']}", estilo_normal))
            elementos.append(Paragraph(f"Zona: {visita['zona']}", estilo_normal))
            elementos.append(Spacer(1, 12))

            # Generar código de barras
            

            if preguntas_respuestas:

                # Agrupar preguntas por categorías
                categorias = {}
                for pregunta in preguntas_respuestas:
                    categoria = str(pregunta.get('categoria', 'Sin Categoría'))
                    if categoria not in categorias:
                        categorias[categoria] = {'preguntas': [], 'cumplimiento': 0, 'total': 0}

                    # Procesar respuestas
                    respuesta = str(pregunta.get('respuesta', 'N/A'))
                    if respuesta == '2':  # Si la respuesta es "2", cambiar a "N/A"
                        respuesta = "N/A"
                    elif respuesta in ['1', '0']:  # Solo contar 1 y 0 como respuestas válidas
                        categorias[categoria]['cumplimiento'] += int(respuesta)
                        categorias[categoria]['total'] += 1

                    pregunta['respuesta'] = respuesta  # Actualizar la respuesta procesada
                    categorias[categoria]['preguntas'].append(pregunta)

                # Calcular totales y construir la tabla por categoría
                total_preguntas = 0
                total_cumplimiento = 0

                for categoria, datos in categorias.items():
                    cumplimiento = datos['cumplimiento']
                    preguntas = datos['total']
                    porcentaje = (cumplimiento / preguntas * 100) if preguntas > 0 else 0

                    # Clasificar el porcentaje
                    if porcentaje >= 80:
                        clasificacion = "Adecuado"
                    elif 61 <= porcentaje < 80:
                        clasificacion = "Regular"
                    else:
                        clasificacion = "Malo"

                    # Agregar título de la categoría
                    elementos.append(Paragraph(f"<b>{categoria}</b>", estilo_normal))
                    elementos.append(Spacer(1, 6))

                    # Crear una tabla para preguntas
                    tabla_datos = []

                    # Encabezados de la tabla de preguntas
                    encabezados = [
                        Paragraph("N°", estilo_normal),
                        Paragraph("Pregunta", estilo_normal),
                        Paragraph("Respuesta", estilo_normal),
                        Paragraph("Observaciones", estilo_normal),
                        Paragraph("Foto", estilo_normal)
                    ]
                    tabla_datos.append(encabezados)

                    # Agregar las preguntas
                    for pregunta in datos['preguntas']:
                        fila = [
                            Paragraph(str(pregunta.get('numero', 'N/A')), estilo_normal),
                            Paragraph(str(pregunta.get('preguntas', 'N/A')), estilo_normal),
                            Paragraph(str(pregunta.get('respuesta', 'N/A')), estilo_normal),
                            Paragraph(str(pregunta.get('foto_tecnica', 'N/A')), estilo_normal)
                        ]
                        tabla_datos.append(fila)

                    # Fila de subtotales (porcentaje y clasificación) al final de la tabla
                    tabla_datos.append([
                        Paragraph(f"SubTotal", estilo_normal),
                        Paragraph(f"{cumplimiento} / {preguntas} * 100 = {porcentaje:.2f}%", estilo_normal),
                        Paragraph(f"{clasificacion}", estilo_normal),
                        Paragraph("", estilo_normal)  # Espacio vacío para la última columna
                    ])

                    # Crear tabla con datos
                    tabla = Table(tabla_datos, colWidths=[60, 250, 70, 100])

                    # Aplicar estilo a la tabla
                    estilo_tabla = TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
                    ])
                    tabla.setStyle(estilo_tabla)

                    # Agregar tabla a los elementos
                    elementos.append(tabla)
                    elementos.append(Spacer(1, 12))

                    # Actualizar totales generales
                    total_preguntas += preguntas
                    total_cumplimiento += cumplimiento

                # Calcular total general
                porcentaje_general = (total_cumplimiento / total_preguntas * 100) if total_preguntas > 0 else 0
                if porcentaje_general >= 80:
                    clasificacion_general = "Adecuado"
                elif 61 <= porcentaje_general < 80:
                    clasificacion_general = "Regular"
                else:
                    clasificacion_general = "Malo"

                # Agregar total general al final
                elementos.append(Paragraph("<b>Total General</b>", estilo_normal))
                tabla_total = Table([[
                    Paragraph(f"Totales", estilo_normal),
                    Paragraph(f"{total_cumplimiento} / {total_preguntas} * 100 = {porcentaje_general:.2f}%", estilo_normal),
                    Paragraph(f"{clasificacion_general}", estilo_normal)
                ]], colWidths=[150, 150, 150])

                tabla_total.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
                ]))
                elementos.append(tabla_total)
            else:
                elementos.append(Paragraph("No se encontraron preguntas y respuestas asociadas.", estilo_normal))

            # Firmas
            
            
            
            if visita.get('id_visita_tecnica') and toma_peso:
            
                elementos.append(Paragraph("Toma de Peso y Temperatura Ración Preparada en Sitio", estilo_titulo))
                elementos.append(Spacer(1, 12))

                # Información de desperdicio y menú del día
                elementos.append(Paragraph(f"Desperdicio: {toma_peso['desperdicio']}", estilo_normal))
                elementos.append(Paragraph(f"Menú del Día: {toma_peso['menu_del_dia']}", estilo_normal))
                elementos.append(Spacer(1, 12))

                # Crear la tabla
                data = [
                    ["Nivel", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5", "Total"],
                    [
                        "Preparado en Sitio",
                        toma_peso['nivel1'],
                        toma_peso['nivel2'],
                        toma_peso['nivel3'],
                        toma_peso['nivel4'],
                        toma_peso['nivel5'],
                        toma_peso['total']
                    ]
                ]

                # Estilo de la tabla
                table = Table(data, colWidths=[80] + [60] * 6)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),  # Encabezado con fondo gris claro
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                elementos.append(table)
                elementos.append(Spacer(1, 12))

            else:
            # Mostrar mensaje si no hay datos
                elementos.append(Paragraph(" ", estilo_normal))
                
            if visita.get('id_visita_tecnica') and componente_alimentario:
                elementos.append(Paragraph("Cumplimiento de Gramajes Preparados AM/PM", estilo_titulo))
                elementos.append(Spacer(1, 5))
                elementos.append(Paragraph("Tabla 1: Componente Alimentario (AM/PM)", estilo_titulo))
                elementos.append(Spacer(1, 3))
                
                # Crear la tabla con los datos de componente_alimentario
                data = [
                    ["Muestra", "Componente", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4", "Nivel 5"]
                ]
                
                muestra_anterior = None
                componente_anterior = None
                for componente in componente_alimentario:
                    # Si el valor de "Muestra" es diferente del anterior, mostrarlo normalmente
                    if componente['muestra'] != muestra_anterior:
                        data.append([
                            componente['muestra'],  # Solo aparece una vez el valor de "Muestra"
                            componente['componente'],
                            componente['nivel_1'],
                            componente['nivel_2'],
                            componente['nivel_3'],
                            componente['nivel_4'],
                            componente['nivel_5']
                        ])
                    else:
                        # Si la muestra es la misma, dejar vacío solo las celdas de la "Muestra"
                        data.append([
                            "",  # Muestra vacía para las filas repetidas
                            componente['componente'],
                            componente['nivel_1'],
                            componente['nivel_2'],
                            componente['nivel_3'],
                            componente['nivel_4'],
                            componente['nivel_5']
                        ])
                    
                    # Actualizar muestra_anterior para verificar si es una nueva fila
                    muestra_anterior = componente['muestra']
                
                # Crear la tabla
                tabla = Table(data)
                
                # Estilos para la tabla
                estilo_tabla = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ])
                
                tabla.setStyle(estilo_tabla)
                elementos.append(tabla)
                elementos.append(Spacer(1, 12))
                
            elif not visita.get('id_visita_tecnica'):
                elementos.append(Paragraph(" ", estilo_normal))
        
            if visita.get('id_visita_tecnica') and componente_alimentario_promedio:
                # Títulos y encabezados
                elementos.append(Paragraph("Tabla 2: Componente Alimentario (AM/PM)", estilo_titulo))
                elementos.append(Spacer(1, 5))
                elementos.append(Paragraph("Promedio Ponderado", estilo_titulo))
                elementos.append(Spacer(1, 5))

                data = [
                    ["Grupos", 
                    "Bebida", "Proteico", "Cereal", "Fruta", 
                    "Bebida", "Proteico", "Cereal", "Fruta", 
                    "Bebida", "Proteico", "Cereal", "Fruta"]
                ]
                
                # Fila para los encabezados que usa el colspan
                encabezados = [
                    "Grupos",
                    "Peso Minuta Patrón (g)",
                    "Peso Promedio Obtenido (g)",
                    "Concepto (C/NC)"
                ]

                # Crear la fila de encabezados con el uso de colspan
                data.insert(0, encabezados)

                # Ahora añadir las filas de datos con los componentes
                for componente in componente_alimentario_promedio:
                    data.append([
                        componente['nivel_escolar'],  # Grupo
                        componente['peso_patron_bebida'],
                        componente['peso_patron_proteico'],
                        componente['peso_patron_cereal'],
                        componente['peso_patron_fruta'],
                        componente['peso_obtenido_bebida'],
                        componente['peso_obtenido_proteico'],
                        componente['peso_obtenido_cereal'],
                        componente['peso_obtenido_fruta'],
                        componente['concepto_bebida'],
                        componente['concepto_proteico'],
                        componente['concepto_cereal'],
                        componente['concepto_fruta']
                    ])
                
                # Crear la tabla con los datos
                tabla = Table(data)

                # Estilos para la tabla
                estilo_tabla = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fila de encabezado
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto en encabezado
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrado de texto
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita en encabezado
                    ('FONTSIZE', (0, 0), (-1, -1), 8),  # Tamaño de fuente
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Relleno debajo del encabezado
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Fondo blanco para filas de datos
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Rejilla
                    # Definir el colspan para las cabeceras de las columnas
                    ('SPAN', (1, 0), (4, 0)),  # Colspan para "Peso Minuta Patrón (g)" de las columnas 1 a 4
                    ('SPAN', (5, 0), (8, 0)),  # Colspan para "Peso Promedio Obtenido (g)" de las columnas 5 a 8
                    ('SPAN', (9, 0), (12, 0))  # Colspan para "Concepto (C/NC)" de las columnas 9 a 12
                ])
                
                tabla.setStyle(estilo_tabla)

                # Agregar la tabla a los elementos
                elementos.append(tabla)


                # Leyenda
                elementos.append(Spacer(1, 10))
                elementos.append(Paragraph("C: Cumple, N/C: No Cumple, N/A: No Aplica", estilo_normal))
                elementos.append(Spacer(1, 12))
                
            else:
                # Si no hay datos para la visita técnica
                elementos.append(Paragraph(" ", estilo_normal))
                
            
        
            if visita.get('id_visita_tecnica') and temperaturas:
                elementos.append(Paragraph("Temperaturas", estilo_titulo))
                elementos.append(Spacer(1, 5))
                
                # Crear la tabla de temperaturas
                data = [
                    ["Componente", "Temperatura (°C)", "Concepto"]
                ]
                
                for temp in temperaturas:
                    data.append([
                        temp['componente'], 
                        f"{temp['temperatura']}°C", 
                        temp['concepto']
                    ])
                
                # Crear la tabla
                tabla = Table(data, colWidths=[150, 100, 150])
                
                # Estilos para la tabla
                estilo_tabla = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reducir tamaño de fuente
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ])
                
                tabla.setStyle(estilo_tabla)
                elementos.append(tabla)
                
                # Agregar el pie de página para la tabla
                elementos.append(Spacer(1, 10))
                elementos.append(Paragraph("C: Cumple, N/C: No Cumple, N/A: No Aplica", estilo_normal))
                elementos.append(Spacer(1, 12))
                
            elif not visita.get('id_visita_tecnica'):
                elementos.append(Paragraph(" ", estilo_normal))
                
                
            elementos.append(Paragraph(f"Observación: {visita['observacion_general']}", estilo_normal))
            elementos.append(Spacer(1, 12))

            elementos.append(Paragraph("Firmas", styles['Heading2']))
            elementos.append(Paragraph(f"Nombre Representante: {nombre_representante}", estilo_normal))
            elementos.append(Paragraph(f"Cédula Representante: {cedula_representante}", estilo_normal))
            elementos.append(Spacer(1, 12))
            elementos.append(Paragraph(f"Nombre Visita Profesional: {nombre_profesional}", estilo_normal))
            elementos.append(Paragraph(f"Cédula Profesional: {cedula_profesional}", estilo_normal))
            elementos.append(Spacer(1, 12))


            # Construir el PDF
            doc.build(elementos)

            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=f"visita_tecnica_{id_tecnica}.pdf", mimetype='application/pdf')


    # Renderizar en caso de GET
    return render_template(
        'detalle_tecnica.html',
        visita=visita,
        toma_peso=toma_peso, componente_alimentario=componente_alimentario,
        componente_alimentario_promedio=componente_alimentario_promedio,
        temperaturas=temperaturas,
        preguntas_respuestas=preguntas_respuestas,
        firmas=firmas,
        archivos=archivos,
        rol=session.get('rol'),
        usuario=session.get('nombre')
    )


@tecnica_bp.route('/editar_visita/<int:id_visita_tecnica>', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def editar_visita(id_visita_tecnica):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        datos_visita = {
            'fecha_visita': request.form['fecha_visita'],
            'hora_visita': request.form['hora_visita'],
            'focalizacion': request.form['focalizacion'],
            'operador': request.form['operador'],
            'institucion_id': request.form['institucion_id'],
            'sede_id': request.form['sede_id'],
            'tipo_racion_tecnica': request.form['tipo_racion_tecnica'],
            'observacion_general': request.form['observacion_general']
        }
        
        cursor.execute("""
            UPDATE visita_tecnica SET fecha_visita = %(fecha_visita)s, hora_visita = %(hora_visita)s,
            focalizacion = %(focalizacion)s, tipo_racion_tecnica = %(tipo_racion_tecnica)s, operador = %(operador)s,
            institucion_id = %(institucion_id)s, sede_id = %(sede_id)s,
            observacion_general = %(observacion_general)s WHERE id_visita_tecnica = %(id_visita_tecnica)s
        """, {**datos_visita, 'id_visita_tecnica': id_visita_tecnica})
        
        preguntas = request.form.getlist('pregunta_id')
        respuestas = request.form.getlist('respuesta')
        observaciones = request.form.getlist('observaciones')
        for i in range(len(preguntas)):
            cursor.execute("""
                UPDATE respuestas_tecnica SET respuesta = %s, observaciones = %s 
                WHERE pregunta_id = %s AND visita_tecnica_id = %s
            """, (respuestas[i], observaciones[i], preguntas[i], id_visita_tecnica))
        
        # Obtener datos del formulario
        desperdicio = request.form['desperdicio']
        menu_del_dia = request.form['menu_del_dia']
        nivel1 = request.form['nivel1']
        nivel2 = request.form['nivel2']
        nivel3 = request.form['nivel3']
        nivel4 = request.form['nivel4']
        nivel5 = request.form['nivel5']
        total = request.form['total']
        observacion = request.form['observacion_toma_peso']

        # Conectar a la base de datos
        # Actualizar datos en la tabla
        cursor.execute("""
            UPDATE toma_peso 
            SET desperdicio = %s, menu_del_dia = %s, nivel1 = %s, nivel2 = %s, nivel3 = %s, 
                nivel4 = %s, nivel5 = %s, total = %s, observacion = %s
            WHERE id_visita_tecnica = %s
        """, (desperdicio, menu_del_dia, nivel1, nivel2, nivel3, nivel4, nivel5, total, observacion, id_visita_tecnica))
        
        # Bucle para actualizar cada fila de la tabla componente_alimentario_1
        for key, value in request.form.items():
            if key.startswith("nivel_"):  # Filtrar solo los campos de nivel
                id_componente = key.split("_")[2]  # Extraer el ID del componente
                nivel = key.split("_")[1]  # Extraer el nivel (1,2,3,4,5)

                # Actualizar el nivel en la base de datos
                cursor.execute(f"""
                    UPDATE componente_alimentario_1 
                    SET nivel_{nivel} = %s
                    WHERE id_componente_alimentario = %s AND id_visita_tecnica = %s
                """, (value, id_componente, id_visita_tecnica))
        
        # Recorrer los elementos enviados en el formulario
        for key, value in request.form.items():
            if key.startswith("peso_patron_bebida_"):
                id_promedio = key.split("_")[-1]  # Extraer el ID de la fila

                # Obtener los valores del formulario
                peso_patron_bebida = request.form.get(f"peso_patron_bebida_{id_promedio}")
                peso_patron_proteico = request.form.get(f"peso_patron_proteico_{id_promedio}")
                peso_patron_cereal = request.form.get(f"peso_patron_cereal_{id_promedio}")
                peso_patron_fruta = request.form.get(f"peso_patron_fruta_{id_promedio}")
                peso_obtenido_bebida = request.form.get(f"peso_obtenido_bebida_{id_promedio}")
                peso_obtenido_proteico = request.form.get(f"peso_obtenido_proteico_{id_promedio}")
                peso_obtenido_cereal = request.form.get(f"peso_obtenido_cereal_{id_promedio}")
                peso_obtenido_fruta = request.form.get(f"peso_obtenido_fruta_{id_promedio}")
                concepto_bebida = request.form.get(f"concepto_bebida_{id_promedio}")
                concepto_proteico = request.form.get(f"concepto_proteico_{id_promedio}")
                concepto_cereal = request.form.get(f"concepto_cereal_{id_promedio}")
                concepto_fruta = request.form.get(f"concepto_fruta_{id_promedio}")

                # Actualizar en la base de datos
                cursor.execute("""
                    UPDATE componente_alimentario_promedio
                    SET 
                        peso_patron_bebida = %s,
                        peso_patron_proteico = %s,
                        peso_patron_cereal = %s,
                        peso_patron_fruta = %s,
                        peso_obtenido_bebida = %s,
                        peso_obtenido_proteico = %s,
                        peso_obtenido_cereal = %s,
                        peso_obtenido_fruta = %s,
                        concepto_bebida = %s,
                        concepto_proteico = %s,
                        concepto_cereal = %s,
                        concepto_fruta = %s
                    WHERE id_promedio = %s
                """, (peso_patron_bebida, peso_patron_proteico, peso_patron_cereal, peso_patron_fruta, 
                    peso_obtenido_bebida, peso_obtenido_proteico, peso_obtenido_cereal, peso_obtenido_fruta, 
                    concepto_bebida, concepto_proteico, concepto_cereal, concepto_fruta, id_promedio))

                
        id_visita_tecnica = request.form.get("id_visita_tecnica")
        nombre_representante = request.form.get("nombre_representante")
        cedula_representante = request.form.get("cedula_representante")
        nombre_profesional = request.form.get("nombre_profesional")
        cedula_profesional = request.form.get("cedula_profesional")

        sql = """
            UPDATE firmas_tecnica
            SET nombre_representante = %s,
                cedula_representante = %s,
                nombre_profesional = %s,
                cedula_profesional = %s
            WHERE id_visita_tecnica = %s
        """

        valores = (nombre_representante, cedula_representante, nombre_profesional, cedula_profesional, id_visita_tecnica)
        
        cursor.execute(sql, valores)
            
        for key, value in request.form.items():
            if key.startswith("temperatura_"):
                id_temperatura = key.split("_")[-1]  # Extrae el ID del registro

                temperatura = request.form.get(f"temperatura_{id_temperatura}")
                concepto = request.form.get(f"concepto_{id_temperatura}")

                # Actualizar en la base de datos
                cursor.execute("""
                    UPDATE temperaturas
                    SET temperatura = %s, concepto = %s
                    WHERE id_temperatura = %s
                """, (temperatura, concepto, id_temperatura))
            
        conexion.commit()
        flash('Visita actualizada correctamente', 'success')
        return redirect(url_for('tecnica.detalle_tecnica', id_visita_tecnica=id_visita_tecnica))
    
    cursor.execute("""SELECT vt.id_visita_tecnica, vt.fecha_visita, vt.hora_visita, vt.focalizacion, op.nombre, 
                   ins.sede_educativa, sed.nombre_sede, vt.tipo_racion_tecnica, vt.observacion_general FROM visita_tecnica vt
                   LEFT JOIN instituciones ins ON vt.institucion_id = ins.id_institucion
                   LEFT JOIN sedes sed ON vt.sede_id = sed.id_sede
                   LEFT JOIN operadores op ON vt.operador = op.id_operador
                   WHERE id_visita_tecnica = %s""", (id_visita_tecnica,))
    visita = cursor.fetchone()
    
    if isinstance(visita['hora_visita'], timedelta):
        segundos_totales = visita['hora_visita'].total_seconds()
        horas = int(segundos_totales // 3600)
        minutos = int((segundos_totales % 3600) // 60)
        visita['hora_visita'] = f"{horas:02}:{minutos:02}"
    
    cursor.execute("""
        SELECT rt.pregunta_id, rt.respuesta, rt.observaciones, pt.preguntas, pt.numero FROM respuestas_tecnica rt 
        LEFT JOIN preguntas_tecnica pt ON pt.id_tecnica = rt.pregunta_id WHERE rt.visita_tecnica_id = %s
        ORDER BY pt.numero
    """, (id_visita_tecnica,))
    preguntas_respuestas = cursor.fetchall()
    
    cursor.execute("SELECT * FROM toma_peso WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
    toma_peso = cursor.fetchone()
    
    cursor.execute("SELECT * FROM componente_alimentario_1 WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
    componente_1 = cursor.fetchall()
    
    cursor.execute("SELECT * FROM componente_alimentario_promedio WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
    componente_promedio = cursor.fetchall()
    
    cursor.execute("SELECT * FROM temperaturas WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
    temperaturas = cursor.fetchall()
    
    
    cursor.execute("SELECT * FROM firmas_tecnica WHERE id_visita_tecnica = %s", (id_visita_tecnica,))
    firmas = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    operadores = obtener_operador()
    instituciones = obtener_institucion()
    tipos_racion = obtener_tipo_racion()    
    
    return render_template('editar_tecnica.html', operadores =operadores, instituciones=instituciones, tipos_racion = tipos_racion, visita=visita, preguntas_respuestas=preguntas_respuestas, 
                           toma_peso=toma_peso, temperaturas=temperaturas, componente_alimentario = componente_1,
                           componente_promedio=componente_promedio, firmas=firmas, rol=session.get('rol'),  usuario=session.get('nombre'))
    
    
@tecnica_bp.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return "Debes proporcionar los parámetros 'fecha_inicio' y 'fecha_fin'", 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Obtener todas las visitas en el rango de fechas
        cursor.execute("""
            SELECT vt.id_visita_tecnica, vt.fecha_visita, vt.hora_visita, operadores.nombre as operador, 
                   vt.focalizacion, vt.tipo_racion_tecnica, vt.codigo_sede, vt.direccion, 
                   vt.zona, instituciones.sede_educativa AS institucion, 
                   sedes.nombre_sede AS sede, vt.observacion_general
            FROM visita_tecnica vt
            JOIN instituciones ON vt.institucion_id = instituciones.id_institucion
            JOIN operadores ON vt.operador = operadores.id_operador
            JOIN sedes ON vt.sede_id = sedes.id_sede
            WHERE vt.fecha_visita BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        visitas = cursor.fetchall()

        # Obtener todas las preguntas y respuestas dentro del rango de fechas
        cursor.execute("""
            SELECT rt.id_respuesta, pt.categorias AS categoria, pt.numero, pt.preguntas, 
                   rt.respuesta, rt.observaciones, rt.visita_tecnica_id
            FROM preguntas_tecnica pt
            LEFT JOIN respuestas_tecnica rt ON pt.id_tecnica = rt.pregunta_id
            JOIN visita_tecnica vt ON rt.visita_tecnica_id = vt.id_visita_tecnica
            WHERE vt.fecha_visita BETWEEN %s AND %s
            ORDER BY pt.id_tecnica
        """, (fecha_inicio, fecha_fin))
        preguntas_respuestas = cursor.fetchall()

        # Obtener los demás datos relacionados con las visitas en el rango de fechas
        cursor.execute("SELECT * FROM toma_peso WHERE id_visita_tecnica IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        toma_peso = cursor.fetchall()

        cursor.execute("SELECT * FROM componente_alimentario_1 WHERE id_visita_tecnica IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        componente_alimentario = cursor.fetchall()

        cursor.execute("SELECT * FROM componente_alimentario_promedio WHERE id_visita_tecnica IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        componente_alimentario_promedio = cursor.fetchall()

        cursor.execute("SELECT * FROM temperaturas WHERE id_visita_tecnica IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        temperaturas = cursor.fetchall()

        cursor.execute("SELECT * FROM firmas_tecnica WHERE id_visita_tecnica IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        firmas = cursor.fetchall()

        cursor.execute("SELECT * FROM archivos_visita_tecnica WHERE visita_tecnica_id IN (SELECT id_visita_tecnica FROM visita_tecnica WHERE fecha_visita BETWEEN %s AND %s)", (fecha_inicio, fecha_fin))
        archivos = cursor.fetchall()

    conexion.close()

    # Crear archivo Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    if visitas:
        df_visitas = pd.DataFrame(visitas)
        df_visitas.to_excel(writer, sheet_name='Visitas Técnicas', index=False)

    if preguntas_respuestas:
        df_preguntas = pd.DataFrame(preguntas_respuestas)
        df_preguntas.to_excel(writer, sheet_name='Preguntas y Respuestas', index=False)

    if toma_peso:
        df_peso = pd.DataFrame(toma_peso)
        df_peso.to_excel(writer, sheet_name='Toma de Peso', index=False)

    if componente_alimentario:
        df_alimentario = pd.DataFrame(componente_alimentario)
        df_alimentario.to_excel(writer, sheet_name='Componente Alimentario', index=False)

    if componente_alimentario_promedio:
        df_alimentario_prom = pd.DataFrame(componente_alimentario_promedio)
        df_alimentario_prom.to_excel(writer, sheet_name='Promedio Componente', index=False)

    if temperaturas:
        df_temperaturas = pd.DataFrame(temperaturas)
        df_temperaturas.to_excel(writer, sheet_name='Temperaturas', index=False)

    if firmas:
        df_firmas = pd.DataFrame(firmas)
        df_firmas.to_excel(writer, sheet_name='Firmas', index=False)

    if archivos:
        df_archivos = pd.DataFrame(archivos)
        df_archivos.to_excel(writer, sheet_name='Archivos Adjuntos', index=False)

    writer.close()
    output.seek(0)

    return send_file(
        output, 
        download_name=f'Visitas_{fecha_inicio}_a_{fecha_fin}.xlsx',
        as_attachment=True, 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )