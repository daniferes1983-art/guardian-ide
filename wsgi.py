"""
WSGI entry point para Guardián IDE
Usado por Gunicorn en producción
"""
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar la aplicación Flask
from app import app

if __name__ == "__main__":
    app.run()
