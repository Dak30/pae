Este documento describe cómo instalar, configurar y ejecutar el aplicativo del **Programa de Alimentación Escolar (PAE)** utilizando **Docker, MySQL y Flask**.

---

## 📌 Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

1. **Docker** - [Descargar aquí](https://www.docker.com/get-started)
2. **Git** (opcional, para clonar el repositorio) - [Descargar aquí](https://git-scm.com/)

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
1. Abre **phpMyAdmin** en el navegador:
   ```
   http://localhost:8081/
   ```
2. Inicia sesión con:
   - Usuario: `pae`
   - Contraseña: `pae_educacion`
3. Carga el archivo `visitas.sql` ubicado en `documentacion/modelado de datos/`.

---

## ▶️ Acceder a la Aplicación

Abre el navegador y accede a:
```
http://localhost:5000/
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

¡Listo! Con estos pasos, la aplicación PAE debería estar funcionando correctamente en Docker. 🚀