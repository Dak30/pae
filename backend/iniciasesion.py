from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify, make_response, Response, g
from functools import wraps
from flask_bcrypt import Bcrypt
from mysql.connector import Error
import os
from base_datos.database import get_db_connection
from datetime import datetime
import pytz
import secrets


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))  # Usa una clave secreta de entorno

bcrypt = Bcrypt(app)

# Crear el Blueprint
iniciasesion_bp = Blueprint('iniciasesion_bp', __name__, template_folder='templates/usuarios')


tz_colombia = pytz.timezone('America/Bogota')
fecha_colombia = datetime.now(tz_colombia).strftime('%Y-%m-%d %H:%M:%S')


# Obtener operadores de la base de datos
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
        
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session or session['usuario_id'] is None:
            flash('Por favor inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))

        user_ip = request.remote_addr  # Obtener IP del usuario
        if not es_red_interna(user_ip):
            flash('Acceso restringido solo desde la red interna.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))

        rol = session.get('rol')
        if rol not in ['supervisor', 'nutricionista', 'administrador'] and session.get('id_operador') is None:
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))

        return f(*args, **kwargs)
    return decorated_function





def supervisor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'supervisor':
            print("Acceso denegado. Usuario sin rol de supervisor.")
            flash('Acceso no autorizado. Solo supervisores pueden acceder.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))  # Cambiado
        print("Acceso concedido. Usuario con rol de supervisor.")
        return f(*args, **kwargs)
    return decorated_function

def operador_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'operador':
            flash('Acceso no autorizado. Solo operadores pueden acceder a esta página.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))  # Cambiado
        return f(*args, **kwargs)
    return decorated_function

def nutricionista_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'nutricionista':
            print("Acceso denegado. Usuario sin rol de nutricionista.")
            flash('Acceso no autorizado. Solo nutricionista pueden acceder.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))  # Cambiado
        print("Acceso concedido. Usuario con rol de nutricionista.")
        return f(*args, **kwargs)
    return decorated_function

def administrador_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        # Verificar si el usuario está autenticado y es administrador
        if session.get('rol') != 'administrador':
            flash('Acceso denegado. Solo los administradores pueden acceder.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))
        return f(*args, **kwargs)
    return wrapped_function

# Ruta para el registro de usuarios
@iniciasesion_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@administrador_required
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form.get('contrasena')
        rol = request.form['rol']
        id_operador = request.form.get('id_operador', None)

        # Si el rol no está relacionado con un operador, el id_operador será nulo
        if rol in ['supervisor', 'nutricionista']:
            id_operador = None

        # Generar el hash de la contraseña
        if not contrasena:
            flash('La contraseña es obligatoria.', 'error')
            return redirect(url_for('iniciasesion_bp.registro'))

        contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        # Datos del administrador que realiza el registro
        admin_id = session.get('usuario_id')
        print(f'Usuario ID:{admin_id}')

        # Conexión a la base de datos
        conn = get_db_connection('visitas')
        if conn is None:
            flash('Error al conectar con la base de datos.', 'error')
            return render_template('registro.html')

        cursor = conn.cursor()
        try:
            # Insertar el nuevo usuario (sin especificar id_usuario para respetar AUTO_INCREMENT)
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol, id_operador) VALUES (%s, %s, %s, %s, %s)",
                (nombre, correo, contrasena_hash, rol, id_operador)
            )
            conn.commit()  # Confirmar inserción antes de obtener el ID
            
            # Registrar en auditoría
            registrar_auditoria(
                usuario_id=admin_id,
                nombre_usuario=session.get('nombre'),
                correo=session.get('correo'),
                accion="INSERT",
                modulo="Gestión de Usuarios",
                detalle_accion=f"Administrador creó usuario '{nombre}' y correo '{correo}'"
            )

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('iniciasesion_bp.dashboard_administrador'))
        except Error as e:
            print(f"Error al registrar el usuario: {e}")
            flash('Error al registrar el usuario. Verifica si el correo ya existe.', 'error')
        finally:
            cursor.close()
            conn.close()

    # Obtener la lista de operadores
    operadores = fetch_operador()
    return render_template('registro.html', operadores=operadores)


import ipaddress

# 🔹 Definir rangos de IP permitidos
RED_INTERNA = [
    ipaddress.ip_network("192.168.1.0/24"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("127.0.0.0/8")
]

def es_red_interna(ip):
    """ Verifica si la IP pertenece a la red interna """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return any(ip_obj in red for red in RED_INTERNA)
    except ValueError:
        return False  # Si la IP no es válida, se considera externa

@iniciasesion_bp.before_request
def generar_nonce():
    g.nonce = secrets.token_urlsafe(16)  # Genera una sola vez por request



@iniciasesion_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        
        if request.method == 'POST':
            correo = request.form.get('correo')
            contrasena = request.form.get('contrasena')
            user_ip = request.remote_addr  

            if not correo or not contrasena:
                return jsonify({'success': False, 'message': 'Correo y contraseña son obligatorios.'}), 400

            with get_db_connection('visitas') as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
                    usuario = cursor.fetchone()

                    if not usuario:
                        registrar_auditoria(None, None, correo, "INTENTO FALLIDO", "Gestión de Usuarios",
                                            f"Intento de inicio de sesión con usuario no registrado ({correo})")
                        return jsonify({'success': False, 'message': 'Usuario no encontrado.'}), 401

                    if usuario['rol'] == 'administrador' and not es_red_interna(user_ip):
                        registrar_auditoria(usuario['id_usuario'], usuario['nombre'], correo, "ACCESO SOSPECHOSO",
                                            "Gestión de Usuarios",
                                            f"Intento de inicio de sesión de administrador desde IP externa {user_ip}")

                    intentos_fallidos = usuario.get('intentos_fallidos', 0)
                    if intentos_fallidos >= 3:
                        registrar_auditoria(usuario['id_usuario'], usuario['nombre'], correo, "CUENTA BLOQUEADA",
                                            "Gestión de Usuarios",
                                            f"Cuenta bloqueada por intentos fallidos ({correo})")
                        return jsonify({'success': False, 'message': 'Cuenta bloqueada. Contacte al administrador.'}), 403

                    if not usuario['habilitar_acceso']:
                        return jsonify({'success': False, 'message': 'Su cuenta está inhabilitada. Contacte al administrador.'}), 403

                    # Verificar la contraseña usando bcrypt
                    if not bcrypt.check_password_hash(usuario['contrasena'], contrasena):
                        intentos_fallidos += 1
                        cursor.execute("UPDATE usuarios SET intentos_fallidos = %s WHERE correo = %s",
                                       (intentos_fallidos, correo))
                        conn.commit()

                        message = 'Cuenta bloqueada por intentos fallidos. Contacte al administrador.' if intentos_fallidos >= 3 else f'Contraseña incorrecta. Intento {intentos_fallidos}/3.'
                        
                        registrar_auditoria(usuario['id_usuario'], usuario['nombre'], correo, "INTENTO FALLIDO",
                                            "Gestión de Usuarios",
                                            f"Contraseña incorrecta (Intento {intentos_fallidos}/3) con el usuario {usuario['nombre']}.")
                        
                        return jsonify({'success': False, 'message': message}), 401

                    # Obtener la fecha en Colombia (UTC-5)
                    tz_colombia = pytz.timezone('America/Bogota')
                    fecha_colombia = datetime.now(tz_colombia).strftime('%Y-%m-%d %H:%M:%S')

                    cursor.execute("UPDATE usuarios SET fecha_ingreso = %s, intentos_fallidos = 0 WHERE correo = %s",
                                   (fecha_colombia, correo))
                    conn.commit()

                    session.clear()
                    session.update({
                        'usuario_id': usuario['id_usuario'],
                        'nombre': usuario['nombre'],
                        'correo': usuario['correo'],
                        'rol': usuario['rol'],
                        'id_operador': usuario.get('id_operador', None)
                    })

                    registrar_auditoria(session.get('usuario_id'), session.get('nombre'), session.get('correo'), "LOGIN",
                                        "Gestión de Usuarios",
                                        f"Inicio de sesión exitoso para '{session.get('nombre')}' ({correo})")

                    return jsonify({'success': True, 'message': 'Inicio de sesión exitoso.',
                                    'redirect': url_for(f"iniciasesion_bp.dashboard_{usuario['rol']}")})

        return render_template('iniciarsesion.html', nonce=g.nonce)

    except Exception as e:
        iniciasesion_bp.logger.error(f"Error en la función login: {e}")
        return jsonify({'success': False, 'message': 'Ocurrió un error inesperado. Intente nuevamente.'}), 500
    
@iniciasesion_bp.route('/toggle_mantenimiento', methods=['POST'])
def toggle_mantenimiento():
    global MANTENIMIENTO_ACTIVO

    if session.get('rol') != 'administrador':
        return jsonify({'success': False, 'message': 'No tienes permisos para cambiar el estado de mantenimiento.'}), 403

    MANTENIMIENTO_ACTIVO = not MANTENIMIENTO_ACTIVO  # Alterna entre activado y desactivado
    estado = "activado" if MANTENIMIENTO_ACTIVO else "desactivado"
    return jsonify({'success': True, 'message': f'Mantenimiento {estado} correctamente.'})





@iniciasesion_bp.route('/cambiar_acceso', methods=['POST'])
@login_required
@administrador_required
def cambiar_acceso():
    usuario_id = request.form['usuario_id']
    habilitar = request.form['habilitar'] == 'true'

    conn = get_db_connection('visitas')
    cursor = conn.cursor()
    try:
        # 🔹 Si se habilita el acceso, también resetear intentos fallidos a 0
        if habilitar:
            cursor.execute("UPDATE usuarios SET habilitar_acceso = %s, intentos_fallidos = 0 WHERE id_usuario = %s", (habilitar, usuario_id))
        else:
            cursor.execute("UPDATE usuarios SET habilitar_acceso = %s WHERE id_usuario = %s", (habilitar, usuario_id))

        conn.commit()
        
        registrar_auditoria(
            usuario_id=session.get('usuario_id'),
            nombre_usuario=session.get('nombre'),
            correo=session.get('correo'),
            accion="UPDATE",
            modulo="Gestión de Usuarios",
            detalle_accion=f"El usuario '{session.get('nombre')}' ({session.get('correo')}) {'habilitó' if habilitar else 'inhabilitó'} el acceso del usuario con ID {usuario_id}"
        )
        flash(f"Acceso {'habilitado' if habilitar else 'inhabilitado'} correctamente para el usuario.", 'success')
    except Error as e:
        print(f"Error al actualizar acceso: {e}")
        flash('Error al actualizar el acceso del usuario.', 'error')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('iniciasesion_bp.lista_usuarios'))


@iniciasesion_bp.route('/lista_usuarios', methods=['GET'])
@login_required
@administrador_required
def lista_usuarios():
    conn = get_db_connection('visitas')
    cursor = conn.cursor(dictionary=True)  # Usamos dictionary=True para obtener un diccionario
    cursor.execute("SELECT id_usuario, nombre, correo, rol, habilitar_acceso, intentos_fallidos FROM usuarios ORDER BY nombre ASC")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    usuario_sesion = session.get('usuario_id')
    nombre_sesion = session.get('nombre', 'Desconocido')
    correo_sesion = session.get('correo', 'Sin correo')
    
    registrar_auditoria(
        usuario_id=usuario_sesion if usuario_sesion else 0,
        nombre_usuario=nombre_sesion,
        correo = correo_sesion,
        accion="QUERY",
        modulo="Gestión de Usuarios",
        detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) consultó la lista de usuarios."
    )

    return render_template('usuarios_lista.html', usuarios=usuarios)

@iniciasesion_bp.route('/actualizar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@administrador_required
def actualizar_usuario(usuario_id):
    conn = get_db_connection('visitas')
    cursor = conn.cursor(dictionary=True)

    # Obtener información del usuario
    cursor.execute("SELECT id_usuario, nombre, correo, rol, id_operador FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario = cursor.fetchone()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado.'}), 404

    # Obtener lista de operadores
    operadores = fetch_operador()

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']
        id_operador = request.form.get('id_operador')  # Permite que sea opcional
        nueva_contrasena = request.form.get('nueva_contrasena', None)

        # Validar el rol: Si no es 'operador', establece id_operador en NULL
        if rol != 'operador':
            id_operador = None

        # Generar hash para la nueva contraseña
        contrasena_hash = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8') if nueva_contrasena else usuario['contrasena']

        # Actualizar usuario
        try:
            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s, correo = %s, contrasena = %s, rol = %s, id_operador = %s
                WHERE id_usuario = %s
            """, (nombre, correo, contrasena_hash, rol, id_operador, usuario_id))
            conn.commit()
            
            usuario_sesion = session.get('usuario_id')
            nombre_sesion = session.get('nombre', 'Unknown')
            correo_sesion = session.get('correo', 'No email')

            registrar_auditoria(
                usuario_id=usuario_sesion if usuario_sesion else 0,
                nombre_usuario=nombre_sesion,
                correo = correo_sesion,
                accion="UPDATE",
                modulo="Gestión de Usuarios",
                detalle_accion=f"El administrador '{nombre_sesion}' ({correo_sesion}) actualizando usuario con el nonmbre '{nombre}' y correo '{correo}'."
            )
            
            return jsonify({'success': 'Usuario actualizado exitosamente.'})
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return jsonify({'error': 'Error al actualizar el usuario.'}), 500

        finally:
            cursor.close()
            conn.close()

    cursor.close()
    conn.close()

    return render_template('actualizar_usuario.html', usuario=usuario, operadores=operadores)



@iniciasesion_bp.route('/actualizar_usuario_rol', methods=['GET', 'POST'])
@login_required
def actualizar_usuario_rol():
    usuario_id = session.get('usuario_id')  # Obtener ID del usuario actual
    conn = None
    cursor = None

    try:
        # Conexión a la base de datos
        conn = get_db_connection('visitas')
        if conn is None:
            flash('Error al conectar con la base de datos.', 'error')
            return redirect(url_for(f"iniciasesion_bp.dashboard_{session['rol']}"))

        cursor = conn.cursor(dictionary=True)

        # Obtener los datos actuales del usuario
        cursor.execute("SELECT nombre, correo FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash("El usuario no existe.", "error")
            return redirect(url_for(f"iniciasesion_bp.dashboard_{session['rol']}"))

        if request.method == 'POST':
            # Obtener los nuevos datos del formulario
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form.get('contrasena')  # Contraseña opcional

            # Actualizar la contraseña solo si se proporciona
            if contrasena:
                contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, correo = %s, contrasena = %s
                    WHERE id_usuario = %s
                """, (nombre, correo, contrasena_hash, usuario_id))
            else:
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, correo = %s
                    WHERE id_usuario = %s
                """, (nombre, correo, usuario_id))
            
            # Registrar auditoría de la actualización del usuario

            conn.commit()
            
            usuario_sesion = session.get('usuario_id')
            nombre_sesion = session.get('nombre', 'Desconocido')
            correo_sesion = session.get('correo', 'Sin correo')

            registrar_auditoria(
                usuario_id=usuario_sesion if usuario_sesion else 0,
                nombre_usuario=nombre_sesion,
                correo = correo_sesion,
                accion="UPDATE",
                modulo="Gestión de Usuarios",
                detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) actualizó los datos del usuario con el Nombre '{nombre}', Correo '{correo}'."
            )

            flash("Perfil actualizado exitosamente.", "success")
            return redirect(url_for(f"iniciasesion_bp.dashboard_{session['rol']}"))

        return render_template('actualizar_usuario_rol.html', usuario=usuario)

    except Exception as e:
        print(f"Error al actualizar el perfil: {e}")
        flash("Ocurrió un error al actualizar el perfil.", "error")
        return redirect(url_for(f"iniciasesion_bp.dashboard_{session['rol']}"))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

from flask import flash, redirect, url_for, render_template

@iniciasesion_bp.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
@login_required
@administrador_required
def eliminar_usuario(usuario_id):
    conn = get_db_connection('visitas')
    cursor = conn.cursor()

    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT id_usuario, nombre, correo FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('iniciasesion_bp.lista_usuarios'))  # Cambia a tu ruta de lista de usuarios

        # Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        conn.commit()
        
        usuario_sesion = session.get('usuario_id')
        nombre_sesion = session.get('nombre', 'Desconocido')
        correo_sesion = session.get('correo', 'Sin correo')

        registrar_auditoria(
            usuario_id=usuario_sesion if usuario_sesion else 0,
            nombre_usuario=nombre_sesion,
            correo = correo_sesion,
            accion="DELETE",
            modulo="Gestión de Usuarios",
            detalle_accion=f"El usuario '{nombre_sesion}' ({correo_sesion}) eliminó los datos del usuario con el nombre '{usuario['nombre']} y el correo ({usuario['correo']})'."
        )
        
        flash("Usuario eliminado exitosamente.", "success")
        return redirect(url_for('iniciasesion_bp.lista_usuarios'))  # Cambia a tu ruta de lista de usuarios
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        flash("Ocurrió un error al intentar eliminar el usuario.", "error")
        return redirect(url_for('iniciasesion_bp.lista_usuarios'))  # Cambia a tu ruta de lista de usuarios
    finally:
        cursor.close()
        conn.close()


# Centralización del Renderizado del Dashboard
def render_dashboard(rol):
    return render_template(
        'indexprincipal.html',
        usuario=session.get('nombre'),
        correo=session.get('correo'),
        rol=rol
    )

def role_required(*roles):
    """Decorador para restringir acceso según roles"""
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            user_role = session.get('rol')
            user_ip = request.remote_addr  # Obtiene la IP real del usuario

            if user_role == 'administrador' and not es_red_interna(user_ip):
                flash('Acceso restringido a la red interna.', 'error')
                return redirect(url_for('iniciasesion_bp.login'))

            if user_role not in roles:
                flash('Acceso no autorizado.', 'error')
                return redirect(url_for('iniciasesion_bp.login'))

            return f(*args, **kwargs)
        return wrapped_function
    return decorator


# Ruta para cada dashboard con acceso limitado por rol
@iniciasesion_bp.route('/indexprincipal/supervisor')
@login_required
@role_required('supervisor')
def dashboard_supervisor():
    return render_dashboard('supervisor')


@iniciasesion_bp.route('/indexprincipal/operador')
@login_required
@role_required('operador')
def dashboard_operador():
    return render_dashboard('operador')


@iniciasesion_bp.route('/indexprincipal/nutricionista')
@login_required
@role_required('nutricionista')
def dashboard_nutricionista():
    return render_dashboard('nutricionista')


@iniciasesion_bp.route('/indexprincipal/administrador')
@login_required
@role_required('administrador')
def dashboard_administrador():
    return render_dashboard('administrador')



# Ruta para cerrar sesión
@iniciasesion_bp.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    flash('Sesión cerrada exitosamente.', 'success')
    response = make_response(redirect(url_for('iniciasesion_bp.login')))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response




def registrar_auditoria(usuario_id, nombre_usuario, correo, accion, modulo, detalle_accion):
    """Registra un evento en la tabla de auditoría con la fecha y hora en Colombia"""
    conn = get_db_connection('visitas')
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        # Configurar la zona horaria de Colombia
        

        cursor.execute("""
            INSERT INTO auditoria (usuario_id, nombre_usuario, correo, accion, modulo, detalle_accion, fecha, ip)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (usuario_id, nombre_usuario, correo, accion, modulo, detalle_accion, fecha_colombia, request.remote_addr))
        
        conn.commit()
    except Error as e:
        pass  # Puedes manejar el error de otra forma si lo deseas
    finally:
        cursor.close()
        conn.close()

