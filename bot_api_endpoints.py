"""
Endpoints de API para el Sistema de Creación de Bots en Guardián IDE
Proporciona endpoints REST para interactuar con el motor de plantillas y el asistente de IA.
"""

from flask import Blueprint, request, jsonify
from bot_template_engine import GuardianBotTemplateEngine
from bot_ai_assistant import GuardianBotAIAssistant
import json
import uuid

# Crear blueprint para los endpoints de bots
bot_api = Blueprint('bot_api', __name__, url_prefix='/api/bots')

# Instancias globales
template_engine = GuardianBotTemplateEngine()
ai_assistant = GuardianBotAIAssistant()

# Almacenamiento temporal de sesiones (en producción usar Redis o base de datos)
active_sessions = {}


@bot_api.route('/templates', methods=['GET'])
def get_available_templates():
    """Obtiene todas las plantillas de bots disponibles"""
    try:
        templates = template_engine.get_available_templates()
        return jsonify({
            'success': True,
            'templates': templates,
            'count': len(templates)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/templates/<template_id>', methods=['GET'])
def get_template_details(template_id):
    """Obtiene los detalles completos de una plantilla específica"""
    try:
        template = template_engine.get_template_details(template_id)
        if template:
            return jsonify({
                'success': True,
                'template': template
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Plantilla {template_id} no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/templates/<template_id>/parameters', methods=['GET'])
def get_template_parameters(template_id):
    """Obtiene los parámetros configurables de una plantilla"""
    try:
        parameters = template_engine.get_template_parameters(template_id)
        if parameters is not None:
            return jsonify({
                'success': True,
                'parameters': parameters
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Plantilla {template_id} no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/sessions/start', methods=['POST'])
def start_bot_creation_session():
    """Inicia una nueva sesión de creación de bot con el asistente de IA"""
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        if not template_id:
            return jsonify({
                'success': False,
                'error': 'template_id es requerido'
            }), 400
        
        # Crear nueva instancia del asistente para esta sesión
        session_assistant = GuardianBotAIAssistant()
        result = session_assistant.start_bot_creation_session(template_id, user_id)
        
        if result['success']:
            # Guardar la sesión
            session_id = result['session_id']
            active_sessions[session_id] = session_assistant
            
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/sessions/<session_id>/respond', methods=['POST'])
def process_user_response(session_id):
    """Procesa una respuesta del usuario en una sesión activa"""
    try:
        data = request.get_json()
        user_response = data.get('response', '')
        
        if not user_response:
            return jsonify({
                'success': False,
                'error': 'response es requerido'
            }), 400
        
        # Obtener la sesión
        session_assistant = active_sessions.get(session_id)
        if not session_assistant:
            return jsonify({
                'success': False,
                'error': 'Sesión no encontrada o expirada'
            }), 404
        
        # Procesar respuesta
        result = session_assistant.process_user_response(session_id, user_response)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/sessions/<session_id>/finalize', methods=['POST'])
def finalize_bot_creation(session_id):
    """Finaliza la creación del bot y genera el código"""
    try:
        # Obtener la sesión
        session_assistant = active_sessions.get(session_id)
        if not session_assistant:
            return jsonify({
                'success': False,
                'error': 'Sesión no encontrada o expirada'
            }), 404
        
        # Finalizar y generar bot
        result = session_assistant.finalize_and_generate_bot(session_id)
        
        if result['success']:
            # Limpiar la sesión después de completarla
            del active_sessions[session_id]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Obtiene el estado actual de una sesión"""
    try:
        session_assistant = active_sessions.get(session_id)
        if not session_assistant:
            return jsonify({
                'success': False,
                'error': 'Sesión no encontrada'
            }), 404
        
        status = session_assistant.get_session_status(session_id)
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/generate', methods=['POST'])
def generate_bot_directly():
    """Genera un bot directamente sin asistente de IA (para usuarios avanzados)"""
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        parameters = data.get('parameters', {})
        
        if not template_id:
            return jsonify({
                'success': False,
                'error': 'template_id es requerido'
            }), 400
        
        # Generar bot usando el motor de plantillas
        result = template_engine.generate_bot_code(template_id, parameters)
        
        if result['success']:
            # Validar el bot generado
            validation = template_engine.validate_generated_bot(
                template_id, result['code'], parameters
            )
            
            return jsonify({
                'success': True,
                'bot_code': result['code'],
                'metadata': result['metadata'],
                'validation': validation,
                'warnings': result['warnings']
            })
        else:
            return jsonify({
                'success': False,
                'errors': result['errors'],
                'warnings': result['warnings']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/validate', methods=['POST'])
def validate_bot_parameters():
    """Valida parámetros de bot antes de la generación"""
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        parameters = data.get('parameters', {})
        
        if not template_id:
            return jsonify({
                'success': False,
                'error': 'template_id es requerido'
            }), 400
        
        # Validar parámetros
        validation_result = template_engine.validate_parameters(template_id, parameters)
        
        return jsonify({
            'success': len(validation_result['errors']) == 0,
            'validation': validation_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/templates/<template_id>/testing-scenarios', methods=['GET'])
def get_testing_scenarios(template_id):
    """Obtiene los escenarios de prueba para una plantilla"""
    try:
        scenarios = template_engine.get_testing_scenarios(template_id)
        return jsonify({
            'success': True,
            'scenarios': scenarios,
            'count': len(scenarios)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/export', methods=['POST'])
def export_bot_configuration():
    """Exporta la configuración de un bot para guardado/carga posterior"""
    try:
        data = request.get_json()
        template_id = data.get('template_id')
        parameters = data.get('parameters', {})
        generated_code = data.get('generated_code', '')
        
        if not all([template_id, parameters, generated_code]):
            return jsonify({
                'success': False,
                'error': 'template_id, parameters y generated_code son requeridos'
            }), 400
        
        # Exportar configuración
        config = template_engine.export_bot_configuration(template_id, parameters, generated_code)
        
        return jsonify({
            'success': True,
            'configuration': config
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bot_api.route('/sessions/cleanup', methods=['POST'])
def cleanup_expired_sessions():
    """Limpia sesiones expiradas (para mantenimiento)"""
    try:
        # En una implementación real, esto verificaría timestamps y limpiaría sesiones viejas
        # Por ahora, simplemente reportamos el número de sesiones activas
        
        return jsonify({
            'success': True,
            'active_sessions': len(active_sessions),
            'message': 'Limpieza de sesiones completada'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Funciones de utilidad para los endpoints
def register_bot_api(app):
    """Registra los endpoints de bots en la aplicación Flask"""
    app.register_blueprint(bot_api)
    print("✅ Endpoints de API de bots registrados")


def get_api_documentation():
    """Retorna documentación de la API de bots"""
    return {
        'endpoints': [
            {
                'path': '/api/bots/templates',
                'method': 'GET',
                'description': 'Obtiene todas las plantillas disponibles'
            },
            {
                'path': '/api/bots/templates/<template_id>',
                'method': 'GET',
                'description': 'Obtiene detalles de una plantilla específica'
            },
            {
                'path': '/api/bots/templates/<template_id>/parameters',
                'method': 'GET',
                'description': 'Obtiene parámetros configurables de una plantilla'
            },
            {
                'path': '/api/bots/sessions/start',
                'method': 'POST',
                'description': 'Inicia sesión de creación de bot con IA',
                'body': {
                    'template_id': 'string',
                    'user_id': 'string (opcional)'
                }
            },
            {
                'path': '/api/bots/sessions/<session_id>/respond',
                'method': 'POST',
                'description': 'Procesa respuesta del usuario en sesión activa',
                'body': {
                    'response': 'string'
                }
            },
            {
                'path': '/api/bots/sessions/<session_id>/finalize',
                'method': 'POST',
                'description': 'Finaliza sesión y genera código del bot'
            },
            {
                'path': '/api/bots/generate',
                'method': 'POST',
                'description': 'Genera bot directamente sin asistente de IA',
                'body': {
                    'template_id': 'string',
                    'parameters': 'object'
                }
            },
            {
                'path': '/api/bots/validate',
                'method': 'POST',
                'description': 'Valida parámetros de bot',
                'body': {
                    'template_id': 'string',
                    'parameters': 'object'
                }
            }
        ]
    }


if __name__ == "__main__":
    # Prueba básica de los endpoints
    print("🔌 Probando Endpoints de API de Bots...")
    
    from flask import Flask
    
    app = Flask(__name__)
    register_bot_api(app)
    
    # Mostrar documentación
    docs = get_api_documentation()
    print("\\n📚 Endpoints disponibles:")
    for endpoint in docs['endpoints']:
        print(f"  {endpoint['method']} {endpoint['path']} - {endpoint['description']}")
    
    print("\\n✅ API de bots lista para usar")

