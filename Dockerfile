# Imagen base ligera
FROM python:3.11-slim

# Evitar archivos .pyc y buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (mejor caching)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto expuesto
EXPOSE 10000

# Comando de arranque (usando variable PORT)
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:${PORT:-10000}"]