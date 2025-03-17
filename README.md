# Aplicativo PAE - Flask, MySQL y HTML

Este documento describe los pasos para instalar, configurar y ejecutar el aplicativo del **Programa de Alimentación Escolar (PAE)** utilizando **XAMPP, MySQL y Flask**.

---

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

1. **XAMPP** (para MySQL y Apache) - [Descargar aquí](https://www.apachefriends.org/es/index.html)
2. **Python** (versión 3.8 o superior) - [Descargar aquí](https://www.python.org/downloads/)
3. **Git** (opcional, para clonar el repositorio) - [Descargar aquí](https://git-scm.com/)

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar o Descargar el Proyecto
Si tienes Git instalado, puedes clonar el repositorio:
```bash
  git clone https://github.com/Dak30/pae.git
  cd pae
```
Si no tienes Git, descarga el código en formato ZIP y extráelo en una carpeta.

### 2️⃣ Configurar el Servidor MySQL en XAMPP
1. Abre **XAMPP** y activa los módulos:
   - `Apache`
   - `MySQL`
2. Accede a **phpMyAdmin** desde el navegador:
   ```
   http://localhost:8081/phpmyadmin/
   ```
3. Crea una base de datos llamada `pae_db`.
4. Importa el archivo `pae_db.sql` (ubicado en el proyecto) en **phpMyAdmin**.

### 3️⃣ Configurar el Entorno de Python
1. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   venv\Scripts\activate     # En Windows
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

### 4️⃣ Configurar la Conexión a la Base de Datos
Edita el archivo **config.py** y asegúrate de que la configuración de MySQL sea correcta:
```python
DB_HOST = "127.0.0.1"
DB_USER = "pae"  # Usuario por defecto en XAMPP
DB_PASSWORD = "pae_educacion"  # XAMPP no tiene contraseña por defecto
DB_NAME = "visitas"
```

---

## ▶️ Ejecutar el Proyecto

1. Activa el entorno virtual (si usaste uno):
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
2. Inicia la aplicación Flask:
   ```bash
   python visitas.py
   ```
3. Abre el navegador y accede a la aplicación:
   ```
   http://ip:5000/
   ```

---

## 🛠 Mantenimiento y Actualización
Si necesitas actualizar el código o instalar nuevas dependencias:
```bash
  git pull origin main  # Si usaste Git
  pip install -r requirements.txt  # Para actualizar librerías
```
Para realizar un respaldo de la base de datos:
1. Abre **phpMyAdmin**.
2. Selecciona `visitas`.
3. Ve a la pestaña **Exportar** y selecciona formato `SQL`.

---

## 📌 Notas Adicionales
- Si MySQL no inicia en XAMPP, verifica que **no haya otro servicio usando el puerto 3306**.
- Puedes cambiar el puerto de Flask en `visitas.py` si es necesario:
  ```python
  visitas.run(port=5001, debug=True)
  ```

---

¡Listo! Con estos pasos, la aplicación PAE debería estar funcionando correctamente. 🚀


