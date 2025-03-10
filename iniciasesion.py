from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify, make_response
from functools import wraps
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error
import os
from database import get_db_connection


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))  # Usa una clave secreta de entorno

bcrypt = Bcrypt(app)

# Crear el Blueprint
iniciasesion_bp = Blueprint('iniciasesion_bp', __name__, template_folder='templates/usuarios')


# Función para conectarse a la base de datos
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="Pae",
            password="Pae_educacion",
            database="visitas"
        )

        if conn.is_connected():
            print("✅ Conexión exitosa a MySQL")
            return conn
        else:
            print("❌ No se pudo conectar a la base de datos")
            return None

    except mysql.connector.Error as err:
        print(f"⚠️ Error de conexión a MySQL: {err}")
        return None

# Obtener operadores de la base de datos
def fetch_operador():
    conn = get_db_connection()
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
            print("Usuario no autenticado, redirigiendo a inicio de sesión.")
            flash('Por favor inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))
        
        # Validar el rol si es necesario
        rol = session.get('rol')
        if rol in ['supervisor', 'nutricionista', 'administrador']:
            print("Usuario con rol supervisor/nutricionista, permitido sin operador asociado.")
            return f(*args, **kwargs)

        # Validar `id_operador` para otros roles
        if session.get('id_operador') is None:
            print("Acceso restringido: Operador no asociado.")
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('iniciasesion_bp.login'))

        print("Usuario autenticado. Sesión:", session)
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'rol' not in session or session['rol'] not in roles:
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('iniciasesion_bp.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


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

        # Conexión a la base de datos
        conn = get_db_connection()
        if conn is None:
            flash('Error al conectar con la base de datos.', 'error')
            return render_template('registro.html')

        cursor = conn.cursor()
        try:
            # Insertar el nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol, id_operador) VALUES (%s, %s, %s, %s, %s)",
                (nombre, correo, contrasena_hash, rol, id_operador)
            )
            conn.commit()
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

@iniciasesion_bp.route('/login', methods=['GET', 'POST'])
def login():  
    try:
        if request.method == 'POST':
            correo = request.form['correo']
            contrasena = request.form['contrasena']

            # Conexión a la base de datos
            conn = get_db_connection()
            if conn is None:
                return jsonify({'error': 'Error al conectar con la base de datos.'}), 500

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            if usuario:
                # Verificar si el usuario está habilitado
                if not usuario.get('habilitar_acceso', False):
                    return jsonify({'error': 'Su cuenta está inhabilitada. Contacte al administrador.'}), 403

                # Verificar la contraseña
                if bcrypt.check_password_hash(usuario['contrasena'], contrasena):
                    session.update({
                        'usuario_id': usuario['id_usuario'],
                        'nombre': usuario['nombre'],
                        'correo': usuario['correo'],
                        'rol': usuario['rol'],
                        'id_operador': usuario['id_operador']
                    })
                    return jsonify({'success': 'Inicio de sesión exitoso.', 'redirect': url_for(f"iniciasesion_bp.dashboard_{usuario['rol']}")})

                return jsonify({'error': 'Correo o contraseña incorrectos.'}), 401

            return jsonify({'error': 'Usuario no encontrado.'}), 404

        return render_template('iniciarsesion.html')

    except Exception as e:
        # Registrar el error para depuración
        app.logger.error(f"Error en la función login: {e}")
        return jsonify({'error': 'Ocurrió un error inesperado. Por favor, intente nuevamente.'}), 500



@iniciasesion_bp.route('/cambiar_acceso', methods=['POST'])
@login_required
@administrador_required
def cambiar_acceso():
    usuario_id = request.form['usuario_id']
    habilitar = request.form['habilitar'] == 'true'

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET habilitar_acceso = %s WHERE id_usuario = %s", (habilitar, usuario_id))
        conn.commit()
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Usamos dictionary=True para obtener un diccionario
    cursor.execute("SELECT id_usuario, nombre, correo, rol, habilitar_acceso FROM usuarios ORDER BY nombre ASC")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('usuarios_lista.html', usuarios=usuarios)

@iniciasesion_bp.route('/actualizar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@administrador_required
def actualizar_usuario(usuario_id):
    conn = get_db_connection()
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
        conn = get_db_connection()
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

            conn.commit()
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
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el usuario existe
        cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('iniciasesion_bp.lista_usuarios'))  # Cambia a tu ruta de lista de usuarios

        # Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        conn.commit()
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

# Ruta para el dashboard de los supervisores (acceso limitado)
@iniciasesion_bp.route('/indexprincipal/supervisor')
@login_required
def dashboard_supervisor():
    if session.get('rol') != 'supervisor':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('iniciasesion_bp.login'))
    return render_dashboard('supervisor')


# Ruta para el dashboard de los operadores (acceso limitado)
@iniciasesion_bp.route('/indexprincipal/operador')
@login_required
def dashboard_operador():
    if session.get('rol') != 'operador':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('iniciasesion_bp.login'))
    return render_dashboard('operador')


# Ruta para el dashboard de nutricionistas (acceso limitado)
@iniciasesion_bp.route('/indexprincipal/nutricionista')
@login_required
def dashboard_nutricionista():
    if session.get('rol') != 'nutricionista':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('iniciasesion_bp.login'))
    return render_dashboard('nutricionista')


# Ruta para el dashboard de administradores (acceso limitado)
@iniciasesion_bp.route('/indexprincipal/administrador')
@login_required
def dashboard_administrador():
    if session.get('rol') != 'administrador':
        flash('Acceso no autorizado.', 'error')
        return redirect(url_for('iniciasesion_bp.login'))
    return render_dashboard('administrador')


def role_required(*roles):
    @wraps(roles)
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            user_role = session.get('rol')
            if user_role not in roles and user_role != 'administrador':
                flash('Acceso no autorizado.', 'error')
                return redirect(url_for('iniciasesion_bp.login'))
            return f(*args, **kwargs)
        return wrapped_function
    return decorator


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

