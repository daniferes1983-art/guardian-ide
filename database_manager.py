"""
Gestor de Base de Datos para IDE Guardián
Sistema de Persistencia de Proyectos
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

class DatabaseManager:
    def __init__(self, db_path: str = "guardian_ide.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con el esquema"""
        try:
            with open('database_schema.sql', 'r', encoding='utf-8') as f:
                schema = f.read()
            
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.commit()
            conn.close()
            print(f"Base de datos inicializada: {self.db_path}")
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        return conn
    
    # === GESTIÓN DE PROYECTOS ===
    
    def create_project(self, name: str, description: str = "", project_type: str = "guardian_script", 
                      tags: List[str] = None, metadata: Dict = None) -> int:
        """Crea un nuevo proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (name, description, type, tags, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name, 
                description, 
                project_type,
                json.dumps(tags or []),
                json.dumps(metadata or {})
            ))
            project_id = cursor.lastrowid
            conn.commit()
            
            # Crear archivo principal por defecto
            self.create_project_file(project_id, "main.guardian", "# Nuevo proyecto Guardián\\n", "guardian")
            
            return project_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """Obtiene un proyecto por ID"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            
            if row:
                project = dict(row)
                project['tags'] = json.loads(project['tags'] or '[]')
                project['metadata'] = json.loads(project['metadata'] or '{}')
                
                # Obtener archivos del proyecto
                project['files'] = self.get_project_files(project_id)
                
                return project
            return None
        finally:
            conn.close()
    
    def get_all_projects(self, limit: int = 50) -> List[Dict]:
        """Obtiene todos los proyectos ordenados por última actualización"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM projects 
                ORDER BY updated_at DESC 
                LIMIT ?
            """, (limit,))
            
            projects = []
            for row in cursor.fetchall():
                project = dict(row)
                project['tags'] = json.loads(project['tags'] or '[]')
                project['metadata'] = json.loads(project['metadata'] or '{}')
                projects.append(project)
            
            return projects
        finally:
            conn.close()
    
    def update_project(self, project_id: int, **kwargs) -> bool:
        """Actualiza un proyecto"""
        conn = self.get_connection()
        try:
            # Construir query dinámicamente
            fields = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['name', 'description', 'type', 'is_favorite']:
                    fields.append(f"{key} = ?")
                    values.append(value)
                elif key in ['tags', 'metadata']:
                    fields.append(f"{key} = ?")
                    values.append(json.dumps(value))
            
            if not fields:
                return False
            
            values.append(project_id)
            query = f"UPDATE projects SET {', '.join(fields)} WHERE id = ?"
            
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def delete_project(self, project_id: int) -> bool:
        """Elimina un proyecto y todos sus datos relacionados"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def update_project_access(self, project_id: int):
        """Actualiza el timestamp de último acceso"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE projects 
                SET last_accessed = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (project_id,))
            conn.commit()
        finally:
            conn.close()
    
    # === GESTIÓN DE ARCHIVOS DE PROYECTO ===
    
    def create_project_file(self, project_id: int, filename: str, content: str, 
                           file_type: str = "guardian") -> int:
        """Crea un archivo en un proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO project_files (project_id, filename, content, file_type)
                VALUES (?, ?, ?, ?)
            """, (project_id, filename, content, file_type))
            file_id = cursor.lastrowid
            conn.commit()
            return file_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_project_files(self, project_id: int) -> List[Dict]:
        """Obtiene todos los archivos de un proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM project_files 
                WHERE project_id = ? 
                ORDER BY filename
            """, (project_id,))
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def update_project_file(self, file_id: int, content: str) -> bool:
        """Actualiza el contenido de un archivo"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE project_files 
                SET content = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (content, file_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_main_file_content(self, project_id: int) -> str:
        """Obtiene el contenido del archivo principal del proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT content FROM project_files 
                WHERE project_id = ? AND filename LIKE 'main.%'
                ORDER BY created_at ASC
                LIMIT 1
            """, (project_id,))
            
            row = cursor.fetchone()
            return row['content'] if row else ""
        finally:
            conn.close()
    
    # === GESTIÓN DE VERSIONES ===
    
    def create_version(self, project_id: int, content_snapshot: Dict, 
                      description: str = "", auto_save: bool = True) -> int:
        """Crea una nueva versión del proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Obtener el siguiente número de versión
            cursor.execute("""
                SELECT COALESCE(MAX(version_number), 0) + 1 
                FROM project_versions 
                WHERE project_id = ?
            """, (project_id,))
            version_number = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO project_versions 
                (project_id, version_number, content_snapshot, description, auto_save)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, version_number, json.dumps(content_snapshot), description, auto_save))
            
            version_id = cursor.lastrowid
            conn.commit()
            
            # Limpiar versiones antiguas si hay demasiadas
            self._cleanup_old_versions(project_id)
            
            return version_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_project_versions(self, project_id: int, limit: int = 20) -> List[Dict]:
        """Obtiene las versiones de un proyecto"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM project_versions 
                WHERE project_id = ? 
                ORDER BY version_number DESC 
                LIMIT ?
            """, (project_id, limit))
            
            versions = []
            for row in cursor.fetchall():
                version = dict(row)
                version['content_snapshot'] = json.loads(version['content_snapshot'])
                versions.append(version)
            
            return versions
        finally:
            conn.close()
    
    def _cleanup_old_versions(self, project_id: int):
        """Limpia versiones antiguas manteniendo solo las más recientes"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            
            # Obtener configuración de máximo de versiones
            cursor.execute("""
                SELECT setting_value FROM user_settings 
                WHERE setting_key = 'max_versions_per_project'
            """)
            row = cursor.fetchone()
            max_versions = int(row['setting_value']) if row else 50
            
            # Eliminar versiones antiguas
            cursor.execute("""
                DELETE FROM project_versions 
                WHERE project_id = ? AND id NOT IN (
                    SELECT id FROM project_versions 
                    WHERE project_id = ? 
                    ORDER BY version_number DESC 
                    LIMIT ?
                )
            """, (project_id, project_id, max_versions))
            
            conn.commit()
        finally:
            conn.close()
    
    # === GESTIÓN DE CONVERSACIONES ===
    
    def create_conversation(self, project_id: Optional[int] = None, 
                           conversation_type: str = "general", title: str = "") -> int:
        """Crea una nueva conversación"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ai_conversations (project_id, conversation_type, title)
                VALUES (?, ?, ?)
            """, (project_id, conversation_type, title))
            conversation_id = cursor.lastrowid
            conn.commit()
            return conversation_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def add_message(self, conversation_id: int, sender: str, message: str, 
                   metadata: Dict = None) -> int:
        """Añade un mensaje a una conversación"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversation_messages (conversation_id, sender, message, metadata)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, sender, message, json.dumps(metadata or {})))
            message_id = cursor.lastrowid
            conn.commit()
            return message_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        """Obtiene todos los mensajes de una conversación"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM conversation_messages 
                WHERE conversation_id = ? 
                ORDER BY timestamp ASC
            """, (conversation_id,))
            
            messages = []
            for row in cursor.fetchall():
                message = dict(row)
                message['metadata'] = json.loads(message['metadata'] or '{}')
                messages.append(message)
            
            return messages
        finally:
            conn.close()
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Obtiene las conversaciones más recientes"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.*, p.name as project_name
                FROM ai_conversations c
                LEFT JOIN projects p ON c.project_id = p.id
                WHERE c.is_active = TRUE
                ORDER BY c.updated_at DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    # === GESTIÓN DE BOTS ===
    
    def save_created_bot(self, project_id: Optional[int], name: str, template_type: str,
                        configuration: Dict, generated_code: str) -> int:
        """Guarda un bot creado"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO created_bots 
                (project_id, name, template_type, configuration, generated_code)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, name, template_type, json.dumps(configuration), generated_code))
            bot_id = cursor.lastrowid
            conn.commit()
            return bot_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_created_bots(self, project_id: Optional[int] = None) -> List[Dict]:
        """Obtiene los bots creados"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if project_id:
                cursor.execute("""
                    SELECT * FROM created_bots 
                    WHERE project_id = ? 
                    ORDER BY created_at DESC
                """, (project_id,))
            else:
                cursor.execute("""
                    SELECT * FROM created_bots 
                    ORDER BY created_at DESC
                """)
            
            bots = []
            for row in cursor.fetchall():
                bot = dict(row)
                bot['configuration'] = json.loads(bot['configuration'])
                bot['deployment_info'] = json.loads(bot['deployment_info'] or '{}')
                bots.append(bot)
            
            return bots
        finally:
            conn.close()
    
    # === CONFIGURACIONES ===
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Obtiene una configuración"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_value FROM user_settings WHERE setting_key = ?", (key,))
            row = cursor.fetchone()
            return row['setting_value'] if row else default
        finally:
            conn.close()
    
    def set_setting(self, key: str, value: Any):
        """Establece una configuración"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_settings (setting_key, setting_value)
                VALUES (?, ?)
            """, (key, str(value)))
            conn.commit()
        finally:
            conn.close()

# Instancia global del gestor de base de datos
db_manager = DatabaseManager()
