from infraestructura import infraestructura_bp
from bodega import bodega_bp
from tecnica import tecnica_bp
from menus import menus_bp
from actualizar import actualizar_bp
from verificacion_menu import verificacion_bp
from instituciones import instituciones_bp  
from sedes import sedes_bp
from iniciasesion import iniciasesion_bp, login_required, supervisor_required, operador_required, nutricionista_required, session, role_required
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory, abort, send_file, session, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
import os
from reportlab.lib.pagesizes import letter, landscape
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from PIL import Image
import locale
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.units import cm 
# from database import get_db_connection
from flask_cors import CORS
from database import get_db_connection



# Agregar cm para configurar los márgenes en centímetros

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


# logging.basicConfig(level=logging.DEBUG)

visitas_bp = Blueprint('visitas', __name__, template_folder='templates/app')

visitas = Flask(__name__)
visitas.secret_key = 'SECRET_KEY'  # Necesario para usar flash
visitas.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'solicitud_intercambio')
visitas.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

CORS(visitas)
# Configuración de la conexión a MySQL  


def fetch_instituciones():
    conn = get_db_connection('visitas')
    if conn is None:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_institucion, sede_educativa FROM Instituciones")
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()
        
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
        cursor.execute("SELECT id_operador, nombre FROM operadores")
        return cursor.fetchall()
    except Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

@visitas.route('/sedes/<int:id_institucion>', methods=['GET'])
def get_sedes_by_institucion(id_institucion):
    conn = get_db_connection('visitas')
    if conn is None:
        return jsonify([]), 500
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_sede, nombre_sede FROM Sedes WHERE id_institucion = %s", (id_institucion,))
        sedes = cursor.fetchall()
        return jsonify(sedes)
    except Error as err:
        print(f"Error: {err}")
        return jsonify([]), 500
    finally:
        cursor.close()
        conn.close()
 


def generar_numero_intercambio(tipo_racion, id_operador):
    conn = get_db_connection('visitas')
    cursor = conn.cursor()
    try:
        # Definir el prefijo según el tipo de ración
        prefijos = {1: 'RI', 2: 'AM', 3: 'PM', 4: 'JU'}
        if tipo_racion not in prefijos:
            raise ValueError('Tipo de ración no válido')

        prefix = prefijos[tipo_racion]

        # Obtener el número máximo de intercambio para el tipo de ración y operador
        cursor.execute(
            "SELECT MAX(numero_intercambio) FROM intercambios WHERE id_tipo_racion = %s AND id_operador = %s",
            (tipo_racion, id_operador)
        )
        max_numero = cursor.fetchone()[0]

        # Inicializar el número de intercambio
        if max_numero is None:
            nuevo_numero = 1
        else:
            try:
                # Extraer solo los dígitos después del prefijo hasta el separador ' - '
                numero_str = max_numero.split(' - ')[0][len(prefix):]  # Tomar todo después del prefijo
                nuevo_numero = int(numero_str) + 1
            except (ValueError, IndexError):
                print(f"Error al convertir max_numero: {max_numero}")
                nuevo_numero = 1  # Resetea a 1 si hay un error

        cursor.execute(
            "SELECT numero_contrato FROM operadores WHERE id_operador = %s",
            (id_operador,)
        )
        result = cursor.fetchone()
        numero_contrato = result[0] if result else "Sin Contrato" 
        

        # Verificar si el nuevo número ya existe, en caso afirmativo, seguir incrementando
        while True:
            numero_intercambio = f"{prefix}{nuevo_numero} - {numero_contrato}"
            cursor.execute(
                "SELECT COUNT(*) FROM intercambios WHERE numero_intercambio = %s AND id_operador = %s",
                (numero_intercambio, id_operador)
            )
            if cursor.fetchone()[0] == 0:
                break  # Si no existe el número, salir del bucle
            nuevo_numero += 1  # Aumentar el número si ya existe

        return numero_intercambio

    except Exception as e:
        print(f"Error en generar_numero_intercambio: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Ruta para obtener el número de intercambio desde la API
@visitas_bp.route('/get_numero_intercambio')
def get_numero_intercambio():
    tipo_racion = request.args.get('tipo_racion')
    id_operador = request.args.get('id_operador')

    # Verificar que los parámetros existen
    if not tipo_racion or not id_operador:
        return jsonify({'error': 'Faltan parámetros requeridos.'}), 400

    try:
        # Convertir parámetros a enteros
        tipo_racion = int(tipo_racion)
        id_operador = int(id_operador)

        # Validar tipo de ración
        if tipo_racion not in [1, 2, 3, 4]:
            raise ValueError('Tipo de ración no válido')

        # Generar el nuevo número de intercambio
        nuevo_numero_intercambio = generar_numero_intercambio(tipo_racion, id_operador)
        return jsonify({'numero_intercambio': nuevo_numero_intercambio})

    except ValueError as ve:
        print(f"Error en generar_numero_intercambio: {ve}")
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Ocurrió un error en el servidor.'}), 500

from werkzeug.utils import secure_filename
from flask import jsonify, request, send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import mysql.connector
from mysql.connector import Error

def crear_pdf_intercambio(datos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']

    elements.append(Paragraph("Solicitud de Intercambio", title_style))
    elements.append(Spacer(1, 12))

    info_general = [
        ["Número de Intercambio:", datos['numero_intercambio']],
        ["Operador:", datos['operador']],
        ["Fecha de Solicitud:", datos['fecha_solicitud']],
        ["Tipo de Ración:", datos['tipo_racion']],
        ["Justificación:", datos['justificacion']],
    ]
    t = Table(info_general, colWidths=[2*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Detalles del Menú", styles['Heading2']))
    elements.append(Spacer(1, 6))
    
    menu_data = [["Componentes", "Menú Oficial", "Menú Intercambio"]]
    for detalle in datos['detalles_menu']:
        menu_data.append([
            detalle['componente'],
            detalle['menu_oficial'],
            detalle['menu_intercambio']
        ])
    
    t = Table(menu_data, colWidths=[2*inch, 2*inch, 2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


@visitas.route('/instituciones/<int:id_operador>', methods=['GET'])
def fetch_instituciones_por_operador(id_operador):
    print(f"ID Operador recibido: {id_operador}")  # Depuración
    conn = get_db_connection('visitas')
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT id_institucion, sede_educativa 
    FROM instituciones 
    WHERE id_operador = %s
    """
    cursor.execute(query, (id_operador,))
    instituciones = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"Instituciones obtenidas: {instituciones}")  # Depuración

    return jsonify(instituciones)  # Devuelve una respuesta JSON


def get_instituciones_por_operador(id_operador):
    """ Función auxiliar para obtener instituciones sin usar jsonify """
    conn = get_db_connection('visitas')
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT id_institucion, sede_educativa 
    FROM instituciones 
    WHERE id_operador = %s
    """
    cursor.execute(query, (id_operador,))
    instituciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return instituciones


@visitas_bp.route('/intercambio_operador.html', methods=['GET', 'POST'])
@login_required
@role_required('operador', 'administrador', 'nutricionista')
def intercambio_operador():
    rol_usuario = session.get('rol')
    print(f"Rol del usuario: {rol_usuario}")  # Depuración

    if request.method == 'POST':
        id_operador = request.form.get('id_operador')
    else:
        id_operador = request.args.get('id_operador') or session.get('id_operador')
    print(f"ID Operador obtenido: {id_operador}")  # Depuración

    # Verificar rol y obtener instituciones
    if rol_usuario in ['administrador', 'nutricionista']:
        instituciones = get_instituciones_por_operador(id_operador) if id_operador else fetch_instituciones()
    elif rol_usuario == 'operador':
        if not id_operador:
            flash("No se pudo obtener el ID del operador.", "error")
            return redirect('/')
        instituciones = get_instituciones_por_operador(id_operador)
    else:
        flash("No tienes permisos para acceder a esta página.", "error")
        return redirect('/')

    # Otras funciones
    tiporacion = fetch_tiporacion()
    operadores = fetch_operador()
    today_date = datetime.today().strftime('%Y-%m-%d')

    print(f"Instituciones a renderizar: {instituciones}")  # Depuración
    return render_template(
        'intercambio_operador.html',
        instituciones=instituciones,  # Ahora es una lista válida
        tiporacion=tiporacion,
        operadores=operadores,
        today_date=today_date,
        rol=rol_usuario,
        usuario=session.get('nombre'),
        id_operador_seleccionado=id_operador
    )

   
@visitas_bp.route('/save_intercambio', methods=['POST'])
def save_intercambio():
    conn = get_db_connection('visitas')
    if conn is None:
        print("❌ Error: No se pudo conectar a la base de datos.")
        return jsonify({'error': 'Error en la conexión a la base de datos.'}), 500

    cursor = conn.cursor()  # Solo se ejecutará si la conexión es válida.

    try:
        # Recoger datos del formulario
        rol = session.get('rol')
        
        correo = request.form.getlist('correo', None)

        correo_operador = session.get('correo')
        # print(f'Correo de Operador: {correo_operador}')

        
        # Validar y convertir id_operador
        id_operador = request.form.get('id_operador')
        fecha_solicitud = request.form.get('fecha_solicitud')
        id_operador = int(id_operador) if id_operador and id_operador.isdigit() else None
        
        # Recoger y validar id_tipo_racion
        id_tipo_racion_list = request.form.getlist('tipo_racion')
        id_tipo_racion = int(id_tipo_racion_list[0]) if id_tipo_racion_list and id_tipo_racion_list[0].isdigit() else None
        
        justificacion_texto = request.form.get('justificacion_texto', '')
        
        justificacion = request.form.get('justificacion', '').strip()
        otros_justificacion = request.form.get('otros_justificacion', '').strip()

        # Validar y asignar la justificación final
        if justificacion == "Otros":
            if not otros_justificacion:
                return jsonify({'error': 'Debe proporcionar un texto para justificar si selecciona "Otros".'}), 400
            justificacion_final = otros_justificacion
        else:
            justificacion_final = justificacion

        # Ahora `justificacion_final` contiene el texto final a usar o guardar
        print(f"Justificación Final: {justificacion_final}")

        
        # Validar y convertir fecha_ejecucion
        fecha_ejecucion = request.form.getlist('fecha_ejecucion[]')
        if not fecha_ejecucion:
            return jsonify({'error': 'No se proporcionó ninguna fecha de ejecución.'}), 400

        conn = get_db_connection('visitas')
        if conn is None:
            return jsonify({'error': 'Error en la conexión a la base de datos.'}), 500

        cursor = conn.cursor()

        # Generar el número de intercambio
        # Obtener ID del operador desde la solicitud (puede venir en GET o POST)
        id_operador = request.form.get('id_operador') or request.args.get('id_operador')



        # Generar número de intercambio con ambos parámetros
        numero_intercambio_unica = generar_numero_intercambio(id_tipo_racion, int(id_operador))

        # print(f"Número de intercambio generado: {numero_intercambio_unica}")

        # Verificar si el número de intercambio ya existe
        cursor.execute("SELECT * FROM intercambios WHERE numero_intercambio = %s AND id_operador = %s", (numero_intercambio_unica, id_operador))
        if cursor.fetchone() is not None:
            return jsonify({'error': 'El número de intercambio ya existe.'}), 400

        # Insertar en la tabla intercambios
        cursor.execute("""INSERT INTO intercambios (correo, fecha_solicitud, id_operador, numero_intercambio, id_tipo_racion, justificacion, justificacion_texto, correo_operador)
                          VALUES (%s, CURRENT_DATE, %s, %s, %s, %s, %s, %s)""",
                       (", ".join(correo), id_operador, numero_intercambio_unica, id_tipo_racion, justificacion_final, justificacion_texto, correo_operador))

        intercambio_id = cursor.lastrowid
        print(f"ID del intercambio guardado: {intercambio_id}")


        # Guardar instituciones y sedes
        institucion_ids = request.form.getlist('instituciones')

        
        instituciones_sedes = {}

        for institucion_id in institucion_ids:
            sedes_seleccionadas = request.form.getlist(f'sedes_{institucion_id}[]')
            print(f"Institución: {institucion_id}, Sedes: {sedes_seleccionadas}")

            if not sedes_seleccionadas:
                print(f"No se seleccionaron sedes para la institución {institucion_id}")
                continue
            
            instituciones_sedes[institucion_id] = sedes_seleccionadas
            
            print(f'Instituciones y sedes Almacenados: {instituciones_sedes}')
            
            for sede_id in sedes_seleccionadas:
                for fecha in fecha_ejecucion:  # Iterar sobre cada fecha de ejecución
                    cursor.execute("""INSERT INTO instituciones_sedes (id_institucion, id_sede, fecha_ejecucion, id_intercambio)
                                      VALUES (%s, %s, %s, %s)""",
                                   (institucion_id, sede_id, fecha, intercambio_id))
        
        # Manejo de componentes e ingredientes
        numero_menu_oficial = request.form.getlist('numero_menu_oficial[]')
        numero_menu_intercambio = request.form.getlist('numero_menu_intercambio[]')

        # Obtener listas de componentes e ingredientes
        componentes = request.form.getlist('componentes[]')
        ingredientes_oficial = request.form.getlist('ingredientes[]')
        ingredientes_intercambio = request.form.getlist('ingredientes_intercambio[]')

        # Limpiar saltos de línea en los ingredientes
        ingredientes_oficial = [ingr.strip() for ingr in ingredientes_oficial]
        ingredientes_intercambio = [ingr.strip() for ingr in ingredientes_intercambio]

        # Imprimir información para depuración
        print(f"Tipo ración: {id_tipo_racion}")
        print(f"Número Oficial: {numero_menu_oficial}")
        print(f"Número Intercambio: {numero_menu_intercambio}")
        print(f"Componentes: {componentes}")
        print(f"Ingredientes Oficial: {ingredientes_oficial}")
        print(f"Ingredientes Intercambio: {ingredientes_intercambio}")
        print(f"Fechas de Ejecución: {fecha_ejecucion}")

        # Validar longitudes
        # if not (len(numero_menu_oficial) == len(numero_menu_intercambio) == len(fecha_ejecucion)):
        #     return jsonify({'error': 'Las listas de menús oficiales, de intercambio y fechas de ejecución no tienen la misma longitud.'}), 400

        # Función para obtener el menú
        def obtener_menu(cursor, id_tipo_racion, numero_menu):
            query = """SELECT componentes, ingredientes FROM (
                        SELECT componentes, ingredientes FROM industrializado WHERE id_tipo_racion = %s AND numero_menu = %s
                        UNION ALL
                        SELECT componentes, ingredientes FROM preparadoensitioam WHERE id_tipo_racion = %s AND numero_menu = %s
                        UNION ALL
                        SELECT componentes, ingredientes FROM preparadoensitiopm WHERE id_tipo_racion = %s AND numero_menu = %s
                        UNION ALL
                        SELECT componentes, ingredientes FROM jornadaunica WHERE id_tipo_racion = %s AND numero_menu = %s) AS detalles_menu"""
            cursor.execute(query, (id_tipo_racion, numero_menu, id_tipo_racion, numero_menu, id_tipo_racion, numero_menu, id_tipo_racion, numero_menu))
            return cursor.fetchall()
        

        # Iterar sobre los menús y fechas
        for idx, (numero_oficial, numero_intercambio, fecha_ejecucion_val) in enumerate(zip(numero_menu_oficial, numero_menu_intercambio, fecha_ejecucion)):
            # print(f"Procesando Número Oficial: {numero_oficial}, Número Intercambio: {numero_intercambio}, Fecha de Ejecución: {fecha_ejecucion_val}")

            # Obtener los ingredientes correspondientes a este menú
            inicio = idx * len(componentes) // len(numero_menu_oficial)
            fin = (idx + 1) * len(componentes) // len(numero_menu_oficial)
            componentes_menu = componentes[inicio:fin]
            ingredientes_oficial_menu = ingredientes_oficial[inicio:fin]
            ingredientes_intercambio_menu = ingredientes_intercambio[inicio:fin]

            # Obtención de los menús oficial e intercambio desde la base de datos
            menu_oficial = obtener_menu(cursor, id_tipo_racion, numero_oficial)
            menu_intercambio = obtener_menu(cursor, id_tipo_racion, numero_intercambio)

            # print(f"Menú Oficial: {menu_oficial}")
            # print(f"Menú Intercambio: {menu_intercambio}")

            # if not menu_oficial or not menu_intercambio:
            #     return jsonify({'error': 'No se encontraron datos para los menús proporcionados.'}), 400

            ingredientes_oficial_bd = [row[1].strip().replace('\r', '').replace('\n', '') for row in menu_oficial]
            ingredientes_intercambio_bd = [row[1].strip().replace('\r', '').replace('\n', '') for row in menu_intercambio]

            print(f"Ingredientes Oficial BD: {ingredientes_oficial_bd}")
            print(f"Ingredientes Intercambio BD: {ingredientes_intercambio_bd}")
            
            
            # Guardar detalle de 'Todo el Menú' o componente por componente
            # print("Guardando detalle de Menu'")
            componentes_menu_str = ', '.join(componentes_menu)
            ingredientes_oficial_menu_str = ', '.join(ingredientes_oficial_menu)
            ingredientes_intercambio_menu_str = ', '.join(ingredientes_intercambio_menu)
            query_todo_menu = """INSERT INTO detalles_menu 
                                (id_intercambio, componente, menu_oficial, menu_intercambio, id_tipo_racion, numero_menu_oficial, numero_menu_intercambio, fecha_ejecucion)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query_todo_menu, (
                intercambio_id, componentes_menu_str, ingredientes_oficial_menu_str, ingredientes_intercambio_menu_str,
                id_tipo_racion, str(numero_oficial), str(numero_intercambio), fecha_ejecucion_val))

        # Obtener los datos del formulario
        nombres_operadores = request.form.getlist('nombre_operadores[]')
        tarjetas_profesionales = request.form.getlist('trajeta_profesional[]')
        cargos = request.form.getlist('cargo[]')

        # Comprobar que todas las listas tengan la misma longitud
        # if not (len(nombres_operadores) == len(tarjetas_profesionales) == len(cargos)):
        #     return jsonify({'error': 'Las listas de operadores, tarjetas profesionales y cargos deben tener la misma longitud.'}), 400

        firma_fotos = request.files.getlist('firma_foto[]')

        soporte_folder_path = os.path.join(visitas.config['UPLOAD_FOLDER'], "soporte")
        os.makedirs(soporte_folder_path, exist_ok=True)

        # Crear una subcarpeta para almacenar archivos específicos de este intercambio
        folder_path = os.path.join(soporte_folder_path, str(numero_intercambio_unica))
        os.makedirs(folder_path, exist_ok=True)

        cursor = conn.cursor()

        pdf_adjuntos = request.files.getlist('pdf_adjunto[]')
        print("PDF:", pdf_adjuntos)

        for pdf in pdf_adjuntos:
            if pdf and pdf.filename.lower().endswith('.pdf'):
                filename = secure_filename(pdf.filename)  # Asegurar nombre seguro del archivo
                file_path = os.path.join(folder_path, filename)  # Ruta dentro de "soporte"
                pdf.save(file_path)  # Guardar el archivo

                # Guardar referencia del archivo en la base de datos
                cursor.execute("""
                    INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                    VALUES (%s, %s, %s, %s)
                """, (intercambio_id, filename, 'soporte', file_path))
                
                print(f"Archivo PDF guardado en 'soporte': {filename}")
            else:
                print(f"Archivo inválido o no es un PDF: {pdf.filename}")

        firma_fotos = request.files.getlist('firma_foto[]')

        for i in range(len(nombres_operadores)):
            nombre_operador = nombres_operadores[i]
            tarjeta_profesional = tarjetas_profesionales[i]
            cargo = cargos[i]

            if i < len(firma_fotos):
                firma_foto = firma_fotos[i]
                if firma_foto and firma_foto.filename:
                    filename = secure_filename(firma_foto.filename)
                    file_path = os.path.join(folder_path, filename).replace('\\', '/')
                    try:
                        firma_foto.save(file_path)

                        # Guardar la ruta del archivo en la base de datos
                        cursor.execute(""" 
                            INSERT INTO firmas (id_intercambio, nombre_operador, tarjeta_profesional, cargo, tipo_firma, firma_foto_ruta, firma_manual_base64)
                            VALUES (%s, %s, %s, %s, %s, %s, NULL)
                        """, (intercambio_id, nombre_operador, tarjeta_profesional, cargo, 'foto', file_path))
                    except Exception as e:
                        return jsonify({'error': f'Error al guardar firma foto para {nombre_operador}: {e}'}), 500
                else:
                    return jsonify({'error': f'Archivo de firma inválido para {nombre_operador}'}), 400
            else:
                return jsonify({'error': f'No se recibió firma foto para {nombre_operador}'}), 400

        datos_por_fecha = {}

        # Llenado de datos en datos_por_fecha
        for idx, fecha in enumerate(fecha_ejecucion):
            fecha_str = str(fecha)

            # Inicializar la lista para la fecha si no existe
            if fecha_str not in datos_por_fecha:
                datos_por_fecha[fecha_str] = []

            # Crear un nuevo registro basado en los datos del formulario
            registro = {
                'numero_menu_oficial': numero_menu_oficial[idx].zfill(2),  # Asegura dos caracteres
                'numero_menu_intercambio': numero_menu_intercambio[idx].zfill(2),  # Asegura dos caracteres
                'componentes': componentes[idx * len(componentes) // len(fecha_ejecucion): (idx + 1) * len(componentes) // len(fecha_ejecucion)],  # Componentes específicos
                'ingredientes_oficial': ingredientes_oficial[idx * len(ingredientes_oficial) // len(fecha_ejecucion): (idx + 1) * len(ingredientes_oficial) // len(fecha_ejecucion)],  # Ingredientes oficiales específicos
                'ingredientes_intercambio': ingredientes_intercambio[idx * len(ingredientes_intercambio) // len(fecha_ejecucion): (idx + 1) * len(ingredientes_intercambio) // len(fecha_ejecucion)]  # Ingredientes de intercambio específicos
            }

            # Verificar si ya existe un registro con la misma combinación de menú oficial e intercambio para esa fecha
            encontrado = False
            for reg in datos_por_fecha[fecha_str]:
                if (reg['numero_menu_oficial'] == registro['numero_menu_oficial'] and
                    reg['numero_menu_intercambio'] == registro['numero_menu_intercambio']):
                    # Si ya existe, agrega solo los componentes y ingredientes únicos al registro existente
                    for componente, oficial, intercambio in zip(registro['componentes'], registro['ingredientes_oficial'], registro['ingredientes_intercambio']):
                        if componente not in reg['componentes']:
                            reg['componentes'].append(componente)
                        if oficial not in reg['ingredientes_oficial']:
                            reg['ingredientes_oficial'].append(oficial)
                        if intercambio not in reg['ingredientes_intercambio']:
                            reg['ingredientes_intercambio'].append(intercambio)
                    encontrado = True
                    break

            # Si no se encontró, agregar el nuevo registro
            if not encontrado:
                datos_por_fecha[fecha_str].append(registro)

        # Procesar datos_por_fecha solo si contiene datos
        if datos_por_fecha:
            print("Estructura final de datos_por_fecha:")
            for fecha, registros in datos_por_fecha.items():
                print(f"Fecha: {fecha}")
                for registro in registros:
                    print(f"Números de menú oficial: {registro['numero_menu_oficial']}")
                    print(f"Números de menú de intercambio: {registro['numero_menu_intercambio']}")
                    print(f"Componentes: {registro['componentes']}")
                    print(f"Ingredientes oficiales: {registro['ingredientes_oficial']}")
                    print(f"Ingredientes de intercambio: {registro['ingredientes_intercambio']}")
                    print()
        else:
            print("datos_por_fecha está vacío. No se encontraron datos para procesar.")


        firma_foto = request.files.getlist('firma_foto[]')

        # Verifica que haya al menos una firma foto
        # if not firma_foto or all(f.filename == '' for f in firma_foto):
        #     return jsonify({'error': 'No se recibió firma foto.'}), 400

        # Obtener las firmas de la base de datos
        cursor.execute("""
            SELECT nombre_operador, tarjeta_profesional, cargo, tipo_firma, firma_foto_ruta
            FROM firmas
            WHERE id_intercambio = %s
        """, (intercambio_id,))
        firmas = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        firmas_lista = []
        for firma in firmas:
            firmas_lista.append({
                'nombre_operador': firma[0],
                'tarjeta_profesional': firma[1],
                'cargo': firma[2],
                'tipo_firma': firma[3],
                'firma_manual_base64': None,  # Siempre NULL
                'firma_foto_ruta': firma[4] if firma[3] == 'foto' else None
            })


        
        # Crear el PDF y obtener la ruta de salida
        pdf_output_path = crear_pdf(
            intercambio_id,
            id_operador,
            id_tipo_racion,
            justificacion_texto,
            datos_por_fecha,
            numero_intercambio_unica,
            correo,
            instituciones_sedes,
            firmas_lista,
            fecha_solicitud
        )

        cursor.execute("""
                    INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                    VALUES (%s, %s, %s, %s)
                """, (intercambio_id, f"{numero_intercambio_unica}.pdf", 'pdf', pdf_output_path))
        print("PDF guardado en la base de datos.")
        
        conn.commit()

        return jsonify({"message": "Guardado con éxito", "rol": rol}), 200

    except Exception as e:
        print(f"Error al guardar el intercambio: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
        return jsonify({'error': 'Se produjo un error al guardar el intercambio'}), 500
    finally:
        if conn:
            conn.close()

#PDF

from PIL import Image
import os
from barcode import Code128
from barcode.writer import ImageWriter
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.ln(20)
        self.set_font('Arial', 'B', 12)
        self.ln(1)

    def footer(self):
        # Posiciona el cursor a 15 mm del borde inferior
        self.set_y(-15)
        # Establece la fuente: Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Calcula el ancho del texto del número de página
        page_number = f'Página {self.page_no()}'
        page_width = self.get_string_width(page_number) + 6  # Añade un pequeño margen
        
        # Posiciona el número de página a la derecha
        self.set_x(self.w - page_width - 10)  # 10 mm desde el borde derecho
        
        # Añade el número de página
        self.cell(page_width, 10, page_number, 0, 0, 'R')


        
import base64


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os
from barcode import Code128
from barcode.writer import ImageWriter
from datetime import datetime


def crear_pdf(intercambio_id, id_operador, id_tipo_racion, justificacion_texto, 
              datos_por_fecha, numero_intercambio_unica, correo, instituciones_sedes, firmas_lista, fecha_solicitud):        

    pdf_folder_path = os.path.join('static', 'uploads', 'solicitud_intercambio', 'pdfs', str(numero_intercambio_unica))
    os.makedirs(pdf_folder_path, exist_ok=True)
    
    pdf_path = os.path.join(pdf_folder_path, f"{numero_intercambio_unica}.pdf")
    
    numeros_menu_intercambio = sorted({
        registro['numero_menu_intercambio']
        for registros in datos_por_fecha.values()
        for registro in registros
    })

    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        leftMargin=85, rightMargin=85, topMargin=85, bottomMargin=85)

    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]

    # 📌 Generar código de barras
    barcode_text = f"{fecha_solicitud} - {numero_intercambio_unica}"
    barcode_path = os.path.join(pdf_folder_path, f"{barcode_text}.png")
    code128 = Code128(barcode_text, writer=ImageWriter())
    code128.save(barcode_path[:-4])  

    # 📌 Encabezado# 📌 Encabezado con imagen desplazada a la izquierda y menos espacio arriba
    
    header_table = Table([
        [
            Image('static/images/cali.png', width=70, height=50),  # Logo alineado a la izquierda
            "",  # Espacio vacío en el centro
            Image(barcode_path, width=150, height=50)  # Código de barras alineado a la derecha
        ]
    ], colWidths=[100, 300, 150])  # Ajuste de espacios entre elementos

    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Alinear logo a la izquierda
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Alinear código de barras a la derecha
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5)  # Reducir espacio inferior
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 5))  # Espacio pequeño después de la tabla

    # 📌 Título centrado debajo del encabezado
    elements.append(Paragraph("ANEXO 17.1", title_style))
    elements.append(Paragraph("SOLICITUD DE INTERCAMBIOS", title_style))
    elements.append(Spacer(1, 10))  # Espacio después del título

    conn = get_db_connection('visitas')
    if conn is None:
        print("Error: No se pudo establecer conexión a la base de datos")
    else:
        cursor = conn.cursor()

        try:
            # 🔹 Obtener nombre del operador
            cursor.execute("SELECT nombre FROM operadores WHERE id_operador = %s", (id_operador,))
            nombre_operador = cursor.fetchone()
            nombre_operador_str = nombre_operador[0] if nombre_operador else 'No encontrado'

            # 🔹 Obtener descripción de la ración
            cursor.execute("SELECT descripcion FROM tiporacion WHERE id_tipo_racion = %s", (id_tipo_racion,))
            nombre_racion = cursor.fetchone()
            nombre_racion_str = nombre_racion[0] if nombre_racion else 'No encontrado'

            # 🔹 Obtener nombres de instituciones y sedes
            nombres_instituciones = []
            nombres_sedes = []
            
            for institucion_id, sedes in instituciones_sedes.items():
                cursor.execute("SELECT sede_educativa FROM instituciones WHERE id_institucion = %s", (institucion_id,))
                nombre_institucion = cursor.fetchone()
                if nombre_institucion:
                    nombres_instituciones.append(nombre_institucion[0])

                for sede_id in sedes:
                    cursor.execute("SELECT nombre_sede FROM sedes WHERE id_sede = %s", (sede_id,))
                    nombre_sede = cursor.fetchone()
                    if nombre_sede:
                        nombres_sedes.append(nombre_sede[0])
                        
            # 🛠 Estilos para ReportLab
            styles = getSampleStyleSheet()
            normal_style = styles["Normal"]
            bold_style = styles["Heading4"]

            # 📌 Formatear fecha
            fecha_solicitud_formateada = datetime.strptime(fecha_solicitud, "%Y-%m-%d").strftime("%d - %B - %Y").capitalize()

            # 📌 Datos generales en tabla
            datos_generales = [
                [Paragraph("<b>DATOS</b>", bold_style), ""],  # Encabezado de la tabla
                [Paragraph("<b>Fecha de Solicitud:</b> " + fecha_solicitud_formateada, normal_style),
                Paragraph("<b>Número Intercambio:</b> " + numero_intercambio_unica, normal_style)],
                [Paragraph("<b>Modalidad:</b> " + nombre_racion_str, normal_style),
                Paragraph("<b>Menú Entregado:</b> " + ', '.join(numeros_menu_intercambio), normal_style)],
                [Paragraph("<b>Operador:</b> " + nombre_operador_str, normal_style), ""],  # Fila única
                [Paragraph("<b>Instituciones:</b> " + ', '.join(nombres_instituciones), normal_style), ""],  # Fila única
                [Paragraph("<b>Sedes:</b> " + ', '.join(nombres_sedes), normal_style), ""],  # Fila única
                [Paragraph("<b>Justificación:</b> " + justificacion_texto, normal_style), ""],  # Fila única
            ]

            # 🔹 **Crear la tabla con el formato correcto**
            tabla_datos = Table(datos_generales, colWidths=[220, 220])  # Ajustar ancho de columnas
            tabla_datos.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes en todas las celdas
                ('SPAN', (0, 0), (1, 0)),  # Unir celdas del título
                ('SPAN', (0, 3), (1, 3)),  # Unir fila "Operador"
                ('SPAN', (0, 4), (1, 4)),  # Unir fila "Instituciones"
                ('SPAN', (0, 5), (1, 5)),  # Unir fila "Sedes"
                ('SPAN', (0, 6), (1, 6)),  # Unir fila "Justificación"
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fondo gris en el título
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))


            # 📌 Agregar a elementos del PDF
            elements.append(tabla_datos)
            elements.append(Spacer(1, 10))  # Espaciado entre tablas
        
        
            # 📌 Tablas de datos
            for fecha, registros in datos_por_fecha.items():
                fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d - %B - %Y").capitalize()
                elements.append(Paragraph(f"Fecha de Ejecución: {fecha_formateada}", normal_style))
                elements.append(Spacer(1, 5))

                for datos in registros:
                    table_data = [[
                        Paragraph("<b>Componentes</b>", normal_style), 
                        Paragraph(f"<b>Menú Oficial: {datos['numero_menu_oficial']}</b>", normal_style),
                        Paragraph(f"<b>Menú Entregado: {datos['numero_menu_intercambio']}</b>", normal_style)
                    ]]

                    for i in range(len(datos['componentes'])):
                        row = [
                            Paragraph(datos['componentes'][i] if i < len(datos['componentes']) else "N/A", normal_style),
                            Paragraph(datos['ingredientes_oficial'][i] if i < len(datos['ingredientes_oficial']) else "N/A", normal_style),
                            Paragraph(datos['ingredientes_intercambio'][i] if i < len(datos['ingredientes_intercambio']) else "N/A", normal_style)
                        ]
                        table_data.append(row)

                    table = Table(table_data, colWidths=[146, 146, 146])  # Ajuste de ancho
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 10))
            
            styles = getSampleStyleSheet()
            style_normal = styles["Normal"]
            style_bold = styles["BodyText"]
            style_bold.fontName = "Helvetica-Bold"

            # 🔹 Sección de Notas
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("<b>Notas:</b>", style_bold))
            elements.append(Paragraph(
                "- Tanto el gramaje de las preparaciones y/o alimentos, como las frecuencias de entrega estos debe estar de acuerdo a la minuta patrón de la Resolución 335 del 2021 y guías de preparación aprobadas por la ETC en las modalidades que aplica.",
                style_normal
            ))
            elements.append(Paragraph(
                "- Toda Solicitud debe ser allegada con sus respectivos soportes (fotografías, certificaciones), cumplir con el protocolo de intercambios establecido por la ETC (Anexo 25) y con las listas de intercambios diseñadas por la ETC (Anexos 9, 10, 11).",
                style_normal
            ))
            elements.append(Spacer(1, 10))

            # 🔹 Sección de Firmas
            firma_data = []
            column_width = 220  # Ancho de columna
            row_height = 70  # Altura estimada de cada fila (firma + texto)

            for idx, firma in enumerate(firmas_lista):
                nombre_operador = firma['nombre_operador']
                tarjeta_profesional = firma.get('tarjeta_profesional', "")
                cargo = firma.get('cargo', "")
                firma_path = firma.get('firma_foto_ruta', None)

                firma_content = []

                # Si hay imagen de la firma, agregarla
                if firma_path:
                    firma_img = Image(firma_path, width=100, height=50)
                    firma_content.append(firma_img)
                else:
                    firma_content.append(Paragraph("<b>Firma no disponible</b>", style_normal))

                # Texto de la firma
                firma_content.append(Paragraph(f"<b>Nombre:</b> {nombre_operador}", style_normal))
                if tarjeta_profesional:
                    firma_content.append(Paragraph(f"<b>Tarjeta Profesional:</b> {tarjeta_profesional}", style_normal))
                if cargo:
                    firma_content.append(Paragraph(f"<b>Cargo:</b> {cargo}", style_normal))

                firma_data.append(firma_content)

            # Convertir datos de firmas en tabla (2 columnas)
            firma_table = Table([firma_data[i:i + 2] for i in range(0, len(firma_data), 2)],
                                colWidths=[column_width, column_width])

            firma_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                
            ]))

            elements.append(firma_table)
                
        except mysql.connector.Error as e:
            print(f"Error al obtener datos: {e}")


        # 📌 Generar PDF
        doc.build(elements)

        print(f"✅ PDF generado: {pdf_path}")
        return pdf_path


#ESTADO


@visitas_bp.route('/estado', methods=['GET'])
@login_required
@role_required('nutricionista', 'administrador')
def estado():
    search_numero = request.args.get('numero', '').strip()
    search_estado = request.args.get('estado', '').strip()
    search_fecha = request.args.get('fecha_solicitud', '').strip()
    
    conn = get_db_connection('visitas')
    cursor = conn.cursor(dictionary=True)

    # Consulta para obtener conceptos únicos
    cursor.execute("SELECT DISTINCT concepto FROM intercambios WHERE concepto IS NOT NULL")
    conceptos = [row['concepto'] for row in cursor.fetchall()]

    # Consulta principal con archivos PDF
    query = """
        SELECT 
            intercambios.numero_intercambio, 
            operadores.nombre AS nombre_operador, 
            tiporacion.descripcion AS descripcion_tipo_racion, 
            intercambios.concepto,
            intercambios.fecha_solicitud,
            GROUP_CONCAT(DISTINCT archivos.nombre_archivo) AS archivos_pdf
        FROM intercambios
        JOIN operadores ON intercambios.id_operador = operadores.id_operador
        JOIN tiporacion ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
        LEFT JOIN archivos 
            ON intercambios.id_intercambio = archivos.id_intercambio AND archivos.tipo_archivo = 'pdf'
        WHERE 1=1
    """
    params = []
    if search_numero:
        query += " AND intercambios.numero_intercambio LIKE %s"
        params.append(f"%{search_numero}%")
    if search_estado:
        query += " AND intercambios.concepto = %s"
        params.append(search_estado)
    if search_fecha:
        query += " AND DATE(intercambios.fecha_solicitud) = %s"
        params.append(search_fecha)

    query += " GROUP BY intercambios.numero_intercambio"

    cursor.execute(query, params)
    intercambios = cursor.fetchall()

    # Convertir fechas a formato DD-MM-YYYY
    for intercambio in intercambios:
        if intercambio['fecha_solicitud']:
            try:
                # Usar la clase datetime para strptime
                fecha_original = datetime.strptime(str(intercambio['fecha_solicitud']), "%Y-%m-%d")
                intercambio['fecha_solicitud'] = fecha_original.strftime("%d-%m-%Y")
            except ValueError:
                intercambio['fecha_solicitud'] = intercambio['fecha_solicitud']  # En caso de error, dejar sin cambios

    cursor.close()
    conn.close()

    # Renderizar plantilla con conceptos y resultados
    return render_template(
        'estado.html',
        intercambios=intercambios,
        conceptos=conceptos,  # Enviar lista de conceptos
        rol=session.get('rol'),
        usuario=session.get('nombre')
    )





#INFORME
@visitas.route('/informe', methods=['GET'])
@login_required
@role_required('supervisor', 'nutricionista', 'administrador')
def informe():
    conn = get_db_connection('visitas')
    cursor = conn.cursor()

    # Obtener los parámetros de búsqueda del cliente
    id_sede = request.args.get('id_sede')
    fecha_ejecucion = request.args.get('fecha_ejecucion')

    # Consulta SQL con JOIN para obtener el informe
    query = """
        SELECT
            detalles_menu.fecha_ejecucion,
            operadores.nombre AS nombre_operador,
            intercambios.numero_intercambio,
            GROUP_CONCAT(DISTINCT sedes.nombre_sede SEPARATOR ', ') AS sedes,
            GROUP_CONCAT(DISTINCT tiporacion.descripcion SEPARATOR ', ') AS descripcion_tipo_racion,
            instituciones_sedes.id_institucion, 
            detalles_menu.numero_menu_intercambio,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_intercambio SEPARATOR ', ') AS menu_intercambio,
            intercambios.concepto      
        FROM intercambios
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN sedes  
            ON instituciones_sedes.id_sede = sedes.id_sede
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
        WHERE 1=1
    """

    # Filtro opcional por id_sede (sede seleccionada)
    params = []
    if id_sede:
        query += " AND instituciones_sedes.id_sede = %s"
        params.append(id_sede)

    # Filtro opcional por fecha de ejecución
    if fecha_ejecucion:
        query += " AND DATE(detalles_menu.fecha_ejecucion) = %s"
        params.append(fecha_ejecucion)

    # Agrupar resultados
    query += " GROUP BY detalles_menu.fecha_ejecucion, intercambios.numero_intercambio, operadores.nombre, intercambios.concepto"

    # Ejecutar la consulta con los filtros
    cursor.execute(query, params)
    intercambios = cursor.fetchall()

    # Obtener todas las sedes para el formulario
    cursor.execute("SELECT id_sede, nombre_sede FROM sedes")
    sedes = cursor.fetchall()
    
    # Obtener todos los operadores
    cursor.execute("SELECT id_operador, nombre FROM operadores")
    operadores = cursor.fetchall()
    
    # Obtener todos los tipos de ración
    cursor.execute("SELECT id_tipo_racion, descripcion FROM tiporacion")
    tipos_racion = cursor.fetchall()

    # Renderizar la plantilla HTML y pasar los datos obtenidos a la misma
    return render_template('informe.html', intercambios=intercambios, sedes=sedes, operadores=operadores, tipos_racion=tipos_racion, fecha_ejecucion=fecha_ejecucion, rol=session.get('rol'), usuario=session.get('nombre'))

@visitas.route('/download_informe', methods=['GET'])
@login_required
def download_informe():
    conn = get_db_connection('visitas')
    cursor = conn.cursor()

    id_sede = request.args.get('id_sede')
    fecha_ejecucion = request.args.get('fecha_ejecucion')

    query = """
        SELECT
            detalles_menu.fecha_ejecucion,
            operadores.nombre AS nombre_operador,
            intercambios.numero_intercambio,
            GROUP_CONCAT(DISTINCT sedes.nombre_sede SEPARATOR ', ') AS sedes,
            GROUP_CONCAT(DISTINCT tiporacion.descripcion SEPARATOR ', ') AS descripcion_tipo_racion,
            instituciones_sedes.id_institucion, 
            detalles_menu.numero_menu_intercambio,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_intercambio SEPARATOR ', ') AS menu_intercambio,
            intercambios.concepto
        FROM intercambios
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN sedes  
            ON instituciones_sedes.id_sede = sedes.id_sede
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
        WHERE 1=1
    """

    params = []

    if id_sede:
        query += " AND instituciones_sedes.id_sede = %s"
        params.append(id_sede)

    if fecha_ejecucion:
        query += " AND DATE(detalles_menu.fecha_ejecucion) = %s"
        params.append(fecha_ejecucion)

    query += " GROUP BY detalles_menu.fecha_ejecucion, intercambios.numero_intercambio, operadores.nombre, intercambios.concepto"

    cursor.execute(query, params)
    intercambios = cursor.fetchall()

    buffer = BytesIO()
    
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Obtener el estilo de párrafo predeterminado
    styles = getSampleStyleSheet()
    
    # Crear un estilo de párrafo con letra más pequeña
    small_style = ParagraphStyle(
        'Small',
        fontName='Helvetica',
        fontSize=6,  # Ajusta el tamaño de la fuente aquí
        leading=8,   # Espaciado entre líneas
        alignment=TA_CENTER
    )

    title_style = styles['Title']
    title = Paragraph("Informe de Intercambios", title_style)

    # Encabezado de la tabla
    data = [["Fecha de Ejecución", "Número", "N° Aval", "Operador", "Nombre de Sede", "Modalidad", "Menú a Entregar", "Detalles del Menú"]]

    # Rellenar la tabla con los datos del intercambio, usando el estilo con letra pequeña
    for intercambio in intercambios:
        fecha_ejecucion = intercambio[0]
        if isinstance(fecha_ejecucion, date):
            fecha_str = fecha_ejecucion.strftime("%d/%m/%Y")
        else:
            fecha_str = str(fecha_ejecucion) if fecha_ejecucion is not None else 'N/A'
        
        data.append([
            Paragraph(fecha_str, small_style),
            Paragraph(str(intercambio[2]), small_style),
            Paragraph(str(intercambio[8]), small_style),
            Paragraph(str(intercambio[1]), small_style),
            Paragraph(str(intercambio[3]), small_style),
            Paragraph(str(intercambio[4]), small_style),
            Paragraph(str(intercambio[6]), small_style),
            Paragraph(str(intercambio[7]), small_style)
        ])


    # Ajustar el ancho de las columnas
    col_widths = [1.0 * inch, 0.9 * inch, 0.8 * inch, 1.5 * inch, 1.5 * inch, 1.0 * inch, 1.5 * inch, 1.5 * inch]

    # Crear la tabla con los estilos
    table = Table(data, colWidths=col_widths, rowHeights=None)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 6),  # Tamaño de fuente general
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente el texto
        ('WORDWRAP', (0, 0), (-1, -1), True)
    ]))

    elements = [title, table]

    pdf.build(elements)

    buffer.seek(0)
    
    fecha_ejecucion_formato = fecha_ejecucion if fecha_ejecucion else 'sin_fecha'
    filename = f"{fecha_ejecucion_formato} - Informe Intercambio.pdf"
    
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='visitaslication/pdf')

#BASE CONSOLIDAD

@visitas.route('/base_consolidado', methods=['GET'])
@login_required
@role_required('nutricionista', 'administrador')
def base_consolidado():
    conn = get_db_connection('visitas')
    if conn is None:
        return "Error al conectar a la base de datos.", 500
    
    cursor = conn.cursor()

    # Obtener parámetros de filtro de la solicitud GET
    id_sede = request.args.get('id_sede')
    tipo_racion = request.args.get('tipo_racion')
    numero_intercambio = request.args.get('numero_intercambio')
    fecha_ejecucion = request.args.get('fecha_ejecucion')
    filtrar_operador = request.args.get('filtrar_operador')

    # Consulta SQL con JOIN para obtener el informe
    query = """
        SELECT
            intercambios.correo_operador,
            operadores.nombre AS nombre_operador,
            intercambios.fecha_solicitud,
            GROUP_CONCAT(DISTINCT detalles_menu.fecha_ejecucion SEPARATOR ', '),
            tiporacion.descripcion AS tipo_racion,
            intercambios.numero_intercambio,
            
            -- Componentes y menús oficiales e intercambios sin concatenación
            GROUP_CONCAT(DISTINCT detalles_menu.componente SEPARATOR ', ') AS componente, 
            GROUP_CONCAT(DISTINCT detalles_menu.numero_menu_oficial SEPARATOR ', ') AS numero_menu_oficial,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_oficial SEPARATOR ', ') AS menu_oficial,
            GROUP_CONCAT(DISTINCT detalles_menu.numero_menu_intercambio SEPARATOR ', ') AS numero_menu_intercambio,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_intercambio SEPARATOR ', ') AS menu_intercambio,

            -- Información de sedes
            GROUP_CONCAT(DISTINCT sedes.nombre_sede SEPARATOR ', ') AS sedes,

            -- Información adicional sobre el intercambio
            intercambios.justificacion_texto,
            intercambios.justificacion,
            intercambios.concepto,

            -- Archivos adjuntos al intercambio
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'pdf', archivos.nombre_archivo, NULL)) AS archivos_pdf,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'soporte', archivos.nombre_archivo, NULL)) AS archivos_soporte,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'estado', archivos.nombre_archivo, NULL)) AS archivos_aprobar
            
        FROM 
            intercambios

        -- Relación con sedes e instituciones
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio

        -- Detalles de los menús
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio

        -- Información de las sedes
        INNER JOIN sedes  
            ON instituciones_sedes.id_sede = sedes.id_sede

        -- Información de los operadores
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador

        -- Información sobre el tipo de ración
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion

        -- Archivos relacionados al intercambio
        LEFT JOIN archivos 
            ON intercambios.id_intercambio = archivos.id_intercambio
            AND archivos.tipo_archivo IN ('estado', 'pdf', 'soporte')  
        WHERE 1=1
    """

    # Inicializar la lista de parámetros
    parameters = []

    # Agregar condiciones de filtro
    if id_sede:
        query += " AND instituciones_sedes.id_sede = %s"
        parameters.append(id_sede)
    if tipo_racion:
        query += " AND intercambios.id_tipo_racion = %s"
        parameters.append(tipo_racion)
    if numero_intercambio:
        query += " AND intercambios.numero_intercambio = %s"
        parameters.append(numero_intercambio)
    if fecha_ejecucion:
        query += " AND detalles_menu.fecha_ejecucion = %s"
        parameters.append(fecha_ejecucion)
    if filtrar_operador:
        query += " AND intercambios.id_operador = %s"
        parameters.append(filtrar_operador)

    # Finalizar la consulta con GROUP BY para filas únicas de cada número de menú oficial e intercambio
    query += """
        GROUP BY 
            intercambios.id_intercambio,
            detalles_menu.fecha_ejecucion,
            detalles_menu.numero_menu_oficial,
            detalles_menu.numero_menu_intercambio
    """
    
    # Ejecutar la consulta con parámetros
    
    cursor.execute(query, parameters)  # Pasa la lista de parámetros aquí
    intercambios = cursor.fetchall()

    # Procesar los resultados de intercambios
    intercambios_enriquecidos = []

    for intercambio in intercambios:
        archivos_pdf = intercambio[15].split(',') if intercambio[15] else []
        archivos_soporte = intercambio[16].split(',') if intercambio[16] else []
        archivos_aprobar = intercambio[17].split(',') if intercambio[17] else []

        # Enriquecer cada intercambio con los archivos
        intercambio_dict = {
            'datos': intercambio,  # Mantén los datos originales en una clave
            'archivos_pdf': archivos_pdf,
            'archivos_soporte': archivos_soporte,
            'archivos_aprobar': archivos_aprobar,
        }

        intercambios_enriquecidos.append(intercambio_dict)
    
    # Obtener todas las sedes para el formulario
    cursor.execute("SELECT id_sede, nombre_sede FROM sedes")
    sedes = cursor.fetchall()
    
    # Obtener todos los operadores
    cursor.execute("SELECT id_operador, nombre FROM operadores")
    operadores = cursor.fetchall()
    
    # Obtener todos los tipos de ración
    cursor.execute("SELECT id_tipo_racion, descripcion FROM tiporacion")
    tipos_racion = cursor.fetchall()
    cursor.close()
    conn.close()

    # Renderizar la plantilla HTML y pasar los datos obtenidos a la misma
    return render_template('base_consolidado.html', intercambios=intercambios_enriquecidos, sedes=sedes, operadores=operadores, tipos_racion=tipos_racion, rol=session.get('rol'), usuario=session.get('nombre'))

import pandas as pd
from flask import Response, send_file, request, flash, redirect, url_for
from io import BytesIO

@visitas.route('/exportar_intercambios', methods=['GET'])
@login_required
@role_required('nutricionista', 'administrador')
def exportar_intercambios():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    conexion = get_db_connection('visitas')
    if conexion is None:
        flash("Error de conexión con la base de datos", "danger")
        return redirect(url_for('base_consolidado'))

    try:
        cursor = conexion.cursor(dictionary=True)

        # Consulta SQL con filtro de fechas
        query = """
        SELECT 
            intercambios.correo_operador,
            operadores.nombre AS nombre_operador,
            intercambios.fecha_solicitud,
            GROUP_CONCAT(DISTINCT detalles_menu.fecha_ejecucion SEPARATOR ', ') AS fechas_ejecucion,
            tiporacion.descripcion AS tipo_racion,
            intercambios.numero_intercambio,
            GROUP_CONCAT(DISTINCT detalles_menu.componente SEPARATOR ', ') AS componente, 
            GROUP_CONCAT(DISTINCT detalles_menu.numero_menu_oficial SEPARATOR ', ') AS numero_menu_oficial,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_oficial SEPARATOR ', ') AS menu_oficial,
            GROUP_CONCAT(DISTINCT detalles_menu.numero_menu_intercambio SEPARATOR ', ') AS numero_menu_intercambio,
            GROUP_CONCAT(DISTINCT detalles_menu.menu_intercambio SEPARATOR ', ') AS menu_intercambio,
            GROUP_CONCAT(DISTINCT sedes.nombre_sede SEPARATOR ', ') AS sedes,
            intercambios.justificacion_texto,
            intercambios.justificacion,
            intercambios.concepto,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'pdf', archivos.nombre_archivo, NULL)) AS archivos_pdf,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'soporte', archivos.nombre_archivo, NULL)) AS archivos_soporte,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'estado', archivos.nombre_archivo, NULL)) AS archivos_aprobar,
            -- Información de firmas
            GROUP_CONCAT(DISTINCT firmas.nombre_operador SEPARATOR ', ') AS firmantes,
            GROUP_CONCAT(DISTINCT firmas.tarjeta_profesional SEPARATOR ', ') AS tarjetas_profesionales,
            GROUP_CONCAT(DISTINCT firmas.cargo SEPARATOR ', ') AS cargos_firmantes

        FROM 
            intercambios
        INNER JOIN instituciones_sedes ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN sedes ON instituciones_sedes.id_sede = sedes.id_sede
        INNER JOIN operadores ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
        LEFT JOIN archivos ON intercambios.id_intercambio = archivos.id_intercambio
            AND archivos.tipo_archivo IN ('estado', 'pdf', 'soporte')
        LEFT JOIN firmas ON intercambios.id_intercambio = firmas.id_intercambio  -- Relacionando firmas
        WHERE 1=1
        """

        # Agregar filtros de fecha si están presentes
        params = []
        if fecha_inicio:
            query += " AND intercambios.fecha_solicitud >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND intercambios.fecha_solicitud <= %s"
            params.append(fecha_fin)

        query += " GROUP BY intercambios.numero_intercambio ORDER BY intercambios.fecha_solicitud DESC"

        cursor.execute(query, tuple(params))
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()

        # Convertir a DataFrame de pandas
        df = pd.DataFrame(datos)

        # Crear un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Intercambios", index=False)

        output.seek(0)  # Ir al inicio del archivo en memoria

        # Enviar el archivo como respuesta
        return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name="intercambios.xlsx")

    except Exception as e:
        flash(f"Error al exportar a Excel: {e}", "danger")
        return redirect(url_for('base_consolidado'))

import zipfile
import io

@visitas.route('/descargar_zip')
@login_required
@role_required('nutricionista', 'administrador')
def descargar_zip():
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        base_dirs = ['pdfs', 'soporte', 'estado']
        base_path = os.path.join(os.getcwd(), 'static', 'uploads', 'solicitud_intercambio')
        
        for base_dir in base_dirs:
            full_path = os.path.join(base_path, base_dir)
            if os.path.exists(full_path):
                for root, _, files in os.walk(full_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Mantener la estructura dentro de "solicitud_intercambio"
                        zipf.write(file_path, os.path.relpath(file_path, base_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='archivos_importantes.zip')



@visitas.route('/eliminar_intercambio/<string:numero_intercambio>', methods=['DELETE'])
@login_required
@role_required('nutricionista', 'administrador')
def eliminar_intercambio(numero_intercambio):
    conexion = get_db_connection('visitas')

    if conexion is None:
        return jsonify({'success': False, 'message': 'Error de conexión con la base de datos'}), 500

    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM intercambios WHERE numero_intercambio = %s", (numero_intercambio,))
        conexion.commit()
        return jsonify({'success': True, 'message': 'Intercambio eliminado correctamente'}), 200

    except Error as e:
        return jsonify({'success': False, 'message': f'Error al eliminar el intercambio: {e}'}), 500

    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()



@visitas.route('/uploads/<path:filename>', methods=['GET'])
@login_required
def upload_file(filename):
    upload_folder = visitas.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, filename)

    if not os.path.isfile(filepath):
        return "Archivo no encontrado.", 404  

    return send_from_directory(upload_folder, filename)


@visitas.route('/download/<path:filename>', methods=['GET'])
@login_required
def download_file(filename):
    try:
        # Cambia 'uploads' al directorio donde se guardan tus archivos
        return send_from_directory('uploads', filename, as_attachment=True)
    except Exception as e:
        abort(404)


#OPERADOR
@visitas.route('/base_operador', methods=['GET'])
@login_required
@role_required('operador', 'administrador')
def base_operador():
    conn = get_db_connection('visitas')
    if conn is None:
        return "Error al conectar a la base de datos.", 500

    cursor = conn.cursor()

    # Obtener el rol y el id_operador del usuario desde la sesión
    rol = session.get('rol')
    id_operador = session.get('id_operador')

    # Construir la consulta base
    query = """
        SELECT
            operadores.id_operador,
            operadores.nombre AS nombre_operador,
            intercambios.fecha_solicitud,
            detalles_menu.fecha_ejecucion,
            tiporacion.descripcion AS tipo_racion,
            intercambios.numero_intercambio,
            detalles_menu.componente AS componente, 
            detalles_menu.numero_menu_oficial AS numero_menu_oficial,
            detalles_menu.menu_oficial AS menu_oficial,
            detalles_menu.numero_menu_intercambio AS numero_menu_intercambio,
            detalles_menu.menu_intercambio AS menu_intercambio,
            GROUP_CONCAT(DISTINCT sedes.nombre_sede SEPARATOR ', ') AS sedes,
            intercambios.justificacion_texto,
            intercambios.justificacion,
            intercambios.concepto,
            intercambios.mensaje,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'pdf', archivos.nombre_archivo, NULL)) AS archivos_pdf,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'soporte', archivos.nombre_archivo, NULL)) AS archivos_soporte,
            GROUP_CONCAT(DISTINCT IF(archivos.tipo_archivo = 'estado', archivos.nombre_archivo, NULL)) AS archivos_aprobar,
            intercambios.asunto
        FROM 
            intercambios
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN sedes  
            ON instituciones_sedes.id_sede = sedes.id_sede
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
        LEFT JOIN archivos 
            ON intercambios.id_intercambio = archivos.id_intercambio
            AND archivos.tipo_archivo IN ('estado', 'pdf', 'soporte')
        WHERE 1=1
    """

    # Inicializar la lista de parámetros
    parameters = []

    # Filtrar por id_operador si no es administrador
    if rol != 'administrador':
        if not id_operador:
            return "El usuario no tiene un operador asignado.", 403
        query += " AND intercambios.id_operador = %s"
        parameters.append(id_operador)

    # Obtener parámetros de filtro de la solicitud GET
    id_sede = request.args.get('id_sede')
    tipo_racion = request.args.get('tipo_racion')
    numero_intercambio = request.args.get('numero_intercambio')
    fecha_ejecucion = request.args.get('fecha_ejecucion')
    concepto = request.args.get('concepto')
    
    # Agregar condiciones de filtro adicionales
    if id_sede:
        query += " AND instituciones_sedes.id_sede = %s"
        parameters.append(id_sede)
    if tipo_racion:
        query += " AND intercambios.id_tipo_racion = %s"
        parameters.append(tipo_racion)
    if numero_intercambio:
        query += " AND intercambios.numero_intercambio = %s"
        parameters.append(numero_intercambio)
    if fecha_ejecucion:
        query += " AND detalles_menu.fecha_ejecucion = %s"
        parameters.append(fecha_ejecucion)
    if concepto:
        query += " AND intercambios.concepto = %s"
        parameters.append(concepto)

    # Finalizar la consulta con GROUP BY
    query += """
        GROUP BY 
            intercambios.id_intercambio
    """

    # Ejecutar la consulta
    cursor.execute(query, parameters)
    intercambios = cursor.fetchall()

    # Procesar los resultados y verificar si se debe mostrar una notificación
    mostrar_notificacion = False
    conceptos_relevantes = ['Aprobado', 'Negado', 'Modificado']
    intercambios_enriquecidos = []
    for intercambio in intercambios:
        archivos_pdf = intercambio[16].split(',') if intercambio[16] else []
        archivos_soporte = intercambio[17].split(',') if intercambio[17] else []
        archivos_aprobar = intercambio[18].split(',') if intercambio[18] else []

        intercambio_dict = {
            'id_operador': intercambio[0],
            'nombre_operador': intercambio[1],
            'datos': intercambio[2:],
            'archivos_pdf': archivos_pdf,
            'archivos_soporte': archivos_soporte,
            'archivos_aprobar': archivos_aprobar,
        }

        # Verificar si el concepto es relevante
        if intercambio[14] in conceptos_relevantes:
            mostrar_notificacion = True

        intercambios_enriquecidos.append(intercambio_dict)

    # Obtener datos auxiliares para el formulario
    cursor.execute("SELECT id_sede, nombre_sede FROM sedes")
    sedes = cursor.fetchall()
    cursor.execute("SELECT id_tipo_racion, descripcion FROM tiporacion")
    tipos_racion = cursor.fetchall()
    cursor.execute("SELECT DISTINCT concepto FROM intercambios WHERE concepto IS NOT NULL")
    conceptos = cursor.fetchall()

    cursor.close()
    conn.close()

    # Renderizar la plantilla
    return render_template(
        'base_operador.html',
        intercambios=intercambios_enriquecidos,
        sedes=sedes,
        tipos_racion=tipos_racion,
        conceptos=conceptos,
        rol=rol,
        usuario=session.get('nombre'),
        id_operador=id_operador,
        mostrar_notificacion=mostrar_notificacion
    )




#SOLCITAR MODIFICAR
@visitas_bp.route('/modificar-intercambio/<string:numero_intercambio>', methods=['POST'])
@login_required
def modificar_intercambio(numero_intercambio):
    try:
        # Extraer datos de la solicitud
        data = request.get_json()
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')

        # Conectar a la base de datos
        conn = get_db_connection('visitas')
        cursor = conn.cursor()

        # Actualizar el concepto en la base de datos
        query = "UPDATE intercambios SET concepto = 'Modificado', asunto = %s, mensaje = %s WHERE numero_intercambio = %s"
        cursor.execute(query, (asunto, mensaje, numero_intercambio))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Para depuración
        return jsonify({'status': 'error', 'message': str(e)}), 500




@visitas.route('/solicitar_modificar_intercambio', methods=['GET', 'POST'])
@login_required
@role_required('operador', 'administrador', 'nutricionista')
def solicitar_modificar_intercambio():
    conn = get_db_connection('visitas')
    if conn is None:
        return "Error al conectar a la base de datos.", 500

    cursor = conn.cursor()
    correo_usuario = session.get('correo')
    rol_usuario = session.get('rol')  # Asumimos que el rol está en la sesión

    if not correo_usuario:
        return "Usuario no autenticado.", 403

    try:
        # Determinar la consulta según el rol del usuario
        if rol_usuario in ['administrador', 'nutricionista']:
            query = """
                SELECT
                    operadores.nombre AS nombre_operador,
                    tiporacion.descripcion,
                    intercambios.numero_intercambio,
                    intercambios.asunto,
                    intercambios.mensaje
                FROM intercambios
                INNER JOIN operadores 
                    ON intercambios.id_operador = operadores.id_operador
                INNER JOIN tiporacion 
                    ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
                WHERE intercambios.concepto = 'Modificado'
                GROUP BY operadores.nombre, tiporacion.descripcion, intercambios.numero_intercambio
            """
            cursor.execute(query)
        else:
            # Obtener el id_operador del usuario
            query_usuario = """
                SELECT id_operador FROM usuarios WHERE correo = %s
            """
            cursor.execute(query_usuario, (correo_usuario,))
            id_operador_usuario = cursor.fetchone()
            
            if id_operador_usuario is None:
                return "Usuario no encontrado.", 404

            id_operador = id_operador_usuario[0]

            # Consulta para operadores
            query = """
                SELECT
                    operadores.nombre AS nombre_operador,
                    tiporacion.descripcion,
                    intercambios.numero_intercambio,
                    intercambios.asunto,
                    intercambios.mensaje
                FROM intercambios
                INNER JOIN operadores 
                    ON intercambios.id_operador = operadores.id_operador
                INNER JOIN tiporacion 
                    ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
                WHERE intercambios.concepto = 'Modificado' AND intercambios.id_operador = %s
                GROUP BY operadores.nombre, tiporacion.descripcion, intercambios.numero_intercambio
            """
            cursor.execute(query, (id_operador,))

        intercambios = cursor.fetchall()

    except Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return "Error al ejecutar la consulta.", 500
    finally:
        cursor.close()
        conn.close()

    # Renderizar la plantilla para mostrar la lista de intercambios modificados
    return render_template('solicitar_modificar_intercambio.html', intercambios=intercambios, rol=rol_usuario, usuario=session.get('nombre'))

import traceback

#MODIFICAR

@visitas.route('/modificar_intercambio2/<string:numero_intercambio>', methods=['GET', 'POST'])
@login_required
@role_required('operador', 'administrador', 'nutricionista')
def modificar_intercambio2(numero_intercambio):
    conn = get_db_connection('visitas')
    cursor = None
    try:
        if conn is None:
            return "No se pudo establecer la conexión a la base de datos.", 500

        cursor = conn.cursor()

        if request.method == 'GET':
            # Obtener datos del intercambio
            cursor.execute("""
                SELECT
                    intercambios.correo_operador,
                    operadores.nombre AS nombre_operador,
                    intercambios.fecha_solicitud,
                    detalles_menu.fecha_ejecucion,
                    tiporacion.descripcion,
                    intercambios.numero_intercambio,
                    GROUP_CONCAT(DISTINCT detalles_menu.componente ORDER BY detalles_menu.componente) AS componentes,
                    detalles_menu.numero_menu_oficial,
                    GROUP_CONCAT(DISTINCT detalles_menu.menu_oficial ORDER BY detalles_menu.menu_oficial) AS menu_oficial,
                    detalles_menu.numero_menu_intercambio,
                    GROUP_CONCAT(DISTINCT detalles_menu.menu_intercambio ORDER BY detalles_menu.menu_intercambio) AS menu_intercambio,
                    intercambios.justificacion_texto,
                    intercambios.justificacion,
                    intercambios.concepto
                FROM intercambios
                INNER JOIN instituciones_sedes ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
                INNER JOIN detalles_menu ON intercambios.id_intercambio = detalles_menu.id_intercambio
                INNER JOIN operadores ON intercambios.id_operador = operadores.id_operador
                INNER JOIN tiporacion ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion
                WHERE intercambios.numero_intercambio = %s
                GROUP BY detalles_menu.fecha_ejecucion, detalles_menu.numero_menu_oficial, detalles_menu.numero_menu_intercambio;
            """, (numero_intercambio,))
            intercambio_data = cursor.fetchall()

            if not intercambio_data:
                return "Intercambio no encontrado.", 404

            # Preparar datos generales
            datos_generales = {
                'correo': intercambio_data[0][0],
                'nombre_operador': intercambio_data[0][1],
                'fecha_solicitud': intercambio_data[0][2],
                'descripcion': intercambio_data[0][4],
                'numero_intercambio': intercambio_data[0][5],
                'justificacion_texto': intercambio_data[0][11],
                'concepto': intercambio_data[0][13]
            }

            # Generar índices para fechas y grupos
            datos_por_fecha = []
            fecha_index = 0
            for row in intercambio_data:
                fecha_ejecucion = row[3]  # Obtener la fecha del registro
                if fecha_ejecucion in (None, "0000-00-00"):
                    fecha_ejecucion_formateada = "Fecha no disponible"
                else:
                    fecha_ejecucion_formateada = fecha_ejecucion.strftime('%Y-%m-%d')

                # Verificar si la fecha ya existe en datos_por_fecha
                fecha_data = next((f for f in datos_por_fecha if f['fecha'] == fecha_ejecucion_formateada), None)
                if not fecha_data:
                    fecha_data = {'fecha': fecha_ejecucion_formateada, 'fecha_index': fecha_index, 'grupos': []}
                    datos_por_fecha.append(fecha_data)
                    fecha_index += 1

                # Calcular el grupo_index dinámicamente
                grupo_index = len(fecha_data['grupos'])  # Basado en el tamaño actual de los grupos de esta fecha
                fecha_data['grupos'].append({
                    'grupo_index': grupo_index,
                    'componentes': row[6].split(','),
                    'menu_oficial': row[8].split(','),
                    'menu_intercambio': row[10].split(','),
                    'numero_menu_oficial': row[7],
                    'numero_menu_intercambio': row[9]
                })


            return render_template('modificar_intercambio2.html',
                                   datos=datos_generales,
                                   datos_por_fecha=datos_por_fecha,
                                   numero_intercambio=numero_intercambio, rol=session.get('rol'), usuario=session.get('nombre'))
            
        elif request.method == 'POST':
            try:
                # Capturar justificación
                justificacion_texto = request.form.get('justificacion_texto', '').strip()
                cursor.execute("""
                    UPDATE intercambios
                    SET justificacion_texto = %s, concepto = 'Pendiente'
                    WHERE numero_intercambio = %s
                """, (justificacion_texto, numero_intercambio))

                datos_por_fecha = {}

                # Procesar fechas y grupos
                fecha_index = 0
                while True:
                    nueva_fecha_ejecucion = request.form.get(f'fecha_ejecucion_{fecha_index}')
                    if not nueva_fecha_ejecucion:
                        break

                    nueva_fecha_ejecucion = nueva_fecha_ejecucion.strip()
                    if nueva_fecha_ejecucion not in datos_por_fecha:
                        datos_por_fecha[nueva_fecha_ejecucion] = []

                    grupo_index = 0
                    while True:
                        numero_menu_oficial = request.form.get(f'numero_menu_oficial_{fecha_index}_{grupo_index}')
                        numero_menu_intercambio = request.form.get(f'numero_menu_intercambio_{fecha_index}_{grupo_index}')

                        if not numero_menu_oficial and not numero_menu_intercambio:
                            break

                        numero_menu_oficial = numero_menu_oficial.strip() if numero_menu_oficial else "N/A"
                        numero_menu_intercambio = numero_menu_intercambio.strip() if numero_menu_intercambio else "N/A"

                        nuevos_componentes = []
                        nuevos_menu_oficial = []
                        nuevos_menus_intercambio = []

                        componente_index = 0
                        while True:
                            nuevo_componente = request.form.get(f'componente_{fecha_index}_{grupo_index}_{componente_index}')
                            nuevo_menu_oficial = request.form.get(f'menu_oficial_{fecha_index}_{grupo_index}_{componente_index}')
                            nuevo_menu_intercambio = request.form.get(f'menu_intercambio_{fecha_index}_{grupo_index}_{componente_index}')

                            if not nuevo_componente and not nuevo_menu_intercambio:
                                break

                            if nuevo_componente:
                                nuevos_componentes.append(nuevo_componente.strip())
                            if nuevo_menu_oficial:
                                nuevos_menu_oficial.append(nuevo_menu_oficial.strip())
                            if nuevo_menu_intercambio:
                                nuevos_menus_intercambio.append(nuevo_menu_intercambio.strip())

                            componente_index += 1

                        # Agregar al diccionario
                        datos_por_fecha[nueva_fecha_ejecucion].append({
                            'numero_menu_oficial': numero_menu_oficial,
                            'numero_menu_intercambio': numero_menu_intercambio,
                            'componentes': nuevos_componentes,
                            'menu_oficial': nuevos_menu_oficial,
                            'menu_intercambio': nuevos_menus_intercambio
                        })

                        # Actualizar base de datos
                        cursor.execute("""
                            UPDATE detalles_menu
                            SET fecha_ejecucion = %s,
                                numero_menu_intercambio = %s,
                                menu_intercambio = %s
                            WHERE id_intercambio = (SELECT id_intercambio FROM intercambios WHERE numero_intercambio = %s)
                            AND fecha_ejecucion = %s
                        """, (nueva_fecha_ejecucion, numero_menu_intercambio, ', '.join(nuevos_menus_intercambio), numero_intercambio, nueva_fecha_ejecucion))

                        grupo_index += 1
                    fecha_index += 1

                # Confirmar cambios
                
                session['datos_por_fecha'] = datos_por_fecha
                print("Datos agrupados por fecha:", datos_por_fecha)

                # Obtener información adicional para generar el PDF y enviar correo
                # Obtener información del intercambio con JOINs para traer el nombre del operador y la descripción del tipo de ración
                cursor.execute("""
                    SELECT 
                        i.id_intercambio, 
                        o.nombre AS nombre_operador, 
                        t.descripcion AS tipo_racion, 
                        i.correo, 
                        i.fecha_solicitud
                    FROM intercambios i
                    JOIN operadores o ON i.id_operador = o.id_operador
                    JOIN tiporacion t ON i.id_tipo_racion = t.id_tipo_racion
                    WHERE i.numero_intercambio = %s
                """, (numero_intercambio,))
                intercambio_info = cursor.fetchone()

                if not intercambio_info:
                    print("Error: No se encontró información de intercambio.")
                    return "Error: No se encontraron datos de intercambio.", 500

                # Obtener instituciones y sedes asociadas al intercambio
                cursor.execute("""
                    SELECT 
                        inst.sede_educativa AS institucion_nombre, 
                        s.nombre_sede AS sede_nombre
                    FROM instituciones_sedes i
                    JOIN instituciones inst ON i.id_institucion = inst.id_institucion
                    JOIN Sedes s ON i.id_sede = s.id_sede
                    JOIN intercambios ic ON i.id_intercambio = ic.id_intercambio
                    WHERE ic.numero_intercambio = %s
                """, (numero_intercambio,))
                instituciones_sedes = cursor.fetchall()


                cursor.execute("""
                    SELECT nombre_operador, tarjeta_profesional, cargo, tipo_firma, firma_foto_ruta, firma_manual_base64
                    FROM firmas
                    WHERE id_intercambio = %s
                """, (intercambio_info[0],))
                firmas_lista = cursor.fetchall()

                # Generar el PDF
                # Asignar variables a partir de la consulta SQL corregida
                id_intercambio, nombre_operador, tipo_racion, correo, fecha_solicitud = intercambio_info


                # Llamada a la función modificar_pdf con los nombres actualizados
                pdf_output_path = modificar_pdf(
                    intercambio_id=id_intercambio,
                    operador=nombre_operador,  # Ahora es el nombre del operador
                    tipo_racion=tipo_racion,  # Ahora es la descripción del tipo de ración
                    justificacion_texto=justificacion_texto,
                    datos_por_fecha=datos_por_fecha,
                    numero_intercambio_unica=numero_intercambio,
                    correo=correo,
                    instituciones_sedes=instituciones_sedes,
                    firmas_lista=firmas_lista,
                    fecha_solicitud=fecha_solicitud
                )
                
                try:
                    # Verificar si ya existe un archivo de tipo 'pdf' para el mismo id_intercambio
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM archivos
                        WHERE id_intercambio = %s AND tipo_archivo = 'pdf'
                    """, (id_intercambio,))
                    existe_pdf = cursor.fetchone()[0]
                    print(f"PDF existente: {existe_pdf}")

                    if existe_pdf:
                        # Actualizar registro existente
                        cursor.execute("""
                            UPDATE archivos
                            SET nombre_archivo = %s, ruta_archivo = %s
                            WHERE id_intercambio = %s AND tipo_archivo = 'pdf'
                        """, (f"{numero_intercambio}.pdf", f'static/uploads/solicitud_intercambio/pdfs/{numero_intercambio}/{numero_intercambio}.pdf', id_intercambio))
                        print("Archivo PDF actualizado exitosamente.")
                    else:
                        # Insertar nuevo registro
                        cursor.execute("""
                            INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                            VALUES (%s, %s, %s, %s)
                        """, (id_intercambio, f"{numero_intercambio}.pdf", f'static/uploads/solicitud_intercambio/pdfs/{numero_intercambio}/{numero_intercambio}.pdf', pdf_output_path))
                        print("Archivo PDF insertado exitosamente.")

                    # Crear la carpeta principal "soporte" si no existe
                    soporte_folder_path = os.path.join(visitas.config['UPLOAD_FOLDER'], "soporte")
                    os.makedirs(soporte_folder_path, exist_ok=True)
                    print(f"Carpeta soporte: {soporte_folder_path}")

                    # Crear una subcarpeta específica para este `numero_intercambio`
                    intercambio_folder_path = os.path.join(soporte_folder_path, numero_intercambio)
                    os.makedirs(intercambio_folder_path, exist_ok=True)
                    print(f"Carpeta para el número de intercambio: {intercambio_folder_path}")

                    # Obtener los archivos del formulario
                    pdf_adjuntos = request.files.getlist('pdf_adjunto[]')
                    print(f"Archivos subidos: {pdf_adjuntos}")

                    for pdf in pdf_adjuntos:
                        if pdf and pdf.filename.lower().endswith('.pdf'):
                            # Asegurar el nombre del archivo
                            filename = secure_filename(pdf.filename)
                            file_path = os.path.join(intercambio_folder_path, filename)  # Ruta en la subcarpeta de `numero_intercambio`
                            pdf.save(file_path)  # Guardar archivo en el servidor
                            print(f"Archivo guardado: {file_path}")

                            # Verificar si ya existe un archivo para este `id_intercambio` y tipo 'soporte'
                            cursor.execute("""
                                SELECT COUNT(*)
                                FROM archivos
                                WHERE id_intercambio = %s AND tipo_archivo = 'soporte'
                            """, (id_intercambio,))
                            existe_soporte = cursor.fetchone()[0]
                            print(f"Archivo soporte existente: {existe_soporte}")

                            if existe_soporte:
                                # Actualizar el registro existente
                                cursor.execute("""
                                    UPDATE archivos
                                    SET nombre_archivo = %s, ruta_archivo = %s
                                    WHERE id_intercambio = %s AND tipo_archivo = 'soporte'
                                """, (filename, file_path, id_intercambio))
                                flash(f"Archivo soporte {filename} actualizado exitosamente.", "success")
                            else:
                                # Insertar un nuevo registro
                                cursor.execute("""
                                    INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                                    VALUES (%s, %s, %s, %s)
                                """, (id_intercambio, filename, 'soporte', file_path))
                                flash(f"Archivo soporte {filename} subido exitosamente.", "success")


                    # Confirmar los cambios
                    conn.commit()
                except Exception as e:
                    print(f"Error al procesar el archivo: {e}")
                    conn.rollback()


                rol_usuario = session.get('rol')
                flash("Ocurrió un error al obtener los detalles de modificado.", "danger")
                if rol_usuario == 'administrador':
                    return redirect(url_for('iniciasesion_bp.dashboard_administrador'))
                elif rol_usuario == 'operador':
                    return redirect(url_for('iniciasesion_bp.dashboard_operador'))
                elif rol_usuario == 'nutricionista':
                    return redirect(url_for('iniciasesion_bp.dashboard_nutricionista'))
                else:
                    flash("Rol no reconocido. Redirigiendo al inicio de sesión.", "danger")
                    return redirect(url_for('iniciasesion_bp.login'))

            except Exception as e:
                error_trace = traceback.format_exc()
                print(f"Error general en el proceso de modificación: {e}\n{error_trace}")
                return "Error al modificar el intercambio.", 500
            
    except Exception as e:
        print(f"Error general en el proceso de modificación: {e}\n{error_trace}")
        return "Error al modificar el intercambio.", 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        
import base64

# REPORTLAB MODIFICAR

import os
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def modificar_pdf(intercambio_id, operador, tipo_racion, justificacion_texto,
                 datos_por_fecha, numero_intercambio_unica, correo, instituciones_sedes, firmas_lista, fecha_solicitud):
    
    pdf_folder_path = os.path.join('static', 'uploads', 'solicitud_intercambio', 'pdfs', str(numero_intercambio_unica))
    os.makedirs(pdf_folder_path, exist_ok=True)
    pdf_path = os.path.join(pdf_folder_path, f"{numero_intercambio_unica}.pdf")
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Agregar logo
    logo_path = 'static/images/cali.png'
    barcode_path = f'static/uploads/solicitud_intercambio/pdfs/{numero_intercambio_unica}/{fecha_solicitud} - {numero_intercambio_unica}.png'

    # Crear imagen del logo
    logo = Image(logo_path, width=70, height=50)

    # Crear código de barras
    barcode = Image(barcode_path, width=120, height=50)  # Ajustar tamaño si es necesario

    # Crear tabla con logo a la izquierda y código de barras a la derecha
    header_table = Table([[logo, barcode]], colWidths=[50, 450], rowHeights=[50])  # Ajustar colWidths según necesidad
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Logo a la izquierda
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Código de barras a la derecha
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Ambos alineados arriba
        ('LEFTPADDING', (0, 0), (0, 0), 0),  # Sin padding en logo
        ('RIGHTPADDING', (1, 0), (1, 0), 0),  # Sin padding en código de barras
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0)
    ]))

    # Agregar la tabla al documento
    elements.append(header_table)
    
    # Título
    elements.append(Paragraph("ANEXO 17.1", styles['Title']))
    elements.append(Paragraph("SOLICITUD DE INTERCAMBIOS", styles['Title']))
    elements.append(Spacer(1, 10))
    
    
    meses = {
        "01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
        "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
        "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"
    }
        
    fecha_formateada = fecha_solicitud.strftime('%d - %m - %Y').replace(fecha_solicitud.strftime('%m'), meses[fecha_solicitud.strftime('%m')])

    # Definir datos en formato de tabla
    data = [
        [Paragraph("<b>DATOS</b>", styles['Normal'])],  # Encabezado de la tabla
        [Paragraph(f"<b>Fecha de Solicitud:</b> {fecha_formateada}", styles['Normal']),
        Paragraph(f"<b>Número Intercambio:</b> {numero_intercambio_unica}", styles['Normal'])],
        [Paragraph(f"<b>Modalidad:</b> {tipo_racion}", styles['Normal'])],
        [Paragraph(f"<b>Operador:</b> {operador}", styles['Normal']), ""],  # Operador en una fila completa
        [Paragraph(f"<b>Instituciones:</b> {', '.join(set(str(inst[0]) for inst in instituciones_sedes))}", styles['Normal']), ""],
        [Paragraph(f"<b>Sedes:</b> {', '.join(set(str(inst[1]) for inst in instituciones_sedes))}", styles['Normal']), ""],
        [Paragraph(f"<b>Justificación:</b> {justificacion_texto}", styles['Normal']), ""]
    ]

    # Crear la tabla
    table = Table(data, colWidths=[220, 220])  # Ajusta los anchos de las columnas según necesidad

    # Estilos para la tabla
    table.setStyle(TableStyle([
        ('SPAN', (0, 0), (-1, 0)),  # Fusiona la primera fila (encabezado)
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fondo gris en el encabezado
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alineación izquierda
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical media
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes en la tabla
        ('SPAN', (0, 3), (-1, 3)),  # Fusionar la fila del operador
        ('SPAN', (0, 4), (-1, 4)),  # Fusionar la fila de instituciones
        ('SPAN', (0, 5), (-1, 5)),  # Fusionar la fila de sedes
        ('SPAN', (0, 6), (-1, 6))   # Fusionar la fila de justificación
    ]))

    # Agregar la tabla a los elementos del PDF
    elements.append(table)
        
    cell_style = ParagraphStyle(
        name="TableText",
        fontName="Helvetica",
        fontSize=7,  # Reducimos tamaño de fuente
        leading=9,  # Ajustamos el espaciado entre líneas
        alignment=1,  # Alineamos el texto al centro
    )

    for fecha, registros in datos_por_fecha.items():
        try:
            fecha_formateada = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d de %B de %Y").capitalize()
        except ValueError:
            fecha_formateada = "Fecha no disponible"

        elements.append(Paragraph(f"Fecha de Ejecución: {fecha_formateada}", styles['Heading2']))
        elements.append(Spacer(1, 10))

        for datos in registros:
            table_data = [
                ["Componente", f"Menú Oficial ({datos.get('numero_menu_oficial', 'N/A')})", f"Menú Intercambio ({datos.get('numero_menu_intercambio', 'N/A')})"]
            ]

            for i in range(len(datos['componentes'])):
                componente = Paragraph(datos['componentes'][i] if i < len(datos['componentes']) else "N/A", cell_style)
                menu_oficial = Paragraph(datos['menu_oficial'][i] if i < len(datos['menu_oficial']) else "N/A", cell_style)
                menu_intercambio = Paragraph(datos['menu_intercambio'][i] if i < len(datos['menu_intercambio']) else "N/A", cell_style)

                table_data.append([componente, menu_oficial, menu_intercambio])

            # Ajustamos anchos de columnas
            table = Table(table_data, colWidths=[146, 146, 146])

            # Aplicar estilos para evitar que el texto cruce los bordes
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reducimos el tamaño de fuente
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(table)
            elements.append(Spacer(1, 10))
    
    # Sección de Firmas en dos columnas
    firmas_data = []
    for i in range(0, len(firmas_lista), 2):
        fila = []
        for j in range(2):
            if i + j < len(firmas_lista):
                nombre, tarjeta, cargo, tipo, foto_ruta, firma_base64 = firmas_lista[i + j]
                firma_elementos = []
                if tipo == 'foto' and foto_ruta:
                    firma_elementos.append(Image(foto_ruta, width=100, height=50))
                elif tipo == 'manual' and firma_base64:
                    firma_base64 = firma_base64.strip()
                    if firma_base64:
                        firma_base64 += '=' * ((4 - len(firma_base64) % 4) % 4)
                        try:
                            firma_data = base64.b64decode(firma_base64)
                            firma_temp_path = os.path.join(pdf_folder_path, f"firma_{nombre}.png")
                            with open(firma_temp_path, 'wb') as f:
                                f.write(firma_data)
                            firma_elementos.append(Image(firma_temp_path, width=100, height=50))
                            os.remove(firma_temp_path)
                        except (base64.binascii.Error, ValueError):
                            firma_elementos.append(Paragraph("Firma inválida", styles['Normal']))
                firma_elementos.append(Paragraph(f"Nombre: {nombre}", styles['Normal']))
                firma_elementos.append(Paragraph(f"Tarjeta Profesional: {tarjeta}", styles['Normal']))
                firma_elementos.append(Paragraph(f"Cargo: {cargo}", styles['Normal']))
                fila.append(firma_elementos)
            else:
                fila.append("")
        firmas_data.append(fila)
    
    firma_table = Table(firmas_data, colWidths=[250, 250])
    firma_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central de contenido
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alineación vertical
        ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Espaciado interno
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))

    
    elements.append(firma_table)
    
    doc.build(elements)



#APROBAR


@visitas.route('/aprobar/<string:numero_intercambio>', methods=['GET', 'POST'])
@login_required
@role_required('nutricionista', 'administrador')
def aprobar(numero_intercambio):
    conn = get_db_connection('visitas')
    if conn is None:
        return "Error al conectar a la base de datos.", 500

    cursor = conn.cursor()

    # Obtener los datos de intercambio en ambos métodos
    cursor.execute("""
        SELECT intercambios.correo_operador, operadores.nombre AS nombre_operador,
            intercambios.fecha_solicitud, detalles_menu.fecha_ejecucion,
            tiporacion.descripcion, intercambios.numero_intercambio,
            detalles_menu.componente, detalles_menu.numero_menu_oficial,
            detalles_menu.menu_oficial, detalles_menu.numero_menu_intercambio,
            detalles_menu.menu_intercambio, instituciones_sedes.id_sede, 
            instituciones_sedes.id_institucion, intercambios.justificacion_texto
        FROM intercambios
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion 
        WHERE intercambios.numero_intercambio = %s
    """, (numero_intercambio,))

    intercambio_data = cursor.fetchall()
    if not intercambio_data:
        return "Intercambio no encontrado.", 404

    # Inicializar listas para instituciones y sedes
    instituciones = []
    sedes = []

    # Recorrer los datos y llenar las listas de instituciones y sedes
    for row in intercambio_data:
        (correo, nombre_operador, fecha_solicitud, fecha_ejecucion, descripcion,
        numero_intercambio, componente, numero_menu_oficial, menu_oficial,
        numero_menu_intercambio, menu_intercambio, id_sede, id_institucion, justificacion_texto) = row

        if id_institucion not in instituciones:
            instituciones.append(id_institucion)
        if id_sede not in sedes:
            sedes.append(id_sede)

    # Asignar datos generales del intercambio
    datos_generales = {
        'Correo': correo,
        'Nombre Operador': nombre_operador,
        'Fecha Solicitud': fecha_solicitud,
        'Modalidad': descripcion,
        'Numero Intercambio': numero_intercambio,
        'Justificación': justificacion_texto,
        'Instituciones': instituciones,  # Lista de instituciones
        'Sedes': sedes  # Lista de sedes
    }

    # Organizar datos agrupados por fecha
    datos_por_fecha = {}
    for row in intercambio_data:
        (correo, nombre_operador, fecha_solicitud, fecha_ejecucion, 
        descripcion, numero_intercambio, componente, numero_menu_oficial, 
        menu_oficial, numero_menu_intercambio, menu_intercambio, 
        id_sede, id_institucion, justificacion_texto) = row
        
        componentes_separados = [c.strip() for c in componente.split(',')]
        menu_oficial_separados = [m.strip() for m in menu_oficial.split(',')]
        menu_intercambio_separados = [m.strip() for m in menu_intercambio.split(',')]

        fecha_ejecucion_str = str(fecha_ejecucion)
        numero_menu_oficial_str = str(numero_menu_oficial).zfill(2)
        numero_menu_intercambio_str = str(numero_menu_intercambio).zfill(2)

        if fecha_ejecucion_str not in datos_por_fecha:
            datos_por_fecha[fecha_ejecucion_str] = []

        encontrado = False
        for grupo in datos_por_fecha[fecha_ejecucion_str]:
            if (grupo['numero_menu_oficial'] == numero_menu_oficial_str and
                grupo['numero_menu_intercambio'] == numero_menu_intercambio_str):
                for comp, oficial, intercambio in zip(componentes_separados, menu_oficial_separados, menu_intercambio_separados):
                    if comp not in grupo['componentes']:
                        grupo['componentes'].append(comp)
                    if oficial not in grupo['menu_oficial']:
                        grupo['menu_oficial'].append(oficial)
                    if intercambio not in grupo['menu_intercambio']:
                        grupo['menu_intercambio'].append(intercambio)
                encontrado = True
                break

        if not encontrado:
            datos_por_fecha[fecha_ejecucion_str].append({
                'componentes': componentes_separados,
                'menu_oficial': menu_oficial_separados,
                'menu_intercambio': menu_intercambio_separados,
                'numero_menu_oficial': numero_menu_oficial_str,
                'numero_menu_intercambio': numero_menu_intercambio_str
            })

    if request.method == 'POST':
        # Obtener datos del formulario
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        justificacion = request.form.get('justificacion')
        firma_imagenes = request.files.getlist('firma_imagen[]')
        firma_nombres = request.form.getlist('firma_nombre[]')
        firma_cargos = request.form.getlist('firma_cargo[]')

        # Actualizar la base de datos
        cursor.execute("""
            UPDATE intercambios
            SET concepto = 'Aprobado', justificacion_texto = %s
            WHERE numero_intercambio = %s
        """, (justificacion, numero_intercambio))

        # Guardar firmas
        firma_dir = 'static/firmas'
        os.makedirs(firma_dir, exist_ok=True)
        firmas = []
        for imagen, nombre, cargo in zip(firma_imagenes, firma_nombres, firma_cargos):
            if imagen:
                filename = secure_filename(imagen.filename)
                imagen_path = os.path.join(firma_dir, filename)
                imagen.save(imagen_path)
                firmas.append(imagen_path)
                cursor.execute("""
                    INSERT INTO firmas_nutricionistas (correo, nombre, cargo, firma_path)
                    VALUES (%s, %s, %s, %s)
                """, (correo, nombre, cargo, imagen_path))

        # Generar el PDF y enviar el correo
        pdf_path = estado_pdf(datos_generales, datos_por_fecha, firmas, firma_nombres, firma_cargos, justificacion, asunto, mensaje, numero_intercambio)
        if not pdf_path or not os.path.isfile(pdf_path):
            print("Error: No se pudo generar el PDF.")
            return jsonify({'error': 'No se pudo generar el PDF.'}), 500
        
        cursor.execute("""
            SELECT intercambios.id_intercambio
            FROM intercambios
            WHERE numero_intercambio = %s
        """, (numero_intercambio,))
        
        intercambio_id = cursor.fetchone()
        intercambio_id = intercambio_id[0] if intercambio_id else None
        
        if intercambio_id is None:
            print("Error: No se encontró el intercambio asociado.")
            return jsonify({'error': 'No se encontró el intercambio asociado.'}), 404
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM archivos
            WHERE id_intercambio = %s AND tipo_archivo = 'estado'
        """, (intercambio_id,))
        existe_archivo = cursor.fetchone()[0] > 0
        
        print("Guardando PDF en la base de datos...")
        if not existe_archivo:
            cursor.execute("""
                INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                VALUES (%s, %s, %s, %s)
            """, (intercambio_id, f"Aval # {numero_intercambio}.pdf", 'estado', pdf_path))
            print("PDF agregado a la base de datos.")
        else:
            cursor.execute("""
                UPDATE archivos
                SET nombre_archivo = %s, ruta_archivo = %s
                WHERE id_intercambio = %s AND tipo_archivo = 'estado'
            """, (f"Aval # {numero_intercambio}.pdf", pdf_path, intercambio_id))
            print("PDF actualizado en la base de datos.")

        print("PDF guardado en la base de datos de aprobado.")
        
        conn.commit()
        print("Transacción confirmada.")
  
        return redirect(url_for('visitas.estado'))

    cursor.close()
    conn.close()
    
    return render_template('aprobar.html', datos=datos_generales, datos_por_fecha=datos_por_fecha, numero_intercambio=numero_intercambio)

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
import os
from datetime import datetime

def estado_pdf(datos_generales, datos_por_fecha, firma_paths, firma_nombres, firma_cargos, justificacion, asunto, mensaje, numero_intercambio):
    # Crear un archivo temporal para el PDF    
    try:
        pdf_folder_path = os.path.join('static','uploads', 'solicitud_intercambio', 'estado', str(numero_intercambio))
        os.makedirs(pdf_folder_path, exist_ok=True)  # Asegurar que la carpeta exista

        # Definir la ruta completa del archivo PDF
        pdf_path = os.path.join(pdf_folder_path, f"Aval # {numero_intercambio}.pdf")
        
        # Crear el documento para agregar contenido con márgenes de 2.5 cm en todos los lados
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            leftMargin=2.5 * cm,
            rightMargin=2.5 * cm,
            topMargin=1.0 * cm,
            bottomMargin=1.5 * cm
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        conn = get_db_connection('visitas')
        if conn is None:
            print("Error: No se pudo establecer conexión a la base de datos")
            return
        
        cursor = conn.cursor()
        
        # Obtener los nombres de instituciones y sedes
        nombres_instituciones = []
        nombres_sedes = []
        for institucion_id in datos_generales['Instituciones']:
            cursor.execute("""
                SELECT sede_educativa
                FROM instituciones
                WHERE id_institucion = %s
            """, (institucion_id,))
            nombre_institucion = cursor.fetchone()
            if nombre_institucion:
                nombres_instituciones.append(nombre_institucion[0])

        for sede_id in datos_generales['Sedes']:
            cursor.execute("""
                SELECT nombre_sede
                FROM sedes
                WHERE id_sede = %s
            """, (sede_id,))
            nombre_sede = cursor.fetchone()
            if nombre_sede:
                nombres_sedes.append(nombre_sede[0])

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

        # Estilos personalizados
        title_style = ParagraphStyle('title', fontSize=14, leading=16, alignment=1)
        cell_style = ParagraphStyle('cell', fontSize=8, leading=10, alignment=1)  # Alineación centrada en las celdas
        
        # Logo
        logo_path = 'static/images/cali.png'
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"No se encontró el archivo del logo en la ruta: {logo_path}")
        logo = Image(logo_path, width=100, height=70)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
        elements.append(Spacer(1, 12))

        # Encabezado
        elements.append(Paragraph(f"<b>Santiago de Cali, {datetime.now().strftime('%d de %B de %Y')}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Señores", styles['Normal']))
        elements.append(Paragraph(f"{datos_generales['Nombre Operador']}", styles['Normal']))
        elements.append(Paragraph("OPERADOR PAE CALI", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph(f"Asunto: {asunto}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"{mensaje}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Datos generales con nombres de instituciones y sedes
        data_generales = [
            [Paragraph("Modalidad:", styles['Normal']), Paragraph(datos_generales['Modalidad'], styles['Normal'])],
            [Paragraph("Número Intercambio:", styles['Normal']), Paragraph(datos_generales['Numero Intercambio'], styles['Normal'])],
            [Paragraph("Instituciones:", styles['Normal']), Paragraph(", ".join(nombres_instituciones), styles['Normal'])],
            [Paragraph("Sedes:", styles['Normal']), Paragraph(", ".join(nombres_sedes), styles['Normal'])],
        ]

        # Configuración de la tabla
        table_generales = Table(data_generales, colWidths=[120, 330])
        table_generales.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        elements.append(table_generales)
        
        data_justificacion_operador = []
        if justificacion:
            data_justificacion_operador.append([Paragraph("Justificación:", styles['Normal']), Paragraph(justificacion, styles['Normal'])])
        if 'Nombre Operador' in datos_generales:
            operador_texto = f"El operador {datos_generales['Nombre Operador']} entregará a los beneficiarios de derecho."
            data_justificacion_operador.append([Paragraph("Operador:", styles['Normal']), Paragraph(operador_texto, styles['Normal'])])

        # Configuración de la tabla para Justificación y Operador
        if data_justificacion_operador:
            table_just_operador = Table(data_justificacion_operador, colWidths=[120, 330])
            table_just_operador.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            # Agregar tabla al documento
            elements.append(table_just_operador)
            elements.append(Spacer(1, 12))
        
        # Datos por fecha
        for fecha, grupos in datos_por_fecha.items():
            # Convertir la fecha a un formato legible antes de agregarla al PDF
            if fecha is None:
                formatted_fecha = "None"
            else:
                try:
                    # Validar que la fecha tenga el formato correcto
                    formatted_fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d - %B - %Y")
                except ValueError:
                    formatted_fecha = "Fecha inválida"
            
            elements.append(Paragraph(f"Fecha Ejecución: {formatted_fecha}", styles['Heading2']))

            elements.append(Spacer(1, 6))

            for grupo in grupos:
                # Configuración de la tabla
                data_componentes = [
                    ["Componente", f"Menú Oficial: {grupo['numero_menu_oficial']}", f"Menú Intercambio: {grupo['numero_menu_intercambio']}"]
                ]

                # Añadir cada fila de componentes, menú oficial e intercambio
                for componente, menu_oficial, menu_intercambio in zip(grupo['componentes'], grupo['menu_oficial'], grupo['menu_intercambio']):
                    data_componentes.append([
                        Paragraph(componente, cell_style),
                        Paragraph(menu_oficial, cell_style),
                        Paragraph(menu_intercambio, cell_style)
                    ])

                # Crear la tabla con anchos ajustados
                table_componentes = Table(data_componentes, colWidths=[150, 150, 150])
                table_componentes.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                ]))

                elements.append(table_componentes)
                elements.append(Spacer(1, 12))

        # Firmas
        elements.append(Spacer(1, 12))

        # Crear una tabla para las firmas
        firmas_data = []
        row = []

        # Iterar por las firmas
        for i, (firma_path, nombre, cargo) in enumerate(zip(firma_paths, firma_nombres, firma_cargos)):
            # Crear la celda con la imagen y los detalles
            image = Image(firma_path, width=100, height=50)
            image.hAlign = 'LEFT'
            
            # Contenido de la celda
            cell_content = [
                image,
                Paragraph(f"Nombre: {nombre}", styles['Normal']),
                Paragraph(f"Cargo: {cargo}", styles['Normal']),
                Paragraph("Secretaría de Educación Distrital", styles['Normal']),
            ]
            
            # Añadir contenido a la fila
            row.append(cell_content)
            
            # Cada 2 firmas, crear una nueva fila
            if (i + 1) % 2 == 0:
                firmas_data.append(row)
                row = []

        # Si hay firmas restantes, añadir la última fila
        if row:
            firmas_data.append(row)

        # Crear la tabla de firmas
        firmas_table = Table(firmas_data, colWidths=[250, 250])  # Ajustar el ancho de las columnas
        firmas_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            # ('BOX', (0, 0), (-1, -1), 0.0, colors.grey),
            # ('INNERGRID', (0, 0), (-1, -1), 0.0, colors.grey),
        ]))

        # Añadir la tabla al documento
        elements.append(firmas_table)
        # Generar el PDF con todos los elementos añadidos
        doc.build(elements)
        print(f"PDF generado en: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None


#NEGAR
@visitas.route('/negar/<string:numero_intercambio>', methods=['GET', 'POST'])
@login_required
@role_required('nutricionista', 'administrador')
def negar(numero_intercambio):
    conn = get_db_connection('visitas')
    if conn is None:
        return "Error al conectar a la base de datos.", 500

    cursor = conn.cursor()

    # Obtener los datos de intercambio en ambos métodos
    cursor.execute("""
        SELECT intercambios.correo_operador, operadores.nombre AS nombre_operador,
            intercambios.fecha_solicitud, detalles_menu.fecha_ejecucion,
            tiporacion.descripcion, intercambios.numero_intercambio,
            detalles_menu.componente, detalles_menu.numero_menu_oficial,
            detalles_menu.menu_oficial, detalles_menu.numero_menu_intercambio,
            detalles_menu.menu_intercambio, instituciones_sedes.id_sede, 
            instituciones_sedes.id_institucion, intercambios.justificacion_texto
        FROM intercambios
        INNER JOIN instituciones_sedes 
            ON intercambios.id_intercambio = instituciones_sedes.id_intercambio
        INNER JOIN detalles_menu 
            ON intercambios.id_intercambio = detalles_menu.id_intercambio
        INNER JOIN operadores 
            ON intercambios.id_operador = operadores.id_operador
        INNER JOIN tiporacion 
            ON intercambios.id_tipo_racion = tiporacion.id_tipo_racion 
        WHERE intercambios.numero_intercambio = %s
    """, (numero_intercambio,))

    intercambio_data = cursor.fetchall()
    if not intercambio_data:
        return "Intercambio no encontrado.", 404

    # Inicializar listas para instituciones y sedes
    instituciones = []
    sedes = []

    # Recorrer los datos y llenar las listas de instituciones y sedes
    for row in intercambio_data:
        (correo, nombre_operador, fecha_solicitud, fecha_ejecucion, descripcion,
        numero_intercambio, componente, numero_menu_oficial, menu_oficial,
        numero_menu_intercambio, menu_intercambio, id_sede, id_institucion, justificacion_texto) = row

        if id_institucion not in instituciones:
            instituciones.append(id_institucion)
        if id_sede not in sedes:
            sedes.append(id_sede)

    # Asignar datos generales del intercambio
    datos_generales = {
        'Correo': correo,
        'Nombre Operador': nombre_operador,
        'Fecha Solicitud': fecha_solicitud,
        'Modalidad': descripcion,
        'Numero Intercambio': numero_intercambio,
        'Justificación': justificacion_texto,
        'Instituciones': instituciones,  # Lista de instituciones
        'Sedes': sedes  # Lista de sedes
    }

    # Organizar datos agrupados por fecha
    datos_por_fecha = {}
    for row in intercambio_data:
        (correo, nombre_operador, fecha_solicitud, fecha_ejecucion, 
        descripcion, numero_intercambio, componente, numero_menu_oficial, 
        menu_oficial, numero_menu_intercambio, menu_intercambio, 
        id_sede, id_institucion, justificacion_texto) = row
        
        componentes_separados = [c.strip() for c in componente.split(',')]
        menu_oficial_separados = [m.strip() for m in menu_oficial.split(',')]
        menu_intercambio_separados = [m.strip() for m in menu_intercambio.split(',')]

        fecha_ejecucion_str = str(fecha_ejecucion)
        numero_menu_oficial_str = str(numero_menu_oficial).zfill(2)
        numero_menu_intercambio_str = str(numero_menu_intercambio).zfill(2)

        if fecha_ejecucion_str not in datos_por_fecha:
            datos_por_fecha[fecha_ejecucion_str] = []

        encontrado = False
        for grupo in datos_por_fecha[fecha_ejecucion_str]:
            if (grupo['numero_menu_oficial'] == numero_menu_oficial_str and
                grupo['numero_menu_intercambio'] == numero_menu_intercambio_str):
                for comp, oficial, intercambio in zip(componentes_separados, menu_oficial_separados, menu_intercambio_separados):
                    if comp not in grupo['componentes']:
                        grupo['componentes'].append(comp)
                    if oficial not in grupo['menu_oficial']:
                        grupo['menu_oficial'].append(oficial)
                    if intercambio not in grupo['menu_intercambio']:
                        grupo['menu_intercambio'].append(intercambio)
                encontrado = True
                break

        if not encontrado:
            datos_por_fecha[fecha_ejecucion_str].append({
                'componentes': componentes_separados,
                'menu_oficial': menu_oficial_separados,
                'menu_intercambio': menu_intercambio_separados,
                'numero_menu_oficial': numero_menu_oficial_str,
                'numero_menu_intercambio': numero_menu_intercambio_str
            })

    if request.method == 'POST':
        # Obtener datos del formulario
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')
        justificacion = request.form.get('justificacion')
        firma_imagenes = request.files.getlist('firma_imagen[]')
        firma_nombres = request.form.getlist('firma_nombre[]')
        firma_cargos = request.form.getlist('firma_cargo[]')

        # Actualizar la base de datos
        cursor.execute("""
            UPDATE intercambios
            SET concepto = 'Negado', justificacion_texto = %s, mensaje = %s, asunto = %s
            WHERE numero_intercambio = %s
        """, (justificacion, mensaje, asunto, numero_intercambio))

        # Guardar firmas
        firma_dir = 'static/firmas'
        os.makedirs(firma_dir, exist_ok=True)
        firmas = []
        for imagen, nombre, cargo in zip(firma_imagenes, firma_nombres, firma_cargos):
            if imagen:
                filename = secure_filename(imagen.filename)
                imagen_path = os.path.join(firma_dir, filename)
                imagen.save(imagen_path)
                firmas.append(imagen_path)
                cursor.execute("""
                    INSERT INTO firmas_nutricionistas (correo, nombre, cargo, firma_path)
                    VALUES (%s, %s, %s, %s)
                """, (correo, nombre, cargo, imagen_path))

        # Generar el PDF y enviar el correo
        pdf_path = estado_pdf(datos_generales, datos_por_fecha, firmas, firma_nombres, firma_cargos, justificacion, asunto, mensaje, numero_intercambio)
        if not pdf_path or not os.path.isfile(pdf_path):
            print("Error: No se pudo generar el PDF.")
            return jsonify({'error': 'No se pudo generar el PDF.'}), 500
        
        cursor.execute("""
            SELECT intercambios.id_intercambio
            FROM intercambios
            WHERE numero_intercambio = %s
        """, (numero_intercambio,))
        
        intercambio_id = cursor.fetchone()
        intercambio_id = intercambio_id[0] if intercambio_id else None
        
        if intercambio_id is None:
            print("Error: No se encontró el intercambio asociado.")
            return jsonify({'error': 'No se encontró el intercambio asociado.'}), 404
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM archivos
            WHERE id_intercambio = %s AND tipo_archivo = 'estado'
        """, (intercambio_id,))
        existe_archivo = cursor.fetchone()[0] > 0
        
        print("Guardando PDF en la base de datos...")
        if not existe_archivo:
            cursor.execute("""
                INSERT INTO archivos (id_intercambio, nombre_archivo, tipo_archivo, ruta_archivo)
                VALUES (%s, %s, %s, %s)
            """, (intercambio_id, f"Aval # {numero_intercambio}.pdf", 'estado', pdf_path))
            print("PDF agregado a la base de datos.")
        else:
            cursor.execute("""
                UPDATE archivos
                SET nombre_archivo = %s, ruta_archivo = %s
                WHERE id_intercambio = %s AND tipo_archivo = 'estado'
            """, (f"Aval # {numero_intercambio}.pdf", pdf_path, intercambio_id))
            print("PDF actualizado en la base de datos.")

        print("PDF guardado en la base de datos de aprobado.")
        
        conn.commit()
        print("Transacción confirmada.")
  
        return redirect(url_for('visitas.estado'))

    cursor.close()
    conn.close()
    
    return render_template('negar.html', datos=datos_generales, datos_por_fecha=datos_por_fecha, numero_intercambio=numero_intercambio)

@visitas.route('/get_menus')
def get_menus():
    tipo_racion_id = request.args.get('tipo_racion')
    
    # Verificar si se ha proporcionado el tipo de ración
    if not tipo_racion_id:
        return jsonify({'error': 'Falta el parámetro tipo_racion'}), 400
    
    # Definir la consulta base dependiendo del tipo de ración
    query = """
    SELECT DISTINCT numero_menu
    FROM (
        SELECT numero_menu FROM industrializado WHERE id_tipo_racion = %s
        UNION
        SELECT numero_menu FROM preparadoensitioam WHERE id_tipo_racion = %s
        UNION
        SELECT numero_menu FROM preparadoensitiopm WHERE id_tipo_racion = %s
        UNION
        SELECT numero_menu FROM jornadaunica WHERE id_tipo_racion = %s
    ) AS menus
    """

    # Conectar a la base de datos
    conn = get_db_connection('visitas')
    if conn is None:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    cursor = conn.cursor()

    try:
        # Ejecutar la consulta
        cursor.execute(query, (tipo_racion_id, tipo_racion_id, tipo_racion_id, tipo_racion_id))
        menus = cursor.fetchall()
        
        # Devolver la lista de menús en formato JSON
        return jsonify([{'numero_menu': menu[0]} for menu in menus])

    except Exception as e:
        print(f"Error al obtener los menús: {e}")
        return jsonify({'error': 'Error al ejecutar la consulta'}), 500

    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()


@visitas.route('/get_menu_details')
def get_menu_details():
    tipo_racion_id = request.args.get('tipo_racion')
    numero_menu_oficial = request.args.get('numero_menu_oficial')
    numero_menu_intercambio = request.args.get('numero_menu_intercambio')
    justificacion = request.args.get('justificacion')

    # Imprimir todos los datos solicitados
    print(f"tipo_racion_id: {tipo_racion_id}, numero_menu_oficial: {numero_menu_oficial}, numero_menu_intercambio: {numero_menu_intercambio}, justificacion: {justificacion}")

    # Verificar si los parámetros necesarios están presentes
    if not numero_menu_oficial and not numero_menu_intercambio:
        return jsonify({'error': 'Debe proporcionar al menos un número de menú oficial o de intercambio'}), 400

    conn = get_db_connection('visitas')
    if conn is None:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    cursor = conn.cursor()

    try:
        # Consulta para obtener detalles del menú oficial
        menu_oficial = []
        if numero_menu_oficial:
            query_oficial = """
            SELECT componentes, ingredientes 
            FROM (
                SELECT componentes, ingredientes FROM industrializado 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitioam 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitiopm 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM jornadaunica 
                WHERE id_tipo_racion = %s AND numero_menu = %s
            ) AS menu_oficial
            """
            cursor.execute(query_oficial, (tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial))
            menu_oficial = cursor.fetchall()
            
            print(f"Menu Oficial: {menu_oficial}")

        # Consulta para obtener detalles del menú de intercambio
        menu_intercambio = []
        if numero_menu_intercambio:
            if justificacion == "Cambio Modalidad":  # Solo permitir para "Industrializado"
                query_intercambio = """
                SELECT componentes, ingredientes 
                FROM industrializado 
                WHERE id_tipo_racion = 1 AND numero_menu = %s
                """
                cursor.execute(query_intercambio, (numero_menu_intercambio,))
                menu_intercambio = cursor.fetchall()
                print(f"Menu Intercambio: {menu_intercambio}")
            else:
                # Otras justificaciones ("Cancelación de Clases", "Escasez", "Otros") para cualquier ración
                query_intercambio = """
                SELECT componentes, ingredientes 
                FROM (
                    SELECT componentes, ingredientes FROM industrializado 
                    WHERE id_tipo_racion = %s AND numero_menu = %s
                    UNION ALL
                    SELECT componentes, ingredientes FROM preparadoensitioam 
                    WHERE id_tipo_racion = %s AND numero_menu = %s
                    UNION ALL
                    SELECT componentes, ingredientes FROM preparadoensitiopm 
                    WHERE id_tipo_racion = %s AND numero_menu = %s
                    UNION ALL
                    SELECT componentes, ingredientes FROM jornadaunica 
                    WHERE id_tipo_racion = %s AND numero_menu = %s
                ) AS menu_intercambio
                """
                cursor.execute(query_intercambio, (tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio))
                menu_intercambio = cursor.fetchall()
                print(f"Menu Intercambio: {menu_intercambio}")


        # Asegúrate de que las listas no estén vacías
        if not menu_oficial and not menu_intercambio:
            return jsonify({'error': 'No se encontraron menús para los parámetros proporcionados'}), 404        
        # Formatear la respuesta
        return jsonify({
            'menu_oficial': [{'componentes': row[0], 'ingredientes': row[1]} for row in menu_oficial],
            'menu_intercambio': [{'componentes': row[0], 'ingredientes': row[1]} for row in menu_intercambio] if menu_intercambio else []
        })

    except Exception as e:
        print(f"Error: {e}")  # Mostrar error en la terminal
        return jsonify({'error': 'Error al ejecutar la consulta'}), 500

    finally:
        cursor.close()
        conn.close()
        
@visitas.route('/get_menu_details_verificacion')
def get_menu_details_verificacion():
    tipo_racion_id = request.args.get('tipo_racion')
    numero_menu_oficial = request.args.get('numero_menu_oficial')
    numero_menu_intercambio = request.args.get('numero_menu_intercambio')

    # Imprimir todos los datos solicitados
    print(f"tipo_racion_id: {tipo_racion_id}, numero_menu_oficial: {numero_menu_oficial}, numero_menu_intercambio: {numero_menu_intercambio}")

    # Verificar si los parámetros necesarios están presentes
    # if not numero_menu_oficial and not numero_menu_intercambio:
    #     return jsonify({'error': 'Debe proporcionar al menos un número de menú oficial o de intercambio'}), 400

    conn = get_db_connection('visitas')
    if conn is None:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500

    cursor = conn.cursor()

    try:
        # Consulta para obtener detalles del menú oficial
        menu_oficial = []
        if numero_menu_oficial:
            query_oficial = """
            SELECT componentes, ingredientes 
            FROM (
                SELECT componentes, ingredientes FROM industrializado 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitioam 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitiopm 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM jornadaunica 
                WHERE id_tipo_racion = %s AND numero_menu = %s
            ) AS menu_oficial
            """
            cursor.execute(query_oficial, (tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial, tipo_racion_id, numero_menu_oficial))
            menu_oficial = cursor.fetchall()
            
            print(f"Menu Oficial: {menu_oficial}")

        # Consulta para obtener detalles del menú de intercambio
        menu_intercambio = []
        if numero_menu_intercambio:
            
            query_intercambio = """
            SELECT componentes, ingredientes 
            FROM (
                SELECT componentes, ingredientes FROM industrializado 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitioam 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM preparadoensitiopm 
                WHERE id_tipo_racion = %s AND numero_menu = %s
                UNION ALL
                SELECT componentes, ingredientes FROM jornadaunica 
                WHERE id_tipo_racion = %s AND numero_menu = %s
            ) AS menu_intercambio
            """
            cursor.execute(query_intercambio, (tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio, tipo_racion_id, numero_menu_intercambio))
            menu_intercambio = cursor.fetchall()
            print(f"Intercambios: {tipo_racion_id}")
            print(f"Menu Intercambio: {menu_intercambio}")


        # Asegúrate de que las listas no estén vacías
        # if not menu_oficial and not menu_intercambio:
        #     return jsonify({'error': 'No se encontraron menús para los parámetros proporcionados'}), 404        
        # Formatear la respuesta
        return jsonify({
            'menu_oficial': [{'componentes': row[0], 'ingredientes': row[1]} for row in menu_oficial],
            'menu_intercambio': [{'componentes': row[0], 'ingredientes': row[1]} for row in menu_intercambio] if menu_intercambio else []
        })

    except Exception as e:
        print(f"Error: {e}")  # Mostrar error en la terminal
        return jsonify({'error': 'Error al ejecutar la consulta'}), 500

    finally:
        cursor.close()
        conn.close()


@visitas.route('/')
def index():
    user_role = session.get('rol')
    return render_template('index.html', user_role=user_role)

# Ruta para el menú principal después de iniciar sesión
@visitas.route('/indexprincipal')
def indexprincipal():
    usuario = session.get('usuario')
    correo = session.get('correo')
    rol = session.get('rol')
    return render_template('indexprincipal.html', usuario=usuario, correo=correo, rol=rol)

# Ruta para cerrar sesión
@visitas.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('correo', None)
    session.pop('rol', None)
    return redirect(url_for('index'))

@visitas.route('/informe_general')
@login_required
def informe_general():
    print("Accediendo a informe_general")
    return render_template('informe_general.html', rol=session.get('rol'), usuario=session.get('nombre'))

@visitas.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


# Registramos los Blueprints

visitas.register_blueprint(bodega_bp)
visitas.register_blueprint(tecnica_bp)
visitas.register_blueprint(visitas_bp)
visitas.register_blueprint(iniciasesion_bp)
visitas.register_blueprint(infraestructura_bp)
visitas.register_blueprint(menus_bp)
visitas.register_blueprint(actualizar_bp)
visitas.register_blueprint(verificacion_bp)
visitas.register_blueprint(instituciones_bp)
visitas.register_blueprint(sedes_bp)

if __name__ == '__main__':
    visitas.run(host="0.0.0.0", port=5001, debug=True)
