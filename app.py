from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
from guardian_lexer import GuardianLexer
from guardian_parser import GuardianParser
from guardian_interpreter import GuardianInterpreter
from bot_api_endpoints import register_bot_api
from real_time_validator import validate_guardian_command
from custom_bot_ai_assistant import get_ai_suggestions, generate_custom_bot

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)  # Habilitar CORS para todas las rutas

# Registrar endpoints de bots
register_bot_api(app)

# Initialize Guardian components
lexer = GuardianLexer()
parser = GuardianParser(lexer)
interpreter = GuardianInterpreter()

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('static', filename)

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a Guardian command"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ningún comando'
            }), 400
        
        command = data['command'].strip()
        if not command:
            return jsonify({
                'success': False,
                'error': 'El comando está vacío'
            }), 400
        
        # Parse the command
        try:
            ast = parser.parse(command)
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Error de sintaxis: {str(e)}',
                'type': 'syntax_error'
            }), 400
        
        # Execute the command
        try:
            # Capture output from interpreter
            import io
            from contextlib import redirect_stdout, redirect_stderr
            
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                result = interpreter.execute(ast)
            
            stdout_content = output_buffer.getvalue()
            stderr_content = error_buffer.getvalue()
            
            # Combine outputs
            output = stdout_content
            if stderr_content:
                output += f"\nErrores: {stderr_content}"
            
            return jsonify({
                'success': True,
                'output': output.strip() if output.strip() else 'Comando ejecutado correctamente',
                'ast': ast,
                'command': command
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error de ejecución: {str(e)}',
                'type': 'execution_error'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}',
            'type': 'server_error'
        }), 500



@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Get list of available commands"""
    commands = [
        {
            'name': 'analizar puertos',
            'syntax': 'analizar puertos de <IP>',
            'description': 'Realiza un escaneo de puertos en la dirección IP especificada',
            'example': 'analizar puertos de 192.168.1.1'
        },
        {
            'name': 'crear regla firewall',
            'syntax': 'crear regla firewall puerto: <PUERTO> protocolo: <TCP|UDP> accion: <bloquear|permitir>',
            'description': 'Crea una nueva regla de firewall',
            'example': 'crear regla firewall puerto: 22 protocolo: TCP accion: bloquear'
        },
        {
            'name': 'leer logs',
            'syntax': 'leer logs de <RUTA>',
            'description': 'Lee y muestra el contenido de un archivo de log',
            'example': 'leer logs de /var/log/syslog'
        },
        {
            'name': 'monitorear trafico',
            'syntax': 'monitorear trafico en <INTERFAZ>',
            'description': 'Inicia el monitoreo de tráfico de red',
            'example': 'monitorear trafico en eth0'
        },
        {
            'name': 'alertar',
            'syntax': 'alertar <MENSAJE>',
            'description': 'Envía una alerta de seguridad',
            'example': 'alertar "Intrusión detectada"'
        },
        {
            'name': 'ver procesos',
            'syntax': 'ver procesos activos',
            'description': 'Muestra una lista de procesos activos',
            'example': 'ver procesos activos'
        }
    ]
    
    return jsonify({
        'commands': commands,
        'total': len(commands)
    })

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example scripts"""
    examples = {
        'basic': {
            'name': 'Comandos Básicos',
            'description': 'Ejemplos de comandos básicos de Guardián',
            'code': '''# Comandos básicos de Guardián
analizar puertos de 192.168.1.1
ver procesos activos
alertar "Sistema iniciado correctamente"'''
        },
        'firewall': {
            'name': 'Configuración Firewall',
            'description': 'Ejemplos de configuración de firewall',
            'code': '''# Configuración de firewall
crear regla firewall puerto: 22 protocolo: TCP accion: bloquear
crear regla firewall puerto: 80 protocolo: TCP accion: permitir
crear regla firewall puerto: 443 protocolo: TCP accion: permitir
alertar "Reglas de firewall configuradas"'''
        },
        'monitoring': {
            'name': 'Monitoreo de Red',
            'description': 'Ejemplos de monitoreo de red y logs',
            'code': '''# Monitoreo de red y logs
monitorear trafico en eth0
leer logs de /var/log/syslog
analizar puertos de 10.0.0.1
alertar "Monitoreo iniciado"'''
        }
    }
    
    return jsonify({
        'examples': examples
    })

@app.route('/api/validate', methods=['POST'])
def validate_real_time():
    """Real-time syntax validation endpoint"""
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({
                'valid': False,
                'errors': [{
                    'type': 'MISSING_INPUT',
                    'message': 'No se proporcionó código para validar',
                    'line': 1,
                    'column': 0,
                    'severity': 'error'
                }]
            }), 400
        
        code = data['code']
        
        # Validate the command
        result = validate_guardian_command(code)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'valid': False,
            'errors': [{
                'type': 'SERVER_ERROR',
                'message': f'Error en validación: {str(e)}',
                'line': 1,
                'column': 0,
                'severity': 'error'
            }]
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Guardian IDE Backend',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=port,
        debug=False  # Set to False for production
    )


# Almacenar sesiones activas
bot_sessions = {}

@app.route('/api/bots/sessions/start', methods=['POST'])
def start_bot_session():
    """Inicia una sesión de creación de bot con IA"""
    try:
        data = request.get_json()
        if not data or 'template_id' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó template_id'
            }), 400
        
        template_id = data['template_id']
        user_id = data.get('user_id', 'web_user_' + str(int(time.time())))
        session_id = f"session_{user_id}_{int(time.time())}"
        
        # Crear sesión
        bot_sessions[session_id] = {
            'template_id': template_id,
            'user_id': user_id,
            'messages': [],
            'created_at': time.time()
        }
        
        # Mensaje inicial según la plantilla
        if template_id == 'network_monitoring_bot':
            initial_message = "¡Hola! Voy a ayudarte a crear un Bot de Monitoreo de Red. ¿Cuál es el nombre que deseas para este bot?"
        elif template_id == 'incident_response_bot':
            initial_message = "¡Hola! Voy a ayudarte a crear un Bot de Respuesta a Incidentes. ¿Cuál es el nombre que deseas para este bot?"
        else:
            initial_message = "¡Hola! Voy a ayudarte a crear tu bot personalizado. ¿Cuál es el nombre que deseas para este bot?"
        
        bot_sessions[session_id]['messages'].append({
            'role': 'assistant',
            'content': initial_message
        })
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': initial_message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al iniciar sesión: {str(e)}'
        }), 500

@app.route('/api/bots/sessions/<session_id>/message', methods=['POST'])
def send_bot_message(session_id):
    """Envía un mensaje a la sesión de creación de bot"""
    try:
        if session_id not in bot_sessions:
            return jsonify({
                'success': False,
                'error': 'Sesión no encontrada'
            }), 404
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó mensaje'
            }), 400
        
        user_message = data['message']
        session = bot_sessions[session_id]
        
        # Agregar mensaje del usuario
        session['messages'].append({
            'role': 'user',
            'content': user_message
        })
        
        # Generar respuesta de IA
        ai_response = generate_bot_ai_response(session['template_id'], session['messages'])
        
        # Agregar respuesta de IA
        session['messages'].append({
            'role': 'assistant',
            'content': ai_response
        })
        
        return jsonify({
            'success': True,
            'message': ai_response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al procesar mensaje: {str(e)}'
        }), 500

def generate_bot_ai_response(template_id, messages):
    """Genera una respuesta de IA para la sesión de bot"""
    # Obtener el último mensaje del usuario
    user_messages = [m for m in messages if m['role'] == 'user']
    if not user_messages:
        return "Por favor, proporciona información sobre tu bot."
    
    last_user_message = user_messages[-1]['content']
    message_count = len(user_messages)
    
    # Lógica de conversación según el número de mensajes
    if message_count == 1:
        # Primer mensaje: confirmar nombre y preguntar función
        return f"Excelente, '{last_user_message}' es un gran nombre. ¿Cuál es la función principal que deseas que realice este bot? (ej: monitoreo, detección, respuesta)"
    elif message_count == 2:
        # Segundo mensaje: preguntar sobre configuración
        return f"Perfecto, un bot de {last_user_message}. ¿Con qué frecuencia deseas que se ejecute? (ej: cada 5 minutos, cada hora, en tiempo real)"
    elif message_count == 3:
        # Tercer mensaje: preguntar sobre acciones
        return f"Bien, cada {last_user_message}. ¿Qué acciones deseas que realice cuando detecte algo? (ej: enviar alerta, generar reporte, bloquear)"
    elif message_count == 4:
        # Cuarto mensaje: confirmación y generación
        return f"Perfecto. Voy a generar tu bot '{messages[0]['content']}' con las configuraciones que especificaste. ¡Tu bot está listo!"
    else:
        # Mensajes posteriores
        return "¿Hay algo más que desees configurar en tu bot?"

@app.route('/api/custom-bot/suggestions', methods=['POST'])
def get_custom_bot_suggestions():
    """Obtiene sugerencias de IA para un bot personalizado"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        suggestions = get_ai_suggestions(data)
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar sugerencias: {str(e)}'
        }), 500

@app.route('/api/custom-bot/generate', methods=['POST'])
def generate_custom_bot_endpoint():
    """Genera un bot personalizado"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        result = generate_custom_bot(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar bot: {str(e)}'
        }), 500
