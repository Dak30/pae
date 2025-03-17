from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file
from iniciasesion import login_required, session, role_required
import pymysql
import pandas as pd
from io import BytesIO
from database import get_db_connection


# Creamos un Blueprint para la infraestructura
infraestructura_bp = Blueprint('infraestructura', __name__, template_folder='templates/infraestructura')

def obtener_operador():
    """Obtiene la lista de operadores desde la base de datos."""
    conexion = get_db_connection('visitas', driver="pymysql")  # ✅ Correcto
  # Usar pymysql con DictCursor
    
    if not conexion:
        print("❌ Error: No se pudo conectar a la base de datos.")
        return []  # Devolver lista vacía en caso de error

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT DISTINCT id_operador, nombre FROM operadores")
            operadores = cursor.fetchall()  # Lista de diccionarios gracias a DictCursor
    except Exception as e:
        print(f"❌ Error al obtener operadores: {e}")
        operadores = []  # Lista vacía en caso de error
    finally:
        conexion.close()  # Cerrar conexión siempre

    return operadores


def obtener_institucion(id_operador):
    if not id_operador:
        return []  # Retorna una lista vacía si no hay operador seleccionado

    conexion = get_db_connection('visitas', driver="pymysql") 
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT id_institucion, sede_educativa FROM instituciones WHERE id_operador = %s", (id_operador,))
    instituciones = [{'id': row['id_institucion'], 'nombre': row['sede_educativa']} for row in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return instituciones


def obtener_sedes_por_institucion(institucion_id):
    conexion = get_db_connection('visitas', driver="pymysql") 
    cursor = conexion.cursor()
    cursor.execute("SELECT id_sede, nombre_sede FROM sedes WHERE id_institucion = %s", (institucion_id,))
    sedes = [{'id': row['id_sede'], 'nombre': row['nombre_sede']} for row in cursor.fetchall()]

    cursor.close()
    conexion.close()
    return sedes

def obtener_tipo_racion():
    conexion = get_db_connection('visitas', driver="pymysql") 
    cursor = conexion.cursor()

    cursor.execute("SELECT id_tipo_racion, descripcion FROM tiporacion WHERE id_tipo_racion IN (1, 2, 3, 4)")

    tipo_racion = [{'id': row['id_tipo_racion'], 'nombre': row['descripcion']} for row in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return tipo_racion


def obtener_preguntas_por_categoria():
    preguntas_por_categoria = {}
    
    try:
        # Conectar a la base de datos
        conexion = get_db_connection('visitas', driver="pymysql") 
        cursor = conexion.cursor()
        
        # Lista de categorías a consultar
        categorias = [
            'infraestructura',
            'area de preparacion de alimentos',
            'area de almacenamiento de alimentos',
            'area de distribucion de alimentos',
            'instalaciones sanitarias y de aseo',
            'servicios publicos',
            'dotacion de menaje'
        ]
        
        # Consultar preguntas para cada categoría
        for categoria in categorias:
            cursor.execute("SELECT id_pregunta, numero, descripcion FROM preguntas_infraestructura WHERE categoria = %s", (categoria,))
            preguntas_por_categoria[categoria] = [
                {'id': row['id_pregunta'], 'numero': row['numero'], 'descripcion': row['descripcion']}
                for row in cursor.fetchall()
            ]
    
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")
    
    finally:
        # Cerrar cursor y conexión
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()
    
    return preguntas_por_categoria


@infraestructura_bp.route('/infraestructura', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def mostrar_infraestructura():
    preguntas_por_categoria = obtener_preguntas_por_categoria()
    operadores = obtener_operador()
    
    # Obtener id_operador desde los argumentos o la sesión
    id_operador = request.args.get('id_operador') or session.get('id_operador')
    
    # Obtener las instituciones solo si hay un operador seleccionado
    instituciones = obtener_institucion(id_operador) if id_operador else []
    
    tipos_racion = obtener_tipo_racion()

    return render_template('infraestructura.html', 
                           preguntas_por_categoria=preguntas_por_categoria,
                           operadores=operadores, 
                           instituciones=instituciones, 
                           tipos_racion=tipos_racion, 
                           rol=session.get('rol'), 
                           usuario=session.get('nombre'))

@infraestructura_bp.route('/get_instituciones/<int:id_operador>', methods=['GET'])
@login_required
def get_instituciones(id_operador):
    instituciones = obtener_institucion(id_operador)
    return jsonify({'instituciones': instituciones})
    
    
@infraestructura_bp.route('/get_sede/<int:institucion_id>', methods=['GET'])
def get_sede(institucion_id):
    try:
        sedes = obtener_sedes_por_institucion(institucion_id)
        return jsonify({'sedes': sedes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@infraestructura_bp.route('/get_sede_details/<int:sede_id>', methods=['GET'])
def get_sede_details(sede_id):
    try:
        # Conectamos a la base de datos
        conexion = get_db_connection('visitas', driver="pymysql") 
        cursor = conexion.cursor()
        
        # Ejecutamos la consulta para obtener los detalles de la sede
        cursor.execute("SELECT codigo, direccion, comuna, zona FROM sedes WHERE id_sede = %s", (sede_id,))
        sede_details = cursor.fetchone()  # Suponemos que solo hay un resultado
        
        # Si no se encuentra la sede, retornamos un error
        if not sede_details:
            return jsonify({'error': 'Sede no encontrada'}), 404
        
        # Devolvemos los detalles de la sede en formato JSON
        return jsonify({
            'codigo': sede_details[0],
            'direccion': sede_details[1],
            'comuna': sede_details[2],
            'zona': sede_details[3]
        })
    except Exception as e:
        # En caso de error, retornamos el mensaje de error
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerramos la conexión y el cursor
        cursor.close()
        conexion.close()    
        

from flask import request, redirect, url_for, flash, current_app
import os
import time
from werkzeug.utils import secure_filename
from pymysql.cursors import DictCursor

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@infraestructura_bp.route('/guardar_infraestructura', methods=['POST'])
def guardar_infraestructura():
    try:
        # Conexión a la base de datos
        conexion = get_db_connection('visitas', driver="pymysql") 
        cursor = conexion.cursor(DictCursor)

        # Obtener datos del formulario
        fecha = request.form.get('fecha')
        municipio = request.form.get('municipio')
        corregimiento = request.form.get('corregimiento')
        vereda = request.form.get('vereda')
        operador = request.form.get('operador')
        institucion_id = request.form.get('institucion')  # ID de la institución
        sede_id = request.form.get('sede')  # ID de la sede

        # Validar que los IDs no sean nulos
        if not institucion_id or not sede_id:
            return jsonify({"error": "ID de institución o sede no proporcionados"}), 400

        # Obtener nombres de la institución y la sede
        sql_institucion = "SELECT sede_educativa FROM instituciones WHERE id_institucion = %s"
        cursor.execute(sql_institucion, (institucion_id,))
        institucion = cursor.fetchone()
        
        institucion_nombre = institucion['sede_educativa'] if institucion else "No encontrada"

        sql_sede = "SELECT nombre_sede FROM sedes WHERE id_sede = %s"
        cursor.execute(sql_sede, (sede_id,))
        sede = cursor.fetchone()
        
        sede_nombre = sede['nombre_sede'] if sede else "No encontrada"

        # Verificar si se encontraron los nombres
        if not institucion_nombre or not sede_nombre:
            return jsonify({"error": "Institución o sede no encontrados"}), 404

        # Extraer los nombres
        institucion_nombre = institucion_nombre[0]
        sede_nombre = sede_nombre[0]

        codigo_sede = request.form.get('codigo_sede')
        direccion = request.form.get('direccion')
        barrio = request.form.get('barrio')
        comuna = request.form.get('comuna')
        zona = request.form.get('zona')

        # Obtener múltiples tipos de ración seleccionados
        tipo_racion_seleccionado = request.form.getlist('tipo_racion')
        tipo_racion = ','.join(tipo_racion_seleccionado)

        focalizacion = request.form.get('focalizacion')
        observacion_general = request.form.get('observacion_general')

        # Insertar datos en la tabla infraestructura
        sql_infraestructura = """INSERT INTO infraestructura 
                                (fecha, municipio, corregimiento, vereda, operador, institucion, sede, codigo_sede, direccion, barrio, comuna, zona, tipo_racion, focalizacion, observacion_general)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        # Insertar datos en la tabla infraestructura
        cursor.execute(sql_infraestructura, (fecha, municipio, corregimiento, vereda, operador, institucion_id, sede_id, codigo_sede, direccion, barrio, comuna, zona, tipo_racion, focalizacion, observacion_general))

        # Guardar el ID correcto antes de otras inserciones
        id_infraestructura = cursor.lastrowid  # ✅ Guardamos la referencia correcta
        print(f"Numero de Infraestructura (guardado): {id_infraestructura}")  # ✅ Depuración

        # Insertar respuestas a las preguntas de Dotación de Menaje
        for key in request.form:
            if key.startswith('cantidad_'):
                pregunta_id = key.split('_')[1]
                cantidad = request.form.get(f'cantidad_{pregunta_id}')
                estados_seleccionados = request.form.getlist(f'estado_{pregunta_id}[]')
                estados = ','.join(estados_seleccionados)
                propiedades = request.form.getlist(f'propiedad_{pregunta_id}[]')
                propiedad = ','.join(propiedades)
                item = request.form.get(f'item_{pregunta_id}') or 'Desconocido'
                fotos = request.files.getlist(f'foto_{pregunta_id}')  

                # Carpeta donde se guardarán las fotos
                upload_folder = os.path.join(current_app.root_path, 'static/uploads/dotacion_menaje')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                foto_nombres = []  # Lista para guardar los nombres de las fotos

                for foto in fotos:
                    if foto and allowed_file(foto.filename):
                        filename = f"{int(time.time())}_{secure_filename(foto.filename)}"
                        foto_path = os.path.join(upload_folder, filename)
                        
                        print(f"Guardando foto en: {foto_path}")  
                        
                        foto.save(foto_path)
                        foto_nombres.append(filename)

                # Guardar los datos en la tabla dotacion_menaje
                foto_menaje = ",".join(foto_nombres) if foto_nombres else None

                sql_dotacion_menaje = """INSERT INTO dotacion_menaje (id_infraestructura, item, cantidad, estado, propiedad, foto_menaje)
                                        VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_dotacion_menaje, (id_infraestructura, item, cantidad, estados, propiedad, foto_menaje))

                print(f"Dotación guardada con {len(foto_nombres)} fotos.")


        for key in request.form:
            if key.startswith('pregunta_'):
                pregunta_id = key.split('_')[1]
                respuesta = request.form.get(key)
                observacion = request.form.get(f'observacion_{pregunta_id}')
                fotos = request.files.getlist(f'foto_{pregunta_id}')  

                print(f"Procesando pregunta {pregunta_id} - {len(fotos)} fotos recibidas.")  

                cursor.execute("SELECT descripcion FROM preguntas_infraestructura WHERE id_pregunta = %s", (pregunta_id,))
                pregunta = cursor.fetchone()

                pregunta_descripcion = pregunta['descripcion'] if pregunta else "Sin descripción"

                upload_folder = os.path.join(current_app.root_path, f'static/uploads/infraestructura/')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                foto_nombres = []

                for foto in fotos:
                    if foto and allowed_file(foto.filename):
                        filename = f"{int(time.time())}_{secure_filename(foto.filename)}"
                        foto_path = os.path.join(upload_folder, filename)
                        
                        print(f"Guardando foto en: {foto_path}")  
                        
                        foto.save(foto_path)
                        foto_nombres.append(filename)

                if pregunta_descripcion:
                    pregunta_descripcion = pregunta_descripcion[0]
                    sql_respuesta = """INSERT INTO respuestas_infraestructura 
                                    (id_pregunta, respuesta, observacion, id_infraestructura, descripcion, foto)
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql_respuesta, (pregunta_id, respuesta, observacion, id_infraestructura, pregunta_descripcion, ",".join(foto_nombres)))

                    print(f"Pregunta {pregunta_id} guardada con {len(foto_nombres)} fotos.")

        # Confirmar cambios en la base de datos
        conexion.commit()
        
        # Obtener el rol del usuario
        # rol_usuario = session.get('rol')

        # Verificar que el ID guardado sigue siendo el correcto
        print(f"ID infraestructura antes de redirigir: {id_infraestructura}")  # ✅ Depuración final

        return redirect(url_for('infraestructura.detalle_infraestructura', id_infraestructura=id_infraestructura))  # ✅ Redirige con el ID correcto

    except pymysql.MySQLError as e:
        print(f"Error en la conexión o transacción: {e}") 
        
        print(f"ID infraestructura antes de redirigir: {id_infraestructura}")# Ahora sí se imprimirá el error

        return redirect(url_for('infraestructura.detalle_infraestructura', id_infraestructura=id_infraestructura))


    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()  
        if 'conexion' in locals() and conexion:
            conexion.close()  
        
@infraestructura_bp.route('/eliminar_infraestructura/<int:id_infraestructura>', methods=['DELETE'])
@login_required
@role_required('supervisor', 'administrador')
def eliminar_infraestructura(id_infraestructura):
    try:
        # Obtener conexión a la base de datos
        conexion = pymysql.connect(
            host="127.0.0.1",
            user="Pae",
            password="Pae_educacion",
            db="visitas",
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM infraestructura WHERE id_infraestructura = %s", (id_infraestructura,))
        conexion.commit()
        
        return jsonify({'success': True, 'message': 'Visita de infraestructura eliminada correctamente'}), 200

    except pymysql.MySQLError as e:
        return jsonify({'success': False, 'message': f'Error al eliminar la visita: {e}'}), 500

    finally:
        if 'conexion' in locals() and conexion.open:
            conexion.close()  # Cerrar conexión solo si está abierta




@infraestructura_bp.route('/lista_infraestructura')
@login_required
@role_required('supervisor', 'administrador')
def lista_infraestructura():
    # Conexión a la base de datos
    conexion = get_db_connection('visitas', driver="pymysql") 
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    # Consulta para obtener todos los registros de infraestructura
    sql = """SELECT i.id_infraestructura, i.fecha, i.municipio, i.corregimiento, i.vereda, o.nombre AS nombre_operador, 
             inst.sede_educativa AS institucion_nombre, s.nombre_sede AS sede_nombre, i.codigo_sede, 
             i.direccion, i.barrio, i.comuna, i.zona, i.tipo_racion, i.focalizacion, i.observacion_general
             FROM infraestructura i
             JOIN instituciones inst ON i.institucion = inst.id_institucion
             JOIN operadores o ON i.operador = o.id_operador
             JOIN sedes s ON i.sede = s.id_sede"""
    
    cursor.execute(sql)
    infraestructuras = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Renderizar la plantilla con los datos de infraestructura
    return render_template('lista_infraestructura.html', infraestructuras=infraestructuras, rol=session.get('rol'), usuario=session.get('nombre'))

import io
import pandas as pd
from flask import send_file, request, flash, redirect, url_for

def obtener_conexion():
    return get_db_connection('visitas', driver="pymysql") 


@infraestructura_bp.route('/exportar_infraestructura', methods=['GET'])
@login_required
@role_required('supervisor', 'administrador')
def exportar_infraestructura():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    conn = None
    cursor = None

    try:
        conn = obtener_conexion()
        if not conn:
            flash('Error al conectar con la base de datos.', 'danger')
            return redirect(url_for('infraestructura.lista_infraestructura'))

        cursor = conn.cursor()

        print(f"📅 Filtrando datos desde: {fecha_inicio} hasta: {fecha_fin}")

        # 🔹 Consultas separadas para cada pestaña
        consultas = {
            "Infraestructura": """
                SELECT DISTINCT i.id_infraestructura, i.fecha, i.municipio, i.corregimiento, i.vereda, 
                    o.nombre AS nombre_operador, inst.sede_educativa AS institucion_nombre, 
                    s.nombre_sede AS sede_nombre, i.codigo_sede, i.direccion, i.barrio, i.comuna, 
                    i.zona, i.tipo_racion, i.focalizacion, i.observacion_general
                FROM infraestructura i
                JOIN instituciones inst ON i.institucion = inst.id_institucion
                JOIN operadores o ON i.operador = o.id_operador
                JOIN sedes s ON i.sede = s.id_sede
                WHERE 1=1
            """,
            "Respuestas Infraestructura": """
                SELECT i.id_infraestructura, p.numero AS pregunta_numero, p.descripcion AS pregunta_descripcion, 
                    r.respuesta, r.observacion AS respuesta_observacion, r.foto AS respuesta_foto
                FROM infraestructura i
                LEFT JOIN respuestas_infraestructura r ON i.id_infraestructura = r.id_infraestructura
                LEFT JOIN preguntas_infraestructura p ON r.id_pregunta = p.id_pregunta
                WHERE 1=1
            """,
            "Dotación de Menaje": """
                SELECT i.id_infraestructura, dm.item AS dotacion_item, dm.cantidad, 
                    dm.estado, dm.propiedad, dm.foto_menaje
                FROM infraestructura i
                LEFT JOIN dotacion_menaje dm ON i.id_infraestructura = dm.id_infraestructura
                WHERE 1=1
            """,
            "Firmas Infraestructura": """
                SELECT i.id_infraestructura, f.nombre_representante_ieo, f.nombre_profesional
                FROM infraestructura i
                LEFT JOIN firmas_infraestructura f ON i.id_infraestructura = f.id_infraestructura
                WHERE 1=1
            """
        }

        params = []
        if fecha_inicio:
            for key in consultas:
                consultas[key] += " AND i.fecha >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            for key in consultas:
                consultas[key] += " AND i.fecha <= %s"
            params.append(fecha_fin)

        # 🔹 Ejecutar las consultas y almacenar resultados en DataFrames
        dataframes = {}
        for nombre_pestana, query in consultas.items():
            print(f"🛠️ Ejecutando consulta para: {nombre_pestana}")
            cursor.execute(query, tuple(params))
            datos = cursor.fetchall()
            if datos:
                columnas = [desc[0] for desc in cursor.description]  # Obtener nombres de columnas
                df = pd.DataFrame(datos, columns=columnas)
                df = df.fillna("")  # Reemplazar valores None con ""
                dataframes[nombre_pestana] = df
            else:
                print(f"⚠️ No hay datos para {nombre_pestana}")

        # 🔹 Si no hay datos en ninguna tabla, evitar descargar un archivo vacío
        if not dataframes:
            flash("No hay datos disponibles para exportar en el rango de fechas seleccionado.", "warning")
            return redirect(url_for('infraestructura.lista_infraestructura'))

        # 🔹 Crear archivo Excel en memoria con múltiples pestañas
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for nombre_pestana, df in dataframes.items():
                df.to_excel(writer, index=False, sheet_name=nombre_pestana)

        output.seek(0)

        print("✅ Exportación completada correctamente.")

        # 🔹 Enviar archivo Excel como descarga
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="infraestructura_export.xlsx"
        )

    except Exception as e:
        flash(f'Error al exportar: {e}', 'danger')
        print(f"❌ Error en exportación: {e}")
        return redirect(url_for('infraestructura.lista_infraestructura'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            

from flask import request
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pymysql
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.graphics.barcode import code128
from reportlab.lib.units import inch

# Estilos para párrafos
styles = getSampleStyleSheet()
style_normal = styles['Normal']
style_heading = styles['Heading2']

@infraestructura_bp.route('/detalle_infraestructura/<int:id_infraestructura>', methods=['GET', 'POST'])
@login_required
@role_required('supervisor', 'administrador')
def detalle_infraestructura(id_infraestructura):
    # Conexión a la base de datos
    conexion = get_db_connection('visitas', driver="pymysql") 
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # Consulta para obtener la información de la infraestructura específica
        sql_infraestructura = """
            SELECT i.id_infraestructura, i.fecha, i.municipio, i.corregimiento, i.vereda, o.nombre AS nombre_operador, 
                   inst.sede_educativa AS institucion_nombre, s.nombre_sede AS sede_nombre, 
                   i.codigo_sede, i.direccion, i.barrio, i.comuna, i.zona, i.tipo_racion, 
                   i.focalizacion, i.observacion_general
            FROM infraestructura i
            JOIN instituciones inst ON i.institucion = inst.id_institucion
            JOIN operadores o ON i.operador = o.id_operador
            JOIN sedes s ON i.sede = s.id_sede
            WHERE i.id_infraestructura = %s
        """
        cursor.execute(sql_infraestructura, (id_infraestructura,))
        infraestructura = cursor.fetchone()

        # Consulta para obtener las respuestas relacionadas con esta infraestructura
        sql_respuestas = """
            SELECT p.numero, p.descripcion, r.respuesta, r.observacion, r.foto
            FROM respuestas_infraestructura r
            JOIN preguntas_infraestructura p ON r.id_pregunta = p.id_pregunta
            WHERE r.id_infraestructura = %s
            ORDER BY p.id_pregunta
        """
        cursor.execute(sql_respuestas, (id_infraestructura,))
        respuestas = cursor.fetchall()

        # Consulta para obtener el inventario de dotación de menaje
        sql_dotacion_menaje = """
            SELECT 
                dm.item, 
                dm.cantidad, 
                dm.estado, 
                dm.propiedad,
                dm.foto_menaje,
                COALESCE(pi.numero, '') AS numero
            FROM dotacion_menaje dm
            LEFT JOIN preguntas_infraestructura pi 
                ON dm.item = pi.descripcion
            WHERE dm.id_infraestructura = %s

        """
        cursor.execute(sql_dotacion_menaje, (id_infraestructura,))
        dotacion_menaje = cursor.fetchall()
        
        # **Consulta para obtener las firmas asociadas a la infraestructura**
        sql_firmas = """
            SELECT nombre_representante_ieo, nombre_profesional
            FROM firmas_infraestructura
            WHERE id_infraestructura = %s
        """
        cursor.execute(sql_firmas, (id_infraestructura,))
        firmas = cursor.fetchall()

    except Exception as e:
        print(f"Error al obtener detalles de infraestructura: {e}")
        infraestructura = None
        respuestas = []
        dotacion_menaje = []
        firmas = []
    finally:
        cursor.close()
        conexion.close()

    # Procesar solicitud GET
    if request.method == 'GET':
        return render_template(
            'detalle_infraestructura.html',
            infraestructura=infraestructura,
            respuestas=respuestas,
            dotacion_menaje=dotacion_menaje,
            firmas = firmas,
            rol=session.get('rol'),
            usuario=session.get('nombre')
        )

    # Procesar solicitud POST (generar PDF)
    elif request.method == 'POST':
        # Capturar datos del formulario
        nombre_representante_ieo = request.form.get('nombre_representante_ieo', 'No especificado')
        nombre_profesional = request.form.get('nombre_profesional', 'No especificado')
        accion = request.form.get('accion')
        
        print("📌 Valores recibidos del formulario:")
        print("   - Nombre representante IEO:", nombre_representante_ieo)
        print("   - Nombre profesional:", nombre_profesional)

        
        if accion == 'guardar':
            if nombre_representante_ieo and nombre_profesional:
                try:
                    conexion = get_db_connection('visitas', driver="pymysql")
                    if not conexion:
                        print("❌ Error: No se pudo conectar a la base de datos")
                        return jsonify({"error": "Error de conexión a la base de datos"}), 500
                    cursor = conexion.cursor()

                    print(f"🔍 id_infraestructura recibido: {id_infraestructura}")  # Depuración

                    # Verificar si ya existe una firma para esta infraestructura
                    sql_check_firma = """
                        SELECT COUNT(*) FROM firmas_infraestructura 
                        WHERE id_infraestructura = %s
                    """
                    cursor.execute(sql_check_firma, (id_infraestructura,))
                    resultado = cursor.fetchone()  # Puede devolver None o una tupla

                    firma_existe = resultado[0] if resultado and isinstance(resultado, (list, tuple)) else 0


                    if firma_existe == 0:  # Si no hay firma, la insertamos
                        sql_insert_firma = """
                            INSERT INTO firmas_infraestructura (id_infraestructura, nombre_representante_ieo, nombre_profesional)
                            VALUES (%s, %s, %s)
                        """
                        cursor.execute(sql_insert_firma, (id_infraestructura, nombre_representante_ieo, nombre_profesional))
                        conexion.commit()
                        print("✅ Firma guardada exitosamente.")
                    else:
                        print("⚠️ La firma ya existe, no se inserta nuevamente.")

                except Exception as e:
                    import traceback
                    print(f"❌ Error inesperado al guardar la firma: {e}")
                    print(traceback.format_exc())  # Muestra el error completo
                    return jsonify({"error": str(e)}), 500

                
                finally:
                    cursor.close()
                    conexion.close()

                return redirect(url_for('infraestructura.lista_infraestructura'))  # Redirección correcta


                    
        elif accion == 'pdf':
            if nombre_representante_ieo and nombre_profesional:
                try:
                    conexion = get_db_connection('visitas', driver="pymysql")
                    if not conexion:
                        print("❌ Error: No se pudo conectar a la base de datos")
                        return jsonify({"error": "Error de conexión a la base de datos"}), 500
                    cursor = conexion.cursor()

                    print(f"🔍 id_infraestructura recibido: {id_infraestructura}")  # Depuración

                    # Verificar si ya existe una firma para esta infraestructura
                    sql_check_firma = """
                        SELECT COUNT(*) FROM firmas_infraestructura 
                        WHERE id_infraestructura = %s
                    """
                    cursor.execute(sql_check_firma, (id_infraestructura,))
                    resultado = cursor.fetchone()  # Puede devolver None o una tupla

                    firma_existe = resultado[0] if resultado and isinstance(resultado, (list, tuple)) else 0


                    if firma_existe == 0:  # Si no hay firma, la insertamos
                        sql_insert_firma = """
                            INSERT INTO firmas_infraestructura (id_infraestructura, nombre_representante_ieo, nombre_profesional)
                            VALUES (%s, %s, %s)
                        """
                        cursor.execute(sql_insert_firma, (id_infraestructura, nombre_representante_ieo, nombre_profesional))
                        conexion.commit()
                        print("✅ Firma guardada exitosamente.")
                    else:
                        print("⚠️ La firma ya existe, no se inserta nuevamente.")

                except Exception as e:
                    import traceback
                    print(f"❌ Error inesperado al guardar la firma: {e}")
                    print(traceback.format_exc())  # Muestra el error completo
                    return jsonify({"error": str(e)}), 500

                
                finally:
                    cursor.close()
                    conexion.close()

            buffer = BytesIO()
            pdf = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Generar código de barras
            barcode_data = f"INF{infraestructura['id_infraestructura']}_{infraestructura['fecha'].strftime('%Y%m%d')}"
            barcode = code128.Code128(barcode_data, barWidth=0.015 * inch, barHeight=0.35 * inch)

            # Crear texto debajo del código de barras, centrado
            styles = getSampleStyleSheet()
            barcode_text = Paragraph(f"<para align='center'>{barcode_data}</para>", styles['Normal'])

            # Cargar la imagen de la Alcaldía de Cali
            logo_path = "static/images/cali.png" # Asegúrate de que la imagen está en la ruta correcta
            logo = Image(logo_path, width=1.2*inch, height=0.9*inch)

            # Crear una tabla con dos celdas: imagen (izquierda) y código de barras + texto (derecha)
            barcode_table = Table([
                [logo, barcode],  # Fila 1: Imagen a la izquierda, código de barras a la derecha
                ["", barcode_text]  # Fila 2: Texto del código de barras alineado a la derecha
            ], colWidths=[2*inch, 4*inch])

            # Aplicar estilos a la tabla para alinear correctamente
            barcode_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),     # Imagen alineada a la izquierda
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),    # Código de barras alineado a la derecha
                ('ALIGN', (1, 1), (1, 1), 'RIGHT'),    # Texto alineado a la derecha, debajo del código de barras
                ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'), # Todo alineado al fondo
                ('BOTTOMPADDING', (1, 1), (1, 1), 0),  # Sin espacio extra entre código y texto
            ]))

            # Agregar la tabla a los elementos del PDF
            elements.append(Spacer(1, 12))
            elements.append(barcode_table)


            # Título
            elements.append(Paragraph("Diagnóstico y Caracterización de Infraestructura y Dotación de Unidades de Servicio - Pae", styles['Title']))
            elements.append(Spacer(1, 12))

            # Información de infraestructura
            info_data = [
                ["ID Infraestructura", f"INF{infraestructura['id_infraestructura']}"],
                ["Fecha", infraestructura['fecha']],
                ["Municipio", infraestructura['municipio']],
                ["Corregimiento", infraestructura['corregimiento']],
                ["Vereda", infraestructura['vereda']],
                ["Operador", infraestructura['nombre_operador']],
                ["Institución", infraestructura['institucion_nombre']],
                ["Sede", infraestructura['sede_nombre']],
                ["Código Sede", infraestructura['codigo_sede']],
                ["Dirección", infraestructura['direccion']],
                ["Barrio", infraestructura['barrio']],
                ["Comuna", infraestructura['comuna']],
                ["Zona", infraestructura['zona']],
                ["Modalidad", infraestructura['tipo_racion']],
                ["Focalización", infraestructura['focalizacion']]
            ]

            info_data = [[Paragraph(str(cell), style_normal) for cell in row] for row in info_data]
            info_table = Table(info_data, colWidths=[150, 350])  # Ajusta los anchos de columnas
            info_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 12))
            

            

            # Respuestas
            elements.append(Paragraph("Aspectos a Evaluar", style_heading))
            respuestas_data = [["N°", "Aspecto", "Resultado", "Observación"]]
            for respuesta in respuestas:
                fila = [
                    respuesta['numero'],
                    Paragraph(respuesta['descripcion'], style_normal),
                    respuesta['respuesta'],
                    Paragraph(respuesta['observacion'], style_normal),
                ]
                respuestas_data.append(fila)

            respuestas_table = Table(respuestas_data, colWidths=[40, 200, 60, 200])  # Ajusta los anchos de columnas
            respuestas_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            elements.append(respuestas_table)
            elements.append(Spacer(1, 12))
            

            # Inventario de Dotación de Menaje
            if dotacion_menaje:
                elements.append(Paragraph("Inventario de Dotación de Menaje", styles['Heading2']))
                
                # Encabezados de la tabla
                dotacion_data = [
                    [
                        Paragraph("Item", style_normal),
                        Paragraph("Cantidad", style_normal),
                        Paragraph("Estado", style_normal),
                        Paragraph("Propiedad", style_normal)
                    ]
                ]
                
                # Filas de datos
                for item in dotacion_menaje:
                    fila = [
                        Paragraph(item['item'], style_normal),
                        Paragraph(item['cantidad'], style_normal),
                        Paragraph(item['estado'], style_normal),
                        Paragraph(item['propiedad'], style_normal)
                    ]
                    dotacion_data.append(fila)
                
                # Crear la tabla con anchos ajustables
                dotacion_table = Table(dotacion_data, colWidths=[200, 100, 110, 100])  # Ajusta los anchos según el contenido
                dotacion_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de las celdas
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Fondo para los encabezados
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente de las celdas
                    ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de la fuente
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alineación vertical en la parte superior
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación horizontal a la izquierda
                ]))
                
                # Agregar tabla al PDF
                elements.append(dotacion_table)
                elements.append(Spacer(1, 12))
            else:
                elements.append(Paragraph("No se encontraron datos para el inventario de dotación de menaje.", style_normal))
                elements.append(Spacer(1, 12))
                
            
            
            elements.append(Paragraph(f"Observación General: {infraestructura['observacion_general']}", style_normal))

            # Firmas
            elements.append(Paragraph("Firmas", style_heading))
            firmas_data = [
                ["Nombre Representante IEO", nombre_representante_ieo],
                ["Nombre Profesional", nombre_profesional],
            ]
            firmas_data = [[Paragraph(cell, style_normal) for cell in row] for row in firmas_data]
            firmas_table = Table(firmas_data, colWidths=[200, 300])  # Ajusta los anchos de columnas
            firmas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]))
            elements.append(firmas_table)

            # Generar PDF
            pdf.build(elements)
            buffer.seek(0)  # Mover el puntero al inicio del archivo

            return send_file(
                buffer,
                as_attachment=False,  # Mostrar en el navegador en lugar de descargar
                download_name=f"infraestructura_INF{id_infraestructura}.pdf",
                mimetype='application/pdf'
            )
     
        
        

from flask import  send_from_directory

@infraestructura_bp.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory('uploads', filename)




@infraestructura_bp.route('/editar_infraestructura/<int:id_infraestructura>')
def editar_infraestructura(id_infraestructura):
    conexion = get_db_connection('visitas', driver="pymysql") 
    with conexion.cursor() as cursor:
        # Obtener datos de la infraestructura
        cursor.execute("SELECT * FROM infraestructura WHERE id_infraestructura = %s", (id_infraestructura,))
        infraestructura = cursor.fetchone()

        # Obtener dotación de menaje
        cursor.execute("""SELECT dm.id, dm.item, dm.cantidad, dm.estado, dm.propiedad, dm.foto_menaje, pi.numero 
                       FROM dotacion_menaje dm
                       LEFT JOIN preguntas_infraestructura pi ON pi.descripcion = dm.item
                       WHERE id_infraestructura = %s""", (id_infraestructura,))
        dotacion_menaje = cursor.fetchall()

        # Obtener respuestas de infraestructura
        cursor.execute("""SELECT rf.id_respuesta, rf.descripcion, rf.respuesta, rf.observacion, inf.numero, rf.foto
                       FROM respuestas_infraestructura rf 
                       LEFT JOIN preguntas_infraestructura inf ON rf.descripcion = inf.descripcion
                       WHERE id_infraestructura = %s""", (id_infraestructura,))
        respuestas_infraestructura = cursor.fetchall()

        # Obtener operadores
        cursor.execute("SELECT id_operador, nombre FROM operadores")
        operadores = cursor.fetchall()

        # Obtener instituciones del operador actual
        cursor.execute("SELECT id_institucion, sede_educativa FROM instituciones WHERE id_operador = %s", 
                       (infraestructura['operador'],))
        instituciones = cursor.fetchall()

        # Obtener sedes de la institución actual
        cursor.execute("SELECT id_sede, nombre_sede FROM sedes WHERE id_institucion = %s", 
                       (infraestructura['institucion'],))
        sedes = cursor.fetchall()
        
        tipo_racion = obtener_tipo_racion()

    conexion.close()

    return render_template("editar_infraestructura.html", 
                           infraestructura=infraestructura,
                           dotacion_menaje=dotacion_menaje, 
                           respuestas_infraestructura=respuestas_infraestructura,
                           operadores=operadores,
                           instituciones=instituciones,
                           sedes=sedes,
                           tipo_racion = tipo_racion)


import pprint  # Importa este módulo para imprimir de forma legible

@infraestructura_bp.route('/actualizar_infraestructura', methods=['POST'])
@login_required
@role_required('supervisor', 'administrador')
def actualizar_infraestructura():
    # Muestra los datos recibidos
    # print("🟢 Datos recibidos:")
    # pprint.pprint(request.form)

    id_infraestructura = request.form.get('id_infraestructura')
    if not id_infraestructura:
        flash("Error: Falta el ID de infraestructura", "danger")
        return redirect(url_for('infraestructura.detalle_infraestructura', id_infraestructura=id_infraestructura))

    conexion = get_db_connection('visitas', driver="pymysql") 
    with conexion.cursor() as cursor:
        # 🏗️ Actualizar infraestructura
        
        tipo_racion_seleccionado = request.form.getlist('tipo_racion_checkbox')  # Obtiene todas las opciones marcadas
        tipo_racion_str = ", ".join(tipo_racion_seleccionado)  # Convierte la lista en un string separado por comas

# Luego, guárdalo en la base de datos

        cursor.execute("""
            UPDATE infraestructura 
            SET fecha=%s, municipio=%s, corregimiento=%s, vereda=%s, operador=%s, institucion=%s, 
                sede=%s, codigo_sede=%s, direccion=%s, barrio=%s, comuna=%s, zona=%s, tipo_racion=%s, 
                focalizacion=%s, observacion_general=%s 
            WHERE id_infraestructura=%s
        """, (
            request.form['fecha'], request.form['municipio'], request.form['corregimiento'], 
            request.form['vereda'], request.form['operador'], request.form['institucion'], 
            request.form['sede'], request.form['codigo_sede'], request.form['direccion'], 
            request.form['barrio'], request.form['comuna'], request.form['zona'], 
            tipo_racion_str, request.form['focalizacion'], request.form['observacion_general'], 
            id_infraestructura
        ))

        # 🍽️ Actualizar dotación de menaje
        for key in request.form:
            if key.startswith("item_"):
                menaje_id = key.split("_")[1]

                # Obtener valores del formulario
                item = request.form.get(f"item_{menaje_id}")
                cantidad = request.form.get(f"cantidad_{menaje_id}")

                # Obtener múltiples valores de checkboxes como lista
                estado = request.form.getlist(f"estado_{menaje_id}[]")  # Devuelve una lista con los valores seleccionados
                propiedad = request.form.getlist(f"propiedad_{menaje_id}[]")  # Devuelve una lista con los valores seleccionados

                # Convertir listas a string separados por comas para almacenar en la base de datos
                estado_str = ",".join(estado) 
                propiedad_str = ",".join(propiedad) 
                
                print(f"estado: {estado_str}")
                print(f"propiedad: {propiedad_str}")

                if item or cantidad or estado_str or propiedad_str:
                    print(f"🔹 Actualizando dotación de menaje ID {menaje_id}: {item}, {cantidad}, {estado_str}, {propiedad_str}")

                    cursor.execute("""
                        UPDATE dotacion_menaje 
                        SET item = %s, cantidad = %s, estado = %s, propiedad = %s 
                        WHERE id = %s AND id_infraestructura = %s
                    """, (item, cantidad, estado_str, propiedad_str, menaje_id, id_infraestructura))


        # 📝 Actualizar respuestas de infraestructura
        for key in request.form:
            if key.startswith("respuesta_"):
                respuesta_id = key.split("_")[1]
                respuesta = request.form.get(f"respuesta_{respuesta_id}")
                observacion = request.form.get(f"observacion_{respuesta_id}", "")

                if respuesta is not None:
                    # print(f"📝 Actualizando respuesta ID {respuesta_id}: {respuesta}, {observacion}")
                    cursor.execute("""
                        UPDATE respuestas_infraestructura 
                        SET respuesta = %s, observacion = %s 
                        WHERE id_respuesta = %s AND id_infraestructura = %s
                    """, (respuesta, observacion, respuesta_id, id_infraestructura))

    conexion.commit()
    conexion.close()

    flash("Infraestructura y datos actualizados correctamente", "success")
    return redirect(url_for('infraestructura.detalle_infraestructura', id_infraestructura=id_infraestructura))

