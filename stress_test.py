from locust import HttpUser, task, between
import random
import mysql.connector

def obtener_usuarios():
    """Consulta la base de datos y obtiene usuarios reales para la prueba."""
    usuarios = []
    try:
        conn = mysql.connector.connect(
            host="tu_host_mysql",
            user="tu_usuario_mysql",
            password="tu_contraseña_mysql",
            database="visitas"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT correo, contrasena FROM usuarios WHERE habilitar_acceso = 1 LIMIT 50")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error al obtener usuarios: {e}")
    return usuarios

class PruebaCargaUsuarios(HttpUser):
    wait_time = between(1, 3)  # Simula tiempo entre peticiones
    rutas = [
        "/login",
        "/bodega",
        "/tecnica",
        "/visitas",
        "/infraestructura",
        "/menus",
        "/actualizar",
        "/verificacion",
        "/instituciones",
        "/sedes"
    ]

    def on_start(self):
        """Carga usuarios de MySQL al iniciar la prueba."""
        self.usuarios = obtener_usuarios()

    @task(3)  # Prioridad más alta (3x veces más que las otras tareas)
    def login(self):
        """Simula múltiples intentos de inicio de sesión."""
        if not self.usuarios:
            print("⚠️ No hay usuarios disponibles para la prueba.")
            return

        usuario = random.choice(self.usuarios)
        response = self.client.post("/login", data={
            "correo": usuario["correo"],
            "contrasena": usuario["contrasena"]
        })

        if response.status_code == 200 and response.json().get("success"):
            print(f"✅ Login exitoso: {response.json()}")
        else:
            print(f"❌ Fallo en login: {response.status_code} {response.text}")

    @task(1)
    def probar_rutas(self):
        """Simula carga en todas las rutas registradas."""
        ruta = random.choice(self.rutas)
        response = self.client.get(ruta)

        if response.status_code == 200:
            print(f"✅ Ruta {ruta} funcionando correctamente.")
        else:
            print(f"❌ Error en ruta {ruta}: {response.status_code}")
