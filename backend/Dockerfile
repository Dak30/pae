FROM python:3.12

WORKDIR /pae

# Instalar dependencias del sistema y configurar locales
RUN apt-get update && apt-get install -y locales default-mysql-client \
    && echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen && update-locale LANG=es_ES.UTF-8 \
    && rm -rf /var/lib/apt/lists/*  # Liberar espacio

# Establecer el locale por defecto
ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES:es
ENV LC_ALL=es_ES.UTF-8

# Copiar archivos
COPY . /pae

# Instalar dependencias de Python
RUN python -m pip install --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5000 

# Ejecutar Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "--log-level", "info", "app:app"]


