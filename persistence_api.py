"""
API REST para Sistema de Persistencia de Proyectos
IDE Guardián
"""

from flask import Blueprint, request, jsonify
from database_manager import db_manager
from datetime import datetime
import traceback

# Blueprint para las rutas de persistencia
persistence_api = Blueprint('persistence', __name__, url_prefix='/api/persistence')

# === ENDPOINTS DE PROYECTOS ===

@persistence_api.route('/projects', methods=['GET'])
def get_projects():
    """Obtiene todos los proyectos"""
    try:
        limit = request.args.get('limit', 50, type=int)
        projects = db_manager.get_all_projects(limit)
        
        return jsonify({
            'success': True,
            'projects': projects,
            'count': len(projects)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects', methods=['POST'])
def create_project():
    """Crea un nuevo proyecto"""
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        if not name:
            return jsonify({
                'success': False,
                'error': 'El nombre del proyecto es requerido'
            }), 400
        
        description = data.get('description', '')
        project_type = data.get('type', 'guardian_script')
        tags = data.get('tags', [])
        metadata = data.get('metadata', {})
        
        project_id = db_manager.create_project(
            name=name,
            description=description,
            project_type=project_type,
            tags=tags,
            metadata=metadata
        )
        
        # Obtener el proyecto creado
        project = db_manager.get_project(project_id)
        
        return jsonify({
            'success': True,
            'project': project,
            'message': f'Proyecto "{name}" creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Obtiene un proyecto específico"""
    try:
        project = db_manager.get_project(project_id)
        
        if not project:
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404
        
        # Actualizar último acceso
        db_manager.update_project_access(project_id)
        
        return jsonify({
            'success': True,
            'project': project
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Actualiza un proyecto"""
    try:
        data = request.get_json()
        
        # Validar que el proyecto existe
        if not db_manager.get_project(project_id):
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404
        
        # Actualizar proyecto
        success = db_manager.update_project(project_id, **data)
        
        if success:
            project = db_manager.get_project(project_id)
            return jsonify({
                'success': True,
                'project': project,
                'message': 'Proyecto actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el proyecto'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Elimina un proyecto"""
    try:
        # Validar que el proyecto existe
        project = db_manager.get_project(project_id)
        if not project:
            return jsonify({
                'success': False,
                'error': 'Proyecto no encontrado'
            }), 404
        
        success = db_manager.delete_project(project_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Proyecto "{project["name"]}" eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el proyecto'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS DE ARCHIVOS ===

@persistence_api.route('/projects/<int:project_id>/files', methods=['GET'])
def get_project_files(project_id):
    """Obtiene los archivos de un proyecto"""
    try:
        files = db_manager.get_project_files(project_id)
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects/<int:project_id>/files', methods=['POST'])
def create_project_file(project_id):
    """Crea un archivo en un proyecto"""
    try:
        data = request.get_json()
        
        filename = data.get('filename', '').strip()
        content = data.get('content', '')
        file_type = data.get('file_type', 'guardian')
        
        if not filename:
            return jsonify({
                'success': False,
                'error': 'El nombre del archivo es requerido'
            }), 400
        
        file_id = db_manager.create_project_file(project_id, filename, content, file_type)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'message': f'Archivo "{filename}" creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/files/<int:file_id>', methods=['PUT'])
def update_project_file(file_id):
    """Actualiza el contenido de un archivo"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        success = db_manager.update_project_file(file_id, content)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Archivo actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el archivo'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/projects/<int:project_id>/save', methods=['POST'])
def save_project_content(project_id):
    """Guarda el contenido actual del proyecto (auto-save)"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        description = data.get('description', 'Auto-guardado')
        auto_save = data.get('auto_save', True)
        
        # Actualizar archivo principal
        files = db_manager.get_project_files(project_id)
        main_file = next((f for f in files if f['filename'].startswith('main.')), None)
        
        if main_file:
            db_manager.update_project_file(main_file['id'], content)
        else:
            db_manager.create_project_file(project_id, 'main.guardian', content, 'guardian')
        
        # Crear versión
        content_snapshot = {
            'main_content': content,
            'timestamp': datetime.now().isoformat(),
            'files': files
        }
        
        version_id = db_manager.create_version(
            project_id, 
            content_snapshot, 
            description, 
            auto_save
        )
        
        return jsonify({
            'success': True,
            'version_id': version_id,
            'message': 'Proyecto guardado exitosamente'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS DE VERSIONES ===

@persistence_api.route('/projects/<int:project_id>/versions', methods=['GET'])
def get_project_versions(project_id):
    """Obtiene las versiones de un proyecto"""
    try:
        limit = request.args.get('limit', 20, type=int)
        versions = db_manager.get_project_versions(project_id, limit)
        
        return jsonify({
            'success': True,
            'versions': versions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS DE CONVERSACIONES ===

@persistence_api.route('/conversations', methods=['GET'])
def get_conversations():
    """Obtiene las conversaciones recientes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        conversations = db_manager.get_recent_conversations(limit)
        
        return jsonify({
            'success': True,
            'conversations': conversations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/conversations', methods=['POST'])
def create_conversation():
    """Crea una nueva conversación"""
    try:
        data = request.get_json()
        
        project_id = data.get('project_id')
        conversation_type = data.get('type', 'general')
        title = data.get('title', f'Conversación {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        conversation_id = db_manager.create_conversation(project_id, conversation_type, title)
        
        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'message': 'Conversación creada exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Obtiene los mensajes de una conversación"""
    try:
        messages = db_manager.get_conversation_messages(conversation_id)
        
        return jsonify({
            'success': True,
            'messages': messages
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def add_conversation_message(conversation_id):
    """Añade un mensaje a una conversación"""
    try:
        data = request.get_json()
        
        sender = data.get('sender', 'user')
        message = data.get('message', '')
        metadata = data.get('metadata', {})
        
        if not message.strip():
            return jsonify({
                'success': False,
                'error': 'El mensaje no puede estar vacío'
            }), 400
        
        message_id = db_manager.add_message(conversation_id, sender, message, metadata)
        
        return jsonify({
            'success': True,
            'message_id': message_id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS DE BOTS ===

@persistence_api.route('/bots', methods=['GET'])
def get_created_bots():
    """Obtiene los bots creados"""
    try:
        project_id = request.args.get('project_id', type=int)
        bots = db_manager.get_created_bots(project_id)
        
        return jsonify({
            'success': True,
            'bots': bots
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/bots', methods=['POST'])
def save_created_bot():
    """Guarda un bot creado"""
    try:
        data = request.get_json()
        
        project_id = data.get('project_id')
        name = data.get('name', '').strip()
        template_type = data.get('template_type', 'custom')
        configuration = data.get('configuration', {})
        generated_code = data.get('generated_code', '')
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'El nombre del bot es requerido'
            }), 400
        
        if not generated_code:
            return jsonify({
                'success': False,
                'error': 'El código generado es requerido'
            }), 400
        
        bot_id = db_manager.save_created_bot(
            project_id, name, template_type, configuration, generated_code
        )
        
        return jsonify({
            'success': True,
            'bot_id': bot_id,
            'message': f'Bot "{name}" guardado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINTS DE CONFIGURACIÓN ===

@persistence_api.route('/settings/<setting_key>', methods=['GET'])
def get_setting(setting_key):
    """Obtiene una configuración"""
    try:
        value = db_manager.get_setting(setting_key)
        
        return jsonify({
            'success': True,
            'key': setting_key,
            'value': value
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@persistence_api.route('/settings/<setting_key>', methods=['PUT'])
def set_setting(setting_key):
    """Establece una configuración"""
    try:
        data = request.get_json()
        value = data.get('value')
        
        db_manager.set_setting(setting_key, value)
        
        return jsonify({
            'success': True,
            'message': f'Configuración "{setting_key}" actualizada'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === ENDPOINT DE ESTADO ===

@persistence_api.route('/status', methods=['GET'])
def get_persistence_status():
    """Obtiene el estado del sistema de persistencia"""
    try:
        # Obtener estadísticas básicas
        projects = db_manager.get_all_projects(limit=1)
        conversations = db_manager.get_recent_conversations(limit=1)
        bots = db_manager.get_created_bots()
        
        return jsonify({
            'success': True,
            'status': 'active',
            'statistics': {
                'total_projects': len(db_manager.get_all_projects(limit=1000)),
                'total_conversations': len(db_manager.get_recent_conversations(limit=1000)),
                'total_bots': len(bots),
                'database_path': db_manager.db_path
            },
            'settings': {
                'auto_save_interval': db_manager.get_setting('auto_save_interval', 30),
                'max_versions_per_project': db_manager.get_setting('max_versions_per_project', 50)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === MANEJO DE ERRORES ===

@persistence_api.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@persistence_api.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500
