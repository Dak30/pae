# Aplicativo PAE - Flask, MySQL y Docker

Este documento describe cómo instalar, configurar y ejecutar el aplicativo del **Programa de Alimentación Escolar (PAE)** utilizando **Docker, MySQL y Flask**.

---

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

1. **Docker** - [Descargar aquí](https://www.docker.com/get-started)
2. **Git** (opcional, para clonar el repositorio) - [Descargar aquí](https://git-scm.com/)
3. **MySQL Workbench 8.0** - [Descargar aquí](https://dev.mysql.com/downloads/workbench/)

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar o Descargar el Proyecto
Si tienes Git instalado, puedes clonar el repositorio:
```bash
git clone https://github.com/Dak30/pae.git
cd pae
```
Si no tienes Git, descarga el código en formato ZIP y extráelo en una carpeta.

### 2️⃣ Configurar y Ejecutar los Contenedores
Ejecuta el siguiente comando en la raíz del proyecto:

```bash
docker-compose up -d
```

Esto levantará:
- Un contenedor MySQL con la base de datos `visitas`.
- Un contenedor Flask ejecutando la aplicación.

### 3️⃣ Importar la Base de Datos
1. Abre **Mysql Worbench** en el navegador:
2. Inicia sesión con:
   - Usuario: `Pae`
   - Contraseña: `Pae_educacion`
3. Carga el archivo `visitas.sql` ubicado en `documentacion/modelado de datos/`.

### 4️⃣ Conectar MySQL Workbench 8.0 a Docker

1. Abre **MySQL Workbench 8.0**.
2. Haz clic en **Database > Manage Connections**.
3. Agrega una nueva conexión con estos datos:
   - **Connection Name:** MySQL Docker PAE
   - **Hostname:** 127.0.0.1
   - **Port:** 3306
   - **Username:** Pae
   - **Password:** Pae_educacion (guárdala si lo deseas)
4. Haz clic en **Test Connection** y verifica que la conexión sea exitosa.
5. Guarda la conexión y usa MySQL Workbench para administrar la base de datos.

---

## ▶️ Acceder a la Aplicación

Abre el navegador y accede a:
```
http://127.0.0.1:5000/
```

---

## 🛠 Mantenimiento y Actualización
Para detener los contenedores:
```bash
docker-compose down
```
Para reconstruir la imagen después de cambios en el código:
```bash
docker-compose up --build -d
```

---

¡Listo! Con estos pasos, la aplicación PAE debería estar funcionando correctamente en Docker y ser accesible desde MySQL Workbench. 🚀
