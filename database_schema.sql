-- Esquema de Base de Datos para IDE Guardián
-- Sistema de Persistencia de Proyectos

-- Tabla de Proyectos
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL DEFAULT 'guardian_script', -- 'guardian_script', 'bot_project', 'conversation'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_favorite BOOLEAN DEFAULT FALSE,
    tags TEXT, -- JSON array de tags
    metadata TEXT -- JSON con metadatos específicos del proyecto
);

-- Tabla de Archivos de Proyecto
CREATE TABLE IF NOT EXISTS project_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    file_type TEXT NOT NULL DEFAULT 'guardian', -- 'guardian', 'config', 'log', 'output'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Tabla de Versiones (Historial)
CREATE TABLE IF NOT EXISTS project_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    content_snapshot TEXT NOT NULL, -- JSON con todo el contenido del proyecto
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    auto_save BOOLEAN DEFAULT TRUE, -- TRUE para auto-guardado, FALSE para guardado manual
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

-- Tabla de Conversaciones de IA
CREATE TABLE IF NOT EXISTS ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    conversation_type TEXT NOT NULL DEFAULT 'general', -- 'general', 'bot_creation', 'help', 'debugging'
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
);

-- Tabla de Mensajes de Conversación
CREATE TABLE IF NOT EXISTS conversation_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender TEXT NOT NULL, -- 'user', 'assistant', 'system'
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT, -- JSON con metadatos del mensaje (contexto, archivos adjuntos, etc.)
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations (id) ON DELETE CASCADE
);

-- Tabla de Bots Creados
CREATE TABLE IF NOT EXISTS created_bots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    template_type TEXT NOT NULL, -- 'network_monitoring', 'incident_response', 'custom'
    configuration TEXT NOT NULL, -- JSON con la configuración del bot
    generated_code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deployed BOOLEAN DEFAULT FALSE,
    deployment_info TEXT, -- JSON con información de despliegue
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL
);

-- Tabla de Configuraciones de Usuario
CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_projects_updated_at ON projects (updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_projects_type ON projects (type);
CREATE INDEX IF NOT EXISTS idx_project_files_project_id ON project_files (project_id);
CREATE INDEX IF NOT EXISTS idx_project_versions_project_id ON project_versions (project_id, version_number DESC);
CREATE INDEX IF NOT EXISTS idx_ai_conversations_project_id ON ai_conversations (project_id);
CREATE INDEX IF NOT EXISTS idx_conversation_messages_conversation_id ON conversation_messages (conversation_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_created_bots_project_id ON created_bots (project_id);

-- Triggers para actualizar timestamps automáticamente
CREATE TRIGGER IF NOT EXISTS update_projects_timestamp 
    AFTER UPDATE ON projects
    BEGIN
        UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_project_files_timestamp 
    AFTER UPDATE ON project_files
    BEGIN
        UPDATE project_files SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        UPDATE projects SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.project_id;
    END;

CREATE TRIGGER IF NOT EXISTS update_ai_conversations_timestamp 
    AFTER UPDATE ON ai_conversations
    BEGIN
        UPDATE ai_conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_created_bots_timestamp 
    AFTER UPDATE ON created_bots
    BEGIN
        UPDATE created_bots SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Insertar configuraciones por defecto
INSERT OR IGNORE INTO user_settings (setting_key, setting_value) VALUES 
    ('auto_save_interval', '30'),
    ('max_versions_per_project', '50'),
    ('default_project_type', 'guardian_script'),
    ('theme', 'dark'),
    ('editor_font_size', '14');
