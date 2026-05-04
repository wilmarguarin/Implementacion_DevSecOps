# Imagen base ligera
FROM python:3.11-slim

# Evitar archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar únicamente los archivos necesarios de la aplicación
COPY main.py .
COPY server.py .
COPY init_db.py .

# Copiar carpetas necesarias para la aplicación Flask
COPY templates ./templates
COPY static ./static
COPY routes ./routes
COPY db ./db

# Crear usuario no privilegiado y asignar permisos
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

# Ejecutar la aplicación con usuario no root
USER appuser

# Puerto expuesto
EXPOSE 10000

# Comando de arranque
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:${PORT:-10000}"]