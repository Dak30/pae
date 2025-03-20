from flask import Blueprint, render_template, request, redirect, flash
from iniciasesion import login_required, session, registrar_auditoria
from mysql.connector import Error
from database import get_db_connection
from collections import defaultdict
from datetime import datetime


menus_bp = Blueprint('menus_bp', __name__, template_folder='templates/menus')


menu_type_titles = {
    "jornadaunica": "Jornada Única",
    "preparadoensitioam": "Preparado en Sitio AM",
    "preparadoensitiopm": "Preparado en Sitio PM",
    "industrializado": "Industrializado"
}

@menus_bp.route('/index_update')
@login_required
def index_update():
    print("Accediendo a Actualizar")
    usuario_sesion = session.get('usuario_id')
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

    registrar_auditoria(
        usuario_id=usuario_sesion if usuario_sesion else 0,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="QUERY",
        modulo="Gestión de Ciclo de Menú",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) accesó la ventana de Ciclo de Menú",
    )
    return render_template('index_update.html', rol=session.get('rol'), usuario=session.get('nombre'))

@menus_bp.route('/update_menu/<menu_type>', methods=['GET', 'POST'])
@login_required
def update_menu(menu_type):
    # Verificar roles permitidos
    rol = session.get('rol')
    if rol not in ['administrador', 'nutricionista']:
        flash("No tienes permiso para acceder a esta página.", "error")
        return redirect('/')

    # Conexión a la base de datos
    conn = get_db_connection("visitas", driver="mysql.connector")
    if not conn:
        flash("No se pudo conectar a la base de datos", "error")
        return redirect('/')

    cursor = conn.cursor(dictionary=True)
    title = menu_type_titles.get(menu_type, "Actualizar Menús")
    
    id_column_map = {
        "jornadaunica": "id_jornada_unica",
        "preparadoensitioam": "id_preparado_sitio_am",
        "preparadoensitiopm": "id_preparado_sitio_pm",
        "industrializado": "id_industrializado"
    }
    id_column = id_column_map.get(menu_type)
    if not id_column:
        flash("Tipo de menú no válido", "error")
        return redirect('/')

    if request.method == 'POST':
        cambios_realizados = []  # Para almacenar detalles de los cambios

        for key, value in request.form.items():
            if key.startswith("ingrediente_"):
                id_value = key.split("_")[1]
                ingrediente_nuevo = value.strip()  # Limpia espacios en blanco

                # Obtener el valor anterior, componente y número de menú
                select_query = f"""
                SELECT ingredientes, componentes, numero_menu 
                FROM {menu_type} 
                WHERE {id_column} = %s
                """
                cursor.execute(select_query, (id_value,))
                resultado = cursor.fetchone()
                ingrediente_anterior = resultado['ingredientes'].strip() if resultado and resultado['ingredientes'] else None
                componente = resultado['componentes'] if resultado else None
                numero_menu = resultado['numero_menu'] if resultado else None

                # Verificar si hay un cambio antes de actualizar y guardar en el historial
                if ingrediente_anterior != ingrediente_nuevo:
                    # Actualizar el registro
                    update_query = f"UPDATE {menu_type} SET ingredientes = %s WHERE {id_column} = %s"
                    cursor.execute(update_query, (ingrediente_nuevo, id_value))

                    # Insertar en el historial de cambios
                    historial_query = """
                    INSERT INTO historial_cambios (modalidad, id_racion, componente, numero_menu, valor_anterior, valor_nuevo, actualizado_por, fecha_actualizacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(historial_query, (
                        menu_type,
                        id_value,
                        componente,
                        numero_menu,
                        ingrediente_anterior,
                        ingrediente_nuevo,
                        session.get('nombre'),  # Usuario que realizó la actualización
                        datetime.now()
                    ))

                    # Agregar cambio a la lista para la auditoría
                    cambios_realizados.append(
                        f"Componente '{componente}', Menú {numero_menu}: '{ingrediente_anterior}' → '{ingrediente_nuevo}'"
                    )

        conn.commit()

        # Registrar auditoría si hubo cambios
        if cambios_realizados:
            usuario_sesion = session.get('usuario_id', 0)
            nombre_sesion = session.get('nombre', 'Desconocido')
            correo_sesion = session.get('correo', 'Sin correo')

            registrar_auditoria(
                usuario_id=usuario_sesion,
                nombre_usuario=nombre_sesion,
                correo=correo_sesion,
                accion="UPDATE",
                modulo="Gestión de Menús",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó los siguientes menus en '{menu_type}': {', '.join(cambios_realizados)}",
            )

        flash("Datos actualizados correctamente.", "success")
        return redirect(f'/update_menu/{menu_type}')

    query = f"""
    SELECT semana, {id_column} AS id, numero_menu, componentes, ingredientes
    FROM {menu_type}
    ORDER BY semana, numero_menu
    """
    cursor.execute(query)
    data = cursor.fetchall()

    rows = {}
    for row in data:
        week = row['semana']
        componente = row['componentes']
        if week not in rows:
            rows[week] = defaultdict(list)
        rows[week][componente].append({
            'id': row['id'],
            'ingrediente': row['ingredientes'],
            'numero_menu': row['numero_menu']
        })

    conn.close()

    return render_template(
        'menu_update.html',
        menu_type=menu_type,
        title=title,
        rows=rows,
        id_column=id_column,
        rol=rol,
        usuario=session.get('nombre')
    )



@menus_bp.route('/historial_cambios', methods=['GET'])
@login_required
def historial_cambios():
    """
    Muestra el historial completo de todos los menús.
    """
    # Verificar el rol del usuario
    rol = session.get('rol')
    if rol not in ['administrador', 'nutricionista']:
        flash("No tienes permiso para acceder a esta página.", "error")
        return redirect('/')

    # Conexión a la base de datos
    conn = get_db_connection("visitas", driver="mysql.connector")
    if not conn:
        flash("No se pudo conectar a la base de datos", "error")
        return redirect('/')

    cursor = conn.cursor(dictionary=True)
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Add a WHERE clause to the SQL query if dates are provided
    where_clause = ""
    if start_date and end_date:
        where_clause = f"WHERE fecha_actualizacion BETWEEN '{start_date}' AND '{end_date}'"

    # Consultar el historial completo
    query = f"""
    SELECT modalidad, id_racion, componente, numero_menu, valor_anterior, valor_nuevo, actualizado_por, fecha_actualizacion
    FROM historial_cambios
    {where_clause}
    ORDER BY fecha_actualizacion DESC
    """
    cursor.execute(query)
    historial = cursor.fetchall()

    # Mapeo de modalidades a nombres más legibles
    modalidad_map = {
        "preparadoensitiopm": "Preparado en Sitio PM",
        "preparadoensitioam": "Preparado en Sitio AM",
        "jornadaunica": "Jornada Única",
        "industrializado": "Industrializado"
    }

    # Aplicar el mapeo al historial
    for cambio in historial:
        cambio['modalidad'] = modalidad_map.get(cambio['modalidad'], cambio['modalidad'])  # Dejar el valor original si no hay mapeo

    # Cerrar la conexión
    cursor.close()
    conn.close()
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="QUERY",
        modulo="Gestión de Menús",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó la ventana de historial de menus cambios",
    )

    # Renderizar la plantilla con el historial completo
    return render_template(
        'historial_cambios.html',
        historial=historial,
        rol=rol,
        usuario=session.get('nombre')
    )

from flask import send_file
import openpyxl
import os

@menus_bp.route('/exportar_historico_excel', methods=['GET'])
@login_required
def exportar_historico_excel():
    # Obtener fechas de inicio y fin de los parámetros GET
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Validar las fechas
    if not start_date or not end_date:
        flash("Debe proporcionar una fecha de inicio y una fecha de fin para filtrar el historial.", "error")
        return redirect('/historial_cambios')

    # Conexión a la base de datos
    conn = get_db_connection("visitas", driver="mysql.connector")
    cursor = conn.cursor()

    # Consulta para obtener los datos filtrados
    query = """
        SELECT 
            modalidad, componente, numero_menu, valor_anterior, valor_nuevo, actualizado_por, fecha_actualizacion
        FROM historial_cambios
        WHERE fecha_actualizacion BETWEEN %s AND %s
        ORDER BY fecha_actualizacion DESC
    """
    cursor.execute(query, (start_date, end_date))
    cambios = cursor.fetchall()

    # Diccionario de mapeo para modalidad
    modalidad_map = {
        "preparadoensitiopm": "Preparado en Sitio PM",
        "preparadoensitioam": "Preparado en Sitio AM",
        "jornadaunica": "Jornada Única",
        "industrializado": "Industrializado"
    }

    # Crear archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial de Cambios"

    # Agregar encabezados
    headers = [
        "Modalidad", "Componente", "Número de Menú", 
        "Preparación/Alimento Anterior", "Preparación/Alimento Nuevo", 
        "Actualizado Por", "Fecha de Actualización"
    ]
    ws.append(headers)

    # Transformar y agregar datos al Excel
    for cambio in cambios:
        modalidad = modalidad_map.get(cambio[0], cambio[0])  # Mapea el valor de modalidad
        fila = [
            modalidad, cambio[1], cambio[2], 
            cambio[3], cambio[4], cambio[5], cambio[6]
        ]
        ws.append(fila)

    # Guardar archivo temporalmente
    file_path = os.path.join("static", "historial_cambios.xlsx")
    wb.save(file_path)
    cursor.close()
    conn.close()

    # Obtener fecha actual y formatearla
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")  # Formato: Año-Mes-Día
    
    usuario_sesion = session.get('usuario_id', 0)
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')

    registrar_auditoria(
        usuario_id=usuario_sesion,
        nombre_usuario=nombre_sesion,
        correo=correo_sesion,
        accion="DONWLOAD",
        modulo="Gestión de Menús",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) descargó un archivo Excel de la historia de menus cambios",
    )
    # Enviar archivo al cliente con la fecha en el nombre
    return send_file(file_path, as_attachment=True, download_name=f"Historial_Cambios_{fecha_hoy}.xlsx")



