"""
Configuración para Guardián IDE
"""
import os
from pathlib import Path

# Directorio base de la aplicación
BASE_DIR = Path(__file__).parent.resolve()

# Configuración de Flask
class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Base de datos
    DATABASE_PATH = os.environ.get('DATABASE_PATH', str(BASE_DIR / 'guardian_ide.db'))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    TESTING = False
    # En producción, usar variables de entorno para la clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar configurada en producción")


class TestingConfig(Config):
    """Configuración de pruebas"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'


# Seleccionar configuración según el entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración según el entorno"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
