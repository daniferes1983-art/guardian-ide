from flask import Flask, render_template_string, request, jsonify
import time
import json

app = Flask(__name__)

# Almacenamiento en memoria para conversaciones y proyectos
conversations = {}
projects = {}

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guardián IDE - Entorno de Desarrollo para Ciberseguridad</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* === HEADER RESPONSIVO === */
        .header {
            background: rgba(0, 0, 0, 0.2);
            padding: 1rem;
            text-align: center;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        
        .header h1 {
            font-size: clamp(1.5rem, 4vw, 2.5rem);
            margin-bottom: 0.5rem;
        }
        
        .header p {
            opacity: 0.8;
            font-size: clamp(0.9rem, 2vw, 1.1rem);
        }
        
        /* === MENÚ HAMBURGUESA === */
        .hamburger {
            display: none;
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 4px;
            transition: background 0.3s ease;
        }
        
        .hamburger:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .hamburger span {
            display: block;
            width: 25px;
            height: 3px;
            background: white;
            margin: 5px 0;
            transition: 0.3s;
        }
        
        .hamburger.active span:nth-child(1) {
            transform: rotate(-45deg) translate(-5px, 6px);
        }
        
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        
        .hamburger.active span:nth-child(3) {
            transform: rotate(45deg) translate(-5px, -6px);
        }
        
        /* === CONTENEDOR PRINCIPAL === */
        .container {
            display: flex;
            height: calc(100vh - 120px);
            position: relative;
        }
        
        /* === SIDEBAR RESPONSIVO === */
        .sidebar {
            width: 300px;
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            overflow-y: auto;
            border-right: 2px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
            z-index: 1000;
        }
        
        .sidebar-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
        
        /* === CONTENIDO PRINCIPAL === */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            min-width: 0;
        }
        
        /* === PESTAÑAS ADAPTATIVAS === */
        .tabs {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            overflow-x: auto;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        
        .tabs::-webkit-scrollbar {
            display: none;
        }
        
        .tab {
            padding: 1rem 2rem;
            background: transparent;
            border: none;
            color: #ffffff;
            cursor: pointer;
            font-size: 1rem;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            white-space: nowrap;
            flex-shrink: 0;
            min-width: 120px;
            text-align: center;
        }
        
        .tab:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .tab.active {
            background: rgba(255, 255, 255, 0.1);
            border-bottom-color: #4CAF50;
        }
        
        .tab-content {
            flex: 1;
            padding: 1rem;
            display: none;
            overflow-y: auto;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* === CATEGORÍAS DEL SIDEBAR === */
        .category {
            margin-bottom: 1.5rem;
        }
        
        .category-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .command-item {
            background: rgba(255, 255, 255, 0.05);
            margin: 0.3rem 0;
            padding: 0.8rem;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }
        
        .command-item:hover {
            background: rgba(255, 255, 255, 0.15);
            border-left-color: #4CAF50;
            transform: translateX(5px);
        }
        
        .command-name {
            font-weight: bold;
            margin-bottom: 0.3rem;
        }
        
        .command-desc {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        /* === EDITOR Y CONTROLES === */
        .editor-container {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .editor-toolbar {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            min-height: 44px;
            min-width: 44px;
        }
        
        .btn:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: #2196F3;
        }
        
        .btn-secondary:hover {
            background: #1976D2;
        }
        
        .editor {
            width: 100%;
            height: 300px;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            color: #ffffff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            padding: 1rem;
            resize: vertical;
            min-height: 200px;
        }
        
        .output {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
        }
        
        /* === CHAT Y CONVERSACIONES === */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
            margin-bottom: 1rem;
            max-height: 400px;
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 0.8rem;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .message.user {
            background: #4CAF50;
            margin-left: auto;
            text-align: right;
        }
        
        .message.assistant {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .chat-input-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .chat-input {
            flex: 1;
            padding: 0.8rem;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            font-size: 1rem;
            min-width: 200px;
        }
        
        /* === CREACIÓN DE BOTS === */
        .bot-templates {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .bot-template {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .bot-template:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: #4CAF50;
            transform: translateY(-5px);
        }
        
        .bot-template h3 {
            margin-bottom: 0.5rem;
            color: #4CAF50;
        }
        
        /* === GUÍA DE COMANDOS === */
        .guide-section {
            margin-bottom: 2rem;
        }
        
        .guide-section h3 {
            color: #4CAF50;
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }
        
        .command-example {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            font-family: 'Courier New', monospace;
            border-left: 4px solid #4CAF50;
        }
        
        /* === MEDIA QUERIES RESPONSIVOS === */
        
        /* Tablets y pantallas medianas */
        @media (max-width: 1024px) {
            .sidebar {
                width: 250px;
            }
            
            .tab {
                padding: 0.8rem 1.5rem;
                font-size: 0.9rem;
            }
            
            .bot-templates {
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            }
        }
        
        /* Móviles y pantallas pequeñas */
        @media (max-width: 768px) {
            .hamburger {
                display: block;
            }
            
            .sidebar {
                position: fixed;
                top: 0;
                left: 0;
                height: 100vh;
                transform: translateX(-100%);
                z-index: 1001;
                width: 280px;
            }
            
            .sidebar.open {
                transform: translateX(0);
            }
            
            .sidebar-overlay.active {
                display: block;
            }
            
            .main-content {
                width: 100%;
            }
            
            .tabs {
                flex-wrap: nowrap;
                overflow-x: auto;
            }
            
            .tab {
                padding: 0.8rem 1rem;
                font-size: 0.9rem;
                min-width: 100px;
            }
            
            .editor-toolbar {
                justify-content: center;
            }
            
            .btn {
                padding: 0.7rem 1.2rem;
                font-size: 0.9rem;
            }
            
            .chat-input-container {
                flex-direction: column;
            }
            
            .chat-input {
                min-width: 100%;
            }
            
            .bot-templates {
                grid-template-columns: 1fr;
            }
            
            .message {
                max-width: 95%;
            }
        }
        
        /* Móviles muy pequeños */
        @media (max-width: 480px) {
            .header {
                padding: 0.8rem;
            }
            
            .container {
                height: calc(100vh - 100px);
            }
            
            .sidebar {
                width: 100%;
            }
            
            .tab {
                padding: 0.6rem 0.8rem;
                font-size: 0.8rem;
                min-width: 80px;
            }
            
            .tab-content {
                padding: 0.8rem;
            }
            
            .btn {
                padding: 0.6rem 1rem;
                font-size: 0.8rem;
            }
            
            .editor {
                height: 250px;
                font-size: 12px;
            }
            
            .command-item {
                padding: 0.6rem;
            }
            
            .category-title {
                font-size: 1rem;
            }
        }
        
        /* Modo landscape en móviles */
        @media (max-height: 500px) and (orientation: landscape) {
            .header {
                padding: 0.5rem;
            }
            
            .header h1 {
                font-size: 1.5rem;
                margin-bottom: 0.2rem;
            }
            
            .container {
                height: calc(100vh - 80px);
            }
            
            .editor {
                height: 200px;
            }
            
            .chat-messages {
                max-height: 200px;
            }
        }
        
        /* Mejoras táctiles */
        @media (hover: none) and (pointer: coarse) {
            .command-item:hover {
                transform: none;
            }
            
            .command-item:active {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(0.98);
            }
            
            .btn:hover {
                transform: none;
            }
            
            .btn:active {
                transform: scale(0.95);
            }
            
            .tab:hover {
                background: transparent;
            }
            
            .tab:active {
                background: rgba(255, 255, 255, 0.15);
            }
        }
        
        /* Scrollbars personalizados para webkit */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <div class="header">
        <button class="hamburger" onclick="toggleSidebar()">
            <span></span>
            <span></span>
            <span></span>
        </button>
        <h1>🛡️ Guardián IDE</h1>
        <p>Entorno de Desarrollo Integrado para Ciberseguridad con IA</p>
    </div>
    
    <div class="container">
        <div class="sidebar-overlay" onclick="closeSidebar()"></div>
        
        <div class="sidebar" id="sidebar">
            <div class="category">
                <div class="category-title">
                    📊 Análisis y Gestión
                </div>
                <div class="command-item" onclick="insertCommand('analizar puertos de ')">
                    <div class="command-name">analizar puertos</div>
                    <div class="command-desc">Escanear puertos de una IP</div>
                </div>
                <div class="command-item" onclick="insertCommand('monitorear trafico en ')">
                    <div class="command-name">monitorear trafico</div>
                    <div class="command-desc">Monitorear tráfico de red</div>
                </div>
                <div class="command-item" onclick="insertCommand('leer logs de ')">
                    <div class="command-name">leer logs</div>
                    <div class="command-desc">Leer archivos de log</div>
                </div>
                <div class="command-item" onclick="insertCommand('ver procesos activos')">
                    <div class="command-name">ver procesos</div>
                    <div class="command-desc">Listar procesos activos</div>
                </div>
            </div>
            
            <div class="category">
                <div class="category-title">
                    🛡️ Escudos y Seguridad
                </div>
                <div class="command-item" onclick="insertCommand('crear regla firewall puerto: ')">
                    <div class="command-name">crear regla firewall</div>
                    <div class="command-desc">Crear regla de firewall</div>
                </div>
                <div class="command-item" onclick="insertCommand('alertar ')">
                    <div class="command-name">alertar</div>
                    <div class="command-desc">Enviar alerta de seguridad</div>
                </div>
            </div>
            
            <div class="category">
                <div class="category-title">
                    🧠 Programación y Gestión IA
                </div>
                <div class="command-item" onclick="insertCommand('analizar amenazas en tiempo real en ')">
                    <div class="command-name">analizar amenazas IA</div>
                    <div class="command-desc">Análisis de amenazas con IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('detectar anomalias en trafico de ')">
                    <div class="command-name">detectar anomalias</div>
                    <div class="command-desc">Detección de anomalías con IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('evaluar vulnerabilidades de ')">
                    <div class="command-name">evaluar vulnerabilidades</div>
                    <div class="command-desc">Escaneo inteligente de vulnerabilidades</div>
                </div>
                <div class="command-item" onclick="insertCommand('predecir ataques')">
                    <div class="command-name">predecir ataques</div>
                    <div class="command-desc">Predicción de ataques con IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('generar reglas firewall inteligentes para ')">
                    <div class="command-name">generar reglas IA</div>
                    <div class="command-desc">Generación inteligente de reglas</div>
                </div>
                <div class="command-item" onclick="insertCommand('optimizar politicas de seguridad')">
                    <div class="command-name">optimizar politicas</div>
                    <div class="command-desc">Optimización automática con IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('monitorear con ia la red ')">
                    <div class="command-name">monitoreo IA</div>
                    <div class="command-desc">Monitoreo avanzado con IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('generar informe de riesgo con ia')">
                    <div class="command-name">informe de riesgo</div>
                    <div class="command-desc">Informe de riesgo generado por IA</div>
                </div>
                <div class="command-item" onclick="insertCommand('recomendar acciones de mitigacion')">
                    <div class="command-name">recomendaciones IA</div>
                    <div class="command-desc">Recomendaciones de mitigación</div>
                </div>
            </div>
            
            <div class="category">
                <div class="category-title">
                    💻 Ejemplos
                </div>
                <div class="command-item" onclick="loadExample('basic')">
                    <div class="command-name">Comandos Básicos</div>
                    <div class="command-desc">Ejemplos de comandos básicos</div>
                </div>
                <div class="command-item" onclick="loadExample('firewall')">
                    <div class="command-name">Configuración Firewall</div>
                    <div class="command-desc">Ejemplos de configuración de firewall</div>
                </div>
                <div class="command-item" onclick="loadExample('monitoring')">
                    <div class="command-name">Monitoreo de Red</div>
                    <div class="command-desc">Ejemplos de monitoreo de red</div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('editor')">📝 Editor</button>
                <button class="tab" onclick="switchTab('output')">📤 Salida</button>
                <button class="tab" onclick="switchTab('guide')">📚 Guía</button>
                <button class="tab" onclick="switchTab('assistant')">🤖 Asistente IA</button>
                <button class="tab" onclick="switchTab('bots')">🤖 Crear Bots</button>
            </div>
            
            <div id="editor-content" class="tab-content active">
                <div class="editor-container">
                    <div class="editor-toolbar">
                        <button class="btn" onclick="executeCommand()">▶️ Ejecutar</button>
                        <button class="btn btn-secondary" onclick="clearEditor()">🗑️ Limpiar</button>
                        <button class="btn btn-secondary" onclick="saveProject()">💾 Guardar</button>
                    </div>
                    <textarea id="editor" class="editor" placeholder="Escribe tus comandos de Guardián aquí...

Ejemplo:
analizar puertos de 192.168.1.1
crear regla firewall puerto: 22 protocolo: TCP accion: bloquear"></textarea>
                    <div id="output" class="output">Bienvenido al IDE Guardián 🛡️

Listo para ejecutar comandos de ciberseguridad.
Usa el menú lateral para insertar comandos o escribe directamente en el editor.</div>
                </div>
            </div>
            
            <div id="output-content" class="tab-content">
                <h2>📤 Salida de Comandos</h2>
                <div id="command-output" class="output">No hay salida disponible. Ejecuta un comando primero.</div>
            </div>
            
            <div id="guide-content" class="tab-content">
                <h2>📚 Guía de Comandos de Guardián</h2>
                
                <div class="guide-section">
                    <h3>📊 Comandos de Análisis y Gestión</h3>
                    <div class="command-example">
                        <strong>analizar puertos de [IP]</strong><br>
                        Ejemplo: analizar puertos de 192.168.1.1<br>
                        Escanea los puertos abiertos de una dirección IP específica.
                    </div>
                    <div class="command-example">
                        <strong>monitorear trafico en [interfaz]</strong><br>
                        Ejemplo: monitorear trafico en eth0<br>
                        Inicia el monitoreo del tráfico de red en una interfaz.
                    </div>
                    <div class="command-example">
                        <strong>leer logs de [ruta]</strong><br>
                        Ejemplo: leer logs de /var/log/syslog<br>
                        Lee y analiza archivos de log del sistema.
                    </div>
                    <div class="command-example">
                        <strong>ver procesos activos</strong><br>
                        Muestra una lista de todos los procesos activos en el sistema.
                    </div>
                </div>
                
                <div class="guide-section">
                    <h3>🛡️ Comandos de Escudos y Seguridad</h3>
                    <div class="command-example">
                        <strong>crear regla firewall puerto: [puerto] protocolo: [TCP/UDP] accion: [permitir/bloquear]</strong><br>
                        Ejemplo: crear regla firewall puerto: 22 protocolo: TCP accion: bloquear<br>
                        Crea una regla de firewall para controlar el tráfico.
                    </div>
                    <div class="command-example">
                        <strong>alertar "[mensaje]" nivel: [bajo/medio/alto/critico]</strong><br>
                        Ejemplo: alertar "Intrusión detectada" nivel: alto<br>
                        Envía una alerta de seguridad con el nivel especificado.
                    </div>
                </div>
                
                <div class="guide-section">
                    <h3>🧠 Comandos de IA Avanzados</h3>
                    <div class="command-example">
                        <strong>analizar amenazas en tiempo real en [interfaz]</strong><br>
                        Ejemplo: analizar amenazas en tiempo real en eth0<br>
                        Utiliza IA para detectar amenazas en tiempo real.
                    </div>
                    <div class="command-example">
                        <strong>detectar anomalias en trafico de [interfaz]</strong><br>
                        Ejemplo: detectar anomalias en trafico de wlan0<br>
                        Detecta patrones anómalos usando machine learning.
                    </div>
                    <div class="command-example">
                        <strong>generar reglas firewall inteligentes para [contexto]</strong><br>
                        Ejemplo: generar reglas firewall inteligentes para servidor web<br>
                        Genera reglas de firewall optimizadas con IA.
                    </div>
                </div>
            </div>
            
            <div id="assistant-content" class="tab-content">
                <h2>🤖 Asistente IA de Guardián</h2>
                <div class="chat-container">
                    <div id="chat-messages" class="chat-messages">
                        <div class="message assistant">
                            ¡Hola! Soy tu asistente de IA especializado en ciberseguridad. Puedo ayudarte con:
                            <br><br>
                            • Explicar comandos de Guardián<br>
                            • Sugerir mejores prácticas de seguridad<br>
                            • Ayudarte a crear scripts de seguridad<br>
                            • Resolver problemas de configuración<br>
                            <br>
                            ¿En qué puedo ayudarte hoy?
                        </div>
                    </div>
                    <div class="chat-input-container">
                        <input type="text" id="chat-input" class="chat-input" placeholder="Escribe tu pregunta aquí..." onkeypress="handleChatKeyPress(event)">
                        <button class="btn" onclick="sendChatMessage()">Enviar</button>
                    </div>
                </div>
            </div>
            
            <div id="bots-content" class="tab-content">
                <h2>🤖 Creación de Bots de Seguridad</h2>
                <p>Selecciona una plantilla para crear tu bot de seguridad personalizado:</p>
                
                <div class="bot-templates">
                    <div class="bot-template" onclick="createBot('network_monitoring')">
                        <h3>🌐 Bot de Monitoreo de Red</h3>
                        <p>Crea un bot que vigile automáticamente el tráfico de red, detecte ataques DDoS y genere alertas en tiempo real.</p>
                        <p><strong>Características:</strong> Análisis de tráfico, detección de anomalías, alertas automáticas</p>
                    </div>
                    
                    <div class="bot-template" onclick="createBot('incident_response')">
                        <h3>🚨 Bot de Respuesta a Incidentes</h3>
                        <p>Desarrolla un bot que responda automáticamente a amenazas de seguridad, bloquee IPs maliciosas y escale alertas críticas.</p>
                        <p><strong>Características:</strong> Respuesta automática, bloqueo de amenazas, escalación de alertas</p>
                    </div>
                    
                    <div class="bot-template" onclick="createBot('custom')">
                        <h3>⚙️ Bot Personalizado</h3>
                        <p>Crea un bot completamente personalizado según tus necesidades específicas de ciberseguridad.</p>
                        <p><strong>Características:</strong> Configuración flexible, funcionalidades a medida, asistencia de IA</p>
                    </div>
                </div>
                
                <div id="bot-creation-area" style="display: none;">
                    <h3>🤖 Asistente de Creación de Bots</h3>
                    <div class="chat-container">
                        <div id="bot-chat-messages" class="chat-messages">
                            <!-- Los mensajes del asistente aparecerán aquí -->
                        </div>
                        <div class="chat-input-container">
                            <input type="text" id="bot-chat-input" class="chat-input" placeholder="Responde a las preguntas del asistente..." onkeypress="handleBotChatKeyPress(event)">
                            <button class="btn" onclick="sendBotChatMessage()">Enviar</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentBotType = null;
        let botConversationId = null;
        
        // === FUNCIONES DE NAVEGACIÓN ===
        
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const hamburger = document.querySelector('.hamburger');
            
            sidebar.classList.toggle('open');
            overlay.classList.toggle('active');
            hamburger.classList.toggle('active');
        }
        
        function closeSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.querySelector('.sidebar-overlay');
            const hamburger = document.querySelector('.hamburger');
            
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
            hamburger.classList.remove('active');
        }
        
        function switchTab(tabName) {
            // Ocultar todos los contenidos
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Desactivar todas las pestañas
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Mostrar el contenido seleccionado
            document.getElementById(tabName + '-content').classList.add('active');
            
            // Activar la pestaña seleccionada
            event.target.classList.add('active');
            
            // Cerrar sidebar en móviles
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
        }
        
        // === FUNCIONES DEL EDITOR ===
        
        function insertCommand(command) {
            const editor = document.getElementById('editor');
            const cursorPos = editor.selectionStart;
            const textBefore = editor.value.substring(0, cursorPos);
            const textAfter = editor.value.substring(cursorPos);
            
            editor.value = textBefore + command + textAfter;
            editor.focus();
            editor.setSelectionRange(cursorPos + command.length, cursorPos + command.length);
            
            // Cerrar sidebar en móviles
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
        }
        
        function executeCommand() {
            const editor = document.getElementById('editor');
            const output = document.getElementById('output');
            const commandOutput = document.getElementById('command-output');
            const command = editor.value.trim();
            
            if (!command) {
                alert('Por favor, escribe un comando primero.');
                return;
            }
            
            // Simular ejecución del comando
            const timestamp = new Date().toLocaleString();
            let result = '';
            
            if (command.includes('analizar puertos')) {
                const ip = command.match(/analizar puertos de (.+)/)?.[1] || 'IP_DESCONOCIDA';
                result = `[${timestamp}] Analizando puertos de ${ip}...

Puertos abiertos encontrados:
22/tcp   SSH     OpenSSH 8.2
80/tcp   HTTP    Apache 2.4.41
443/tcp  HTTPS   Apache 2.4.41
3306/tcp MySQL   MySQL 8.0.25

Análisis completado. 4 puertos abiertos detectados.`;
            } else if (command.includes('monitorear trafico')) {
                const interfaz = command.match(/monitorear trafico en (.+)/)?.[1] || 'INTERFAZ_DESCONOCIDA';
                result = `[${timestamp}] Iniciando monitoreo de tráfico en ${interfaz}...

Estadísticas de tráfico:
- Paquetes recibidos: 1,247
- Paquetes enviados: 892
- Bytes totales: 2.3 MB
- Conexiones activas: 15

Monitoreo activo. Presiona Ctrl+C para detener.`;
            } else if (command.includes('crear regla firewall')) {
                result = `[${timestamp}] Creando regla de firewall...

Regla creada exitosamente:
${command}

Estado: ACTIVA
ID de regla: FW_001_${Date.now()}
Aplicada a: iptables`;
            } else if (command.includes('analizar amenazas')) {
                result = `[${timestamp}] Analizando amenazas con IA...

🤖 Análisis de IA completado:
- Amenazas detectadas: 2
- Nivel de riesgo: MEDIO
- Recomendación: Revisar conexiones sospechosas

Detalles:
1. Conexión desde IP 192.168.1.100 - Patrón anómalo
2. Tráfico inusual en puerto 8080 - Posible escaneo`;
            } else {
                result = `[${timestamp}] Ejecutando: ${command}

Comando procesado exitosamente.
Estado: OK`;
            }
            
            output.textContent = result;
            commandOutput.textContent = result;
            
            // Cambiar a la pestaña de salida automáticamente
            switchTab('output');
        }
        
        function clearEditor() {
            document.getElementById('editor').value = '';
            document.getElementById('output').textContent = 'Editor limpiado. Listo para nuevos comandos.';
        }
        
        function saveProject() {
            const content = document.getElementById('editor').value;
            if (!content.trim()) {
                alert('No hay contenido para guardar.');
                return;
            }
            
            // Simular guardado
            const projectName = prompt('Nombre del proyecto:', 'Mi_Proyecto_Guardian');
            if (projectName) {
                document.getElementById('output').textContent = `Proyecto "${projectName}" guardado exitosamente.
Contenido: ${content.length} caracteres
Fecha: ${new Date().toLocaleString()}`;
                alert(`Proyecto "${projectName}" guardado exitosamente.`);
            }
        }
        
        function loadExample(type) {
            const editor = document.getElementById('editor');
            let example = '';
            
            switch(type) {
                case 'basic':
                    example = `# Comandos básicos de Guardián
analizar puertos de 192.168.1.1
ver procesos activos
leer logs de /var/log/syslog`;
                    break;
                case 'firewall':
                    example = `# Configuración de Firewall
crear regla firewall puerto: 22 protocolo: TCP accion: bloquear
crear regla firewall puerto: 80 protocolo: TCP accion: permitir
crear regla firewall puerto: 443 protocolo: TCP accion: permitir
alertar "Firewall configurado" nivel: medio`;
                    break;
                case 'monitoring':
                    example = `# Monitoreo de Red con IA
monitorear trafico en eth0
analizar amenazas en tiempo real en eth0
detectar anomalias en trafico de eth0
generar informe de riesgo con ia`;
                    break;
            }
            
            editor.value = example;
            switchTab('editor');
            
            // Cerrar sidebar en móviles
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
        }
        
        // === FUNCIONES DEL CHAT ===
        
        function handleChatKeyPress(event) {
            if (event.key === 'Enter') {
                sendChatMessage();
            }
        }
        
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            const chatMessages = document.getElementById('chat-messages');
            
            // Añadir mensaje del usuario
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = message;
            chatMessages.appendChild(userMessage);
            
            // Limpiar input
            input.value = '';
            
            // Simular respuesta del asistente
            setTimeout(() => {
                const assistantMessage = document.createElement('div');
                assistantMessage.className = 'message assistant';
                
                let response = '';
                if (message.toLowerCase().includes('firewall')) {
                    response = `Para crear reglas de firewall, usa: **crear regla firewall puerto: [puerto] protocolo: [TCP/UDP] accion: [permitir/bloquear]**

Ejemplos:
• crear regla firewall puerto: 22 protocolo: TCP accion: bloquear
• crear regla firewall puerto: 80 protocolo: TCP accion: permitir

¿Necesitas ayuda con algún puerto específico?`;
                } else if (message.toLowerCase().includes('monitoreo') || message.toLowerCase().includes('trafico')) {
                    response = `Para monitorear tráfico de red, puedes usar:

• **monitorear trafico en [interfaz]** - Monitoreo básico
• **analizar amenazas en tiempo real en [interfaz]** - Con IA
• **detectar anomalias en trafico de [interfaz]** - Detección inteligente

¿Qué interfaz de red quieres monitorear?`;
                } else {
                    response = `Entiendo tu consulta sobre "${message}". 

Como asistente especializado en ciberseguridad, puedo ayudarte con:
• Comandos de Guardián
• Configuración de seguridad
• Análisis de amenazas
• Creación de bots de seguridad

¿Podrías ser más específico sobre lo que necesitas?`;
                }
                
                assistantMessage.innerHTML = response;
                chatMessages.appendChild(assistantMessage);
                
                // Scroll al final
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
            
            // Scroll al final
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // === FUNCIONES DE CREACIÓN DE BOTS ===
        
        function createBot(type) {
            currentBotType = type;
            const creationArea = document.getElementById('bot-creation-area');
            const chatMessages = document.getElementById('bot-chat-messages');
            
            creationArea.style.display = 'block';
            chatMessages.innerHTML = '';
            
            let initialMessage = '';
            switch(type) {
                case 'network_monitoring':
                    initialMessage = `🌐 **Creando Bot de Monitoreo de Red**

¡Perfecto! Vamos a crear tu bot de monitoreo de red personalizado. Te haré algunas preguntas para configurarlo correctamente.

**Pregunta 1:** ¿Cómo quieres llamar a tu bot de monitoreo?`;
                    break;
                case 'incident_response':
                    initialMessage = `🚨 **Creando Bot de Respuesta a Incidentes**

¡Excelente elección! Vamos a configurar tu bot de respuesta automática a incidentes.

**Pregunta 1:** ¿Qué nombre le darás a tu bot de respuesta a incidentes?`;
                    break;
                case 'custom':
                    initialMessage = `⚙️ **Creando Bot Personalizado**

¡Genial! Vamos a crear un bot completamente personalizado según tus necesidades.

**Pregunta 1:** ¿Cómo se llamará tu bot personalizado?`;
                    break;
            }
            
            const assistantMessage = document.createElement('div');
            assistantMessage.className = 'message assistant';
            assistantMessage.innerHTML = initialMessage;
            chatMessages.appendChild(assistantMessage);
        }
        
        function handleBotChatKeyPress(event) {
            if (event.key === 'Enter') {
                sendBotChatMessage();
            }
        }
        
        function sendBotChatMessage() {
            const input = document.getElementById('bot-chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            const chatMessages = document.getElementById('bot-chat-messages');
            
            // Añadir mensaje del usuario
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = message;
            chatMessages.appendChild(userMessage);
            
            // Limpiar input
            input.value = '';
            
            // Simular respuesta del asistente
            setTimeout(() => {
                const assistantMessage = document.createElement('div');
                assistantMessage.className = 'message assistant';
                
                let response = `¡Perfecto! Has elegido el nombre "${message}" para tu bot.

**Pregunta 2:** ¿Qué interfaz de red quieres que monitoree? (ejemplo: eth0, wlan0, etc.)`;
                
                assistantMessage.innerHTML = response;
                chatMessages.appendChild(assistantMessage);
                
                // Scroll al final
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
            
            // Scroll al final
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // === EVENTOS DE REDIMENSIONAMIENTO ===
        
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                closeSidebar();
            }
        });
        
        // === INICIALIZACIÓN ===
        
        document.addEventListener('DOMContentLoaded', function() {
            // Configurar el editor por defecto
            document.getElementById('editor').focus();
        });
    </script>
</body>
</html>
    ''')

@app.route('/api/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    command = data.get('command', '')
    
    # Simulación de ejecución de comandos
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    if 'analizar puertos' in command:
        result = f"[{timestamp}] Ejecutando: {command}\\n\\nPuertos abiertos encontrados:\\n22/tcp SSH OpenSSH 8.2\\n80/tcp HTTP Apache 2.4\\n443/tcp HTTPS Apache 2.4\\n\\nAnálisis completado."
    elif 'monitorear trafico' in command:
        result = f"[{timestamp}] Ejecutando: {command}\\n\\nMonitoreo iniciado...\\nPaquetes: 1,247 recibidos, 892 enviados\\nConexiones activas: 15\\n\\nMonitoreo en progreso."
    else:
        result = f"[{timestamp}] Ejecutando: {command}\\n\\nComando procesado exitosamente.\\nEstado: OK"
    
    return jsonify({'success': True, 'output': result})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    # Simulación de respuesta de IA
    if 'firewall' in message.lower():
        response = "Para crear reglas de firewall, usa: **crear regla firewall puerto: [puerto] protocolo: [TCP/UDP] accion: [permitir/bloquear]**\\n\\nEjemplos:\\n• crear regla firewall puerto: 22 protocolo: TCP accion: bloquear\\n• crear regla firewall puerto: 80 protocolo: TCP accion: permitir"
    elif 'monitoreo' in message.lower():
        response = "Para monitorear tráfico, puedes usar:\\n• **monitorear trafico en [interfaz]** - Monitoreo básico\\n• **analizar amenazas en tiempo real en [interfaz]** - Con IA\\n• **detectar anomalias en trafico de [interfaz]** - Detección inteligente"
    else:
        response = f"Entiendo tu consulta sobre '{message}'. Como asistente de ciberseguridad, puedo ayudarte con comandos de Guardián, configuración de seguridad y análisis de amenazas. ¿Podrías ser más específico?"
    
    return jsonify({'success': True, 'response': response})

@app.route('/api/bot/chat', methods=['POST'])
def bot_chat():
    data = request.get_json()
    message = data.get('message', '')
    
    # Simulación de conversación para creación de bots
    response = f"¡Perfecto! Has respondido '{message}'. Continuemos con la configuración de tu bot..."
    
    return jsonify({'success': True, 'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
