#!/bin/bash

# Guardián IDE - Start Server Script
# Este script inicia el servidor Gunicorn de forma permanente

set -e

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Crear directorio de logs si no existe
mkdir -p logs

# Activar entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Entorno virtual no encontrado. Creando..."
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Obtener puerto de variable de entorno o usar 5000 por defecto
PORT=${PORT:-5000}

# Iniciar Gunicorn
echo "Iniciando Guardián IDE en puerto $PORT..."
echo "Accede a: http://localhost:$PORT"

gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --keep-alive 5 \
    wsgi:app
