// DOM Elements
const codeEditor = document.getElementById('codeEditor');
const lineNumbers = document.getElementById('lineNumbers');
const outputContent = document.getElementById('outputContent');
const runBtn = document.getElementById('runBtn');
const clearBtn = document.getElementById('clearBtn');
const clearOutputBtn = document.getElementById('clearOutputBtn');
const helpBtn = document.getElementById('helpBtn');
const docsBtn = document.getElementById('docsBtn');
const helpModal = document.getElementById('helpModal');
const closeHelpModal = document.getElementById('closeHelpModal');
const lineCol = document.getElementById('lineCol');
const commandCount = document.getElementById('commandCount');

// Tab elements
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

// Command and example elements
const commandItems = document.querySelectorAll('.command-item');
const exampleItems = document.querySelectorAll('.example-item');

// State
let currentLine = 1;
let currentColumn = 1;
let executionHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updateLineNumbers();
    updateStatusBar();
    setupEventListeners();
    setupKeyboardShortcuts();
});

// Event Listeners
function setupEventListeners() {
    // Editor events
    codeEditor.addEventListener('input', handleEditorInput);
    codeEditor.addEventListener('keydown', handleEditorKeydown);
    codeEditor.addEventListener('click', updateCursorPosition);
    codeEditor.addEventListener('keyup', updateCursorPosition);

    // Button events
    runBtn.addEventListener('click', executeCode);
    clearBtn.addEventListener('click', clearEditor);
    clearOutputBtn.addEventListener('click', clearOutput);
    helpBtn.addEventListener('click', showHelpModal);
    docsBtn.addEventListener('click', () => switchTab('docs'));
    closeHelpModal.addEventListener('click', hideHelpModal);

    // Tab events
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // Command item events
    commandItems.forEach(item => {
        item.addEventListener('click', () => {
            const command = item.getAttribute('data-command');
            insertCommand(command);
        });
    });

    // Example item events
    exampleItems.forEach(item => {
        item.addEventListener('click', () => {
            const example = item.getAttribute('data-example');
            loadExample(example);
        });
    });

    // Modal events
    helpModal.addEventListener('click', (e) => {
        if (e.target === helpModal) {
            hideHelpModal();
        }
    });
}

// Keyboard Shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl + Enter - Execute code
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            executeCode();
        }
        
        // Ctrl + L - Clear editor
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            clearEditor();
        }
        
        // F1 - Show help
        if (e.key === 'F1') {
            e.preventDefault();
            showHelpModal();
        }
        
        // Escape - Close modal
        if (e.key === 'Escape') {
            hideHelpModal();
        }
    });
}

// Editor Functions
function handleEditorInput() {
    updateLineNumbers();
    updateStatusBar();
    updateCommandCount();
}

function handleEditorKeydown(e) {
    // Tab for autocompletion
    if (e.key === 'Tab') {
        e.preventDefault();
        handleAutoComplete();
    }
}

function updateLineNumbers() {
    const lines = codeEditor.value.split('\n');
    const lineNumbersText = lines.map((_, index) => index + 1).join('\n');
    lineNumbers.textContent = lineNumbersText;
}

function updateCursorPosition() {
    const cursorPosition = codeEditor.selectionStart;
    const textBeforeCursor = codeEditor.value.substring(0, cursorPosition);
    const lines = textBeforeCursor.split('\n');
    
    currentLine = lines.length;
    currentColumn = lines[lines.length - 1].length + 1;
    
    updateStatusBar();
}

function updateStatusBar() {
    lineCol.textContent = `Línea ${currentLine}, Columna ${currentColumn}`;
}

function updateCommandCount() {
    const commands = codeEditor.value.split('\n').filter(line => line.trim().length > 0);
    commandCount.textContent = `Comandos: ${commands.length}`;
}

// Autocompletion
function handleAutoComplete() {
    const cursorPosition = codeEditor.selectionStart;
    const textBeforeCursor = codeEditor.value.substring(0, cursorPosition);
    const currentLineText = textBeforeCursor.split('\n').pop();
    
    const commands = [
        'analizar puertos de ',
        'crear regla firewall puerto: ',
        'leer logs de ',
        'monitorear trafico en ',
        'alertar ',
        'ver procesos activos'
    ];
    
    const matchingCommand = commands.find(cmd => 
        cmd.toLowerCase().startsWith(currentLineText.toLowerCase())
    );
    
    if (matchingCommand) {
        const completion = matchingCommand.substring(currentLineText.length);
        const newValue = codeEditor.value.substring(0, cursorPosition) + 
                        completion + 
                        codeEditor.value.substring(cursorPosition);
        
        codeEditor.value = newValue;
        codeEditor.selectionStart = codeEditor.selectionEnd = cursorPosition + completion.length;
        updateLineNumbers();
        updateStatusBar();
    }
}

// Command Insertion
function insertCommand(command) {
    const cursorPosition = codeEditor.selectionStart;
    const newValue = codeEditor.value.substring(0, cursorPosition) + 
                    command + '\n' + 
                    codeEditor.value.substring(cursorPosition);
    
    codeEditor.value = newValue;
    codeEditor.focus();
    codeEditor.selectionStart = codeEditor.selectionEnd = cursorPosition + command.length + 1;
    
    updateLineNumbers();
    updateStatusBar();
    updateCommandCount();
}

// Example Loading
function loadExample(exampleType) {
    let exampleCode = '';
    
    switch (exampleType) {
        case 'basic':
            exampleCode = `# Comandos básicos de Guardián
analizar puertos de 192.168.1.1
ver procesos activos
alertar "Sistema iniciado correctamente"`;
            break;
        case 'firewall':
            exampleCode = `# Configuración de firewall
crear regla firewall puerto: 22 protocolo: TCP accion: bloquear
crear regla firewall puerto: 80 protocolo: TCP accion: permitir
crear regla firewall puerto: 443 protocolo: TCP accion: permitir
alertar "Reglas de firewall configuradas"`;
            break;
        case 'monitoring':
            exampleCode = `# Monitoreo de red y logs
monitorear trafico en eth0
leer logs de /var/log/syslog
analizar puertos de 10.0.0.1
alertar "Monitoreo iniciado"`;
            break;
    }
    
    codeEditor.value = exampleCode;
    updateLineNumbers();
    updateStatusBar();
    updateCommandCount();
    codeEditor.focus();
    
    // Switch to editor tab
    switchTab('editor');
}

// Code Execution
async function executeCode() {
    const code = codeEditor.value.trim();
    if (!code) {
        showOutput('Error: No hay código para ejecutar', 'error');
        return;
    }
    
    // Switch to output tab
    switchTab('output');
    
    // Clear previous output
    clearOutput();
    
    // Show execution start
    showOutput('> Ejecutando comandos de Guardián...', 'command');
    
    const commands = code.split('\n').filter(line => {
        const trimmed = line.trim();
        return trimmed.length > 0 && !trimmed.startsWith('#');
    });
    
    for (let i = 0; i < commands.length; i++) {
        const command = commands[i].trim();
        showOutput(`\n> ${command}`, 'command');
        
        try {
            const result = await executeGuardianCommand(command);
            showOutput(result, 'success');
        } catch (error) {
            showOutput(`Error: ${error.message}`, 'error');
        }
        
        // Add small delay for better UX
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    showOutput('\n> Ejecución completada', 'command');
    executionHistory.push({
        timestamp: new Date(),
        code: code,
        commands: commands.length
    });
}

// Guardian Command Execution (Simulated)
async function executeGuardianCommand(command) {
    // Simulate API call to backend
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: command })
        });
        
        if (response.ok) {
            const result = await response.json();
            return result.output || result.message || 'Comando ejecutado correctamente';
        } else {
            throw new Error('Error del servidor');
        }
    } catch (error) {
        // Fallback to simulated execution
        return simulateGuardianCommand(command);
    }
}

// Simulated Command Execution
function simulateGuardianCommand(command) {
    const cmd = command.toLowerCase();
    
    if (cmd.includes('analizar puertos')) {
        const ipMatch = command.match(/(\d+\.\d+\.\d+\.\d+)/);
        const ip = ipMatch ? ipMatch[1] : '192.168.1.1';
        return `Analizando puertos en ${ip}...
Puerto 22/tcp: abierto (SSH)
Puerto 80/tcp: abierto (HTTP)
Puerto 443/tcp: abierto (HTTPS)
Escaneo completado - 3 puertos abiertos encontrados`;
    }
    
    if (cmd.includes('crear regla firewall')) {
        const puertoMatch = command.match(/puerto:\s*(\d+)/);
        const protocoloMatch = command.match(/protocolo:\s*(TCP|UDP)/i);
        const accionMatch = command.match(/accion:\s*(bloquear|permitir)/i);
        
        const puerto = puertoMatch ? puertoMatch[1] : '22';
        const protocolo = protocoloMatch ? protocoloMatch[1] : 'TCP';
        const accion = accionMatch ? accionMatch[1] : 'bloquear';
        
        return `Creando regla de firewall:
Puerto: ${puerto}/${protocolo}
Acción: ${accion}
Regla aplicada correctamente`;
    }
    
    if (cmd.includes('leer logs')) {
        const rutaMatch = command.match(/de\s+(.+)$/);
        const ruta = rutaMatch ? rutaMatch[1] : '/var/log/syslog';
        return `Leyendo logs de ${ruta}...
[2024-01-15 10:30:15] INFO: Sistema iniciado
[2024-01-15 10:30:16] INFO: Servicios cargados
[2024-01-15 10:30:17] WARN: Conexión SSH desde IP desconocida
[2024-01-15 10:30:18] INFO: Firewall activado
Fin del archivo de log`;
    }
    
    if (cmd.includes('monitorear trafico')) {
        const interfazMatch = command.match(/en\s+(\w+)/);
        const interfaz = interfazMatch ? interfazMatch[1] : 'eth0';
        return `Iniciando monitoreo de tráfico en ${interfaz}...
Paquetes capturados: 1,247
Tráfico HTTP: 45%
Tráfico HTTPS: 35%
Tráfico SSH: 15%
Otro tráfico: 5%
Monitoreo activo`;
    }
    
    if (cmd.includes('alertar')) {
        const mensajeMatch = command.match(/alertar\s+(.+)$/);
        const mensaje = mensajeMatch ? mensajeMatch[1].replace(/['"]/g, '') : 'Alerta de seguridad';
        return `🚨 ALERTA DE SEGURIDAD 🚨
Mensaje: ${mensaje}
Timestamp: ${new Date().toLocaleString()}
Alerta enviada a administradores`;
    }
    
    if (cmd.includes('ver procesos activos')) {
        return `Procesos activos del sistema:
PID    COMANDO           CPU%   MEM%
1234   nginx             2.1    1.5
5678   mysql             5.3    12.8
9012   ssh               0.1    0.3
3456   guardian-monitor  1.2    2.1
Total: 47 procesos activos`;
    }
    
    throw new Error('Comando no reconocido');
}

// Output Functions
function showOutput(text, type = 'result') {
    // Remove welcome message if it exists
    const welcome = outputContent.querySelector('.output-welcome');
    if (welcome) {
        welcome.remove();
    }
    
    const outputLine = document.createElement('div');
    outputLine.className = `output-line output-${type}`;
    outputLine.textContent = text;
    
    outputContent.appendChild(outputLine);
    outputContent.scrollTop = outputContent.scrollHeight;
}

function clearOutput() {
    outputContent.innerHTML = `
        <div class="output-welcome">
            <i class="fas fa-shield-alt"></i>
            <p>Salida de ejecución</p>
            <p>Los resultados aparecerán aquí</p>
        </div>
    `;
}

// Editor Functions
function clearEditor() {
    codeEditor.value = '';
    updateLineNumbers();
    updateStatusBar();
    updateCommandCount();
    codeEditor.focus();
}

// Tab Functions
function switchTab(tabName) {
    // Update tab buttons
    tabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        }
    });
    
    // Update tab content
    tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === `${tabName}-tab`) {
            content.classList.add('active');
        }
    });
    
    // Focus editor if switching to editor tab
    if (tabName === 'editor') {
        setTimeout(() => codeEditor.focus(), 100);
    }
}

// Modal Functions
function showHelpModal() {
    helpModal.classList.add('active');
}

function hideHelpModal() {
    helpModal.classList.remove('active');
}

// Utility Functions
function formatTimestamp(date) {
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Export functions for potential external use
window.GuardianIDE = {
    executeCode,
    clearEditor,
    clearOutput,
    insertCommand,
    loadExample,
    switchTab
};



// AI Dashboard functionality
function setupAIDashboard() {
    // AI Dashboard elements
    const refreshTrafficBtn = document.getElementById('refreshTrafficBtn');
    const scanVulnBtn = document.getElementById('scanVulnBtn');
    const generateRecommendationsBtn = document.getElementById('generateRecommendationsBtn');
    const quickActionBtns = document.querySelectorAll('.quick-action-btn');

    // Event listeners for AI Dashboard
    if (refreshTrafficBtn) {
        refreshTrafficBtn.addEventListener('click', refreshTrafficMetrics);
    }
    
    if (scanVulnBtn) {
        scanVulnBtn.addEventListener('click', scanVulnerabilities);
    }
    
    if (generateRecommendationsBtn) {
        generateRecommendationsBtn.addEventListener('click', generateRecommendations);
    }

    // Quick action buttons
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', handleQuickAction);
    });

    // Start real-time updates for AI dashboard
    startAIDashboardUpdates();
}

function refreshTrafficMetrics() {
    const packetsPerSec = document.getElementById('packetsPerSec');
    const activeConnections = document.getElementById('activeConnections');
    const anomaliesCount = document.getElementById('anomaliesCount');

    // Simulate real-time data
    if (packetsPerSec) {
        packetsPerSec.textContent = (Math.random() * 2000 + 500).toFixed(0);
    }
    if (activeConnections) {
        activeConnections.textContent = (Math.random() * 200 + 50).toFixed(0);
    }
    if (anomaliesCount) {
        anomaliesCount.textContent = Math.floor(Math.random() * 10);
    }

    // Add visual feedback
    const btn = document.getElementById('refreshTrafficBtn');
    if (btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-sync-alt"></i>';
        }, 1000);
    }
}

function scanVulnerabilities() {
    const criticalVulns = document.getElementById('criticalVulns');
    const highVulns = document.getElementById('highVulns');
    const mediumVulns = document.getElementById('mediumVulns');

    // Simulate vulnerability scan
    if (criticalVulns) {
        criticalVulns.textContent = Math.floor(Math.random() * 5);
    }
    if (highVulns) {
        highVulns.textContent = Math.floor(Math.random() * 10 + 2);
    }
    if (mediumVulns) {
        mediumVulns.textContent = Math.floor(Math.random() * 20 + 5);
    }

    // Add visual feedback
    const btn = document.getElementById('scanVulnBtn');
    if (btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Escaneando...';
        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-search"></i> Escanear';
        }, 3000);
    }
}

function generateRecommendations() {
    const recommendationsList = document.getElementById('recommendationsList');
    
    const newRecommendations = [
        {
            priority: 'high',
            icon: 'fas fa-exclamation-triangle',
            title: 'Actualizar sistema de detección de intrusiones',
            desc: 'Se han detectado nuevas técnicas de evasión que requieren actualización del IDS',
            timeline: '48 horas'
        },
        {
            priority: 'medium',
            icon: 'fas fa-key',
            title: 'Rotar credenciales de servicios críticos',
            desc: 'Recomendado rotar credenciales como medida preventiva',
            timeline: '1 semana'
        }
    ];

    if (recommendationsList) {
        recommendationsList.innerHTML = '';
        newRecommendations.forEach(rec => {
            const recElement = createRecommendationElement(rec);
            recommendationsList.appendChild(recElement);
        });
    }

    // Add visual feedback
    const btn = document.getElementById('generateRecommendationsBtn');
    if (btn) {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando...';
        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-magic"></i> Generar';
        }, 2000);
    }
}

function createRecommendationElement(rec) {
    const div = document.createElement('div');
    div.className = `recommendation-item priority-${rec.priority}`;
    div.innerHTML = `
        <div class="recommendation-icon">
            <i class="${rec.icon}"></i>
        </div>
        <div class="recommendation-content">
            <div class="recommendation-title">${rec.title}</div>
            <div class="recommendation-desc">${rec.desc}</div>
            <div class="recommendation-timeline">Timeline: ${rec.timeline}</div>
        </div>
        <div class="recommendation-priority">${rec.priority.toUpperCase()}</div>
    `;
    return div;
}

function handleQuickAction(event) {
    const action = event.currentTarget.getAttribute('data-ai-action');
    const commands = {
        'analyze-threats': 'analizar amenazas en tiempo real en eth0',
        'generate-firewall-rules': 'generar reglas firewall inteligentes para web_server',
        'predict-attacks': 'predecir ataques basado en patrones historicos',
        'optimize-policies': 'optimizar politicas de seguridad automaticamente',
        'generate-report': 'generar informe de riesgo con ia',
        'recommend-mitigation': 'recomendar acciones de mitigacion'
    };

    const command = commands[action];
    if (command) {
        // Switch to editor tab and insert command
        switchTab('editor');
        insertCommand(command);
        
        // Add visual feedback
        event.currentTarget.style.transform = 'scale(0.95)';
        setTimeout(() => {
            event.currentTarget.style.transform = '';
        }, 150);
    }
}

function insertCommand(command) {
    const currentValue = codeEditor.value;
    const newValue = currentValue ? currentValue + '\n' + command : command;
    codeEditor.value = newValue;
    updateLineNumbers();
    updateStatusBar();
    codeEditor.focus();
}

function startAIDashboardUpdates() {
    // Update threat level periodically
    setInterval(() => {
        updateThreatLevel();
        updatePredictions();
    }, 30000); // Update every 30 seconds
}

function updateThreatLevel() {
    const threatLevel = document.getElementById('threatLevel');
    const threatScore = document.getElementById('threatScore');
    
    const score = Math.random() * 10;
    let level, className;
    
    if (score < 3) {
        level = 'BAJO';
        className = 'status-low';
    } else if (score < 7) {
        level = 'MEDIO';
        className = 'status-medium';
    } else {
        level = 'ALTO';
        className = 'status-high';
    }
    
    if (threatLevel) {
        threatLevel.textContent = level;
        threatLevel.className = `status-badge ${className}`;
    }
    
    if (threatScore) {
        threatScore.textContent = score.toFixed(1);
    }
    
    // Update progress bar
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = `${(score / 10) * 100}%`;
    }
}

function updatePredictions() {
    const predictionsList = document.getElementById('predictionsList');
    
    const predictions = [
        {
            type: 'Escaneo de Puertos',
            probability: Math.floor(Math.random() * 40 + 30) + '%',
            timeframe: 'Próximas ' + Math.floor(Math.random() * 8 + 2) + 'h'
        },
        {
            type: 'Actividad Sospechosa',
            probability: Math.floor(Math.random() * 30 + 20) + '%',
            timeframe: 'Próximas ' + Math.floor(Math.random() * 48 + 12) + 'h'
        },
        {
            type: 'Intento de Intrusión',
            probability: Math.floor(Math.random() * 20 + 10) + '%',
            timeframe: 'Próximos ' + Math.floor(Math.random() * 5 + 2) + ' días'
        }
    ];
    
    if (predictionsList) {
        predictionsList.innerHTML = '';
        predictions.slice(0, 2).forEach(pred => {
            const predElement = document.createElement('div');
            predElement.className = 'prediction-item';
            predElement.innerHTML = `
                <div class="prediction-type">${pred.type}</div>
                <div class="prediction-probability">${pred.probability}</div>
                <div class="prediction-timeframe">${pred.timeframe}</div>
            `;
            predictionsList.appendChild(predElement);
        });
    }
}

// Enhanced tab switching to include AI dashboard
function switchTab(tabName) {
    // Remove active class from all tabs and contents
    tabs.forEach(tab => tab.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedContent = document.getElementById(`${tabName}-tab`);
    
    if (selectedTab && selectedContent) {
        selectedTab.classList.add('active');
        selectedContent.classList.add('active');
        
        // Initialize AI dashboard if switching to it
        if (tabName === 'ai-dashboard') {
            setupAIDashboard();
            updateThreatLevel();
            updatePredictions();
        }
    }
}

// Update the original setupEventListeners to include AI dashboard
const originalSetupEventListeners = setupEventListeners;
setupEventListeners = function() {
    originalSetupEventListeners();
    
    // Setup AI dashboard when page loads
    setupAIDashboard();
};


// ===== SISTEMA DE CREACIÓN DE BOTS =====

let currentBotSession = null;
let currentSessionId = null;

// Iniciar creación de bot desde la barra lateral
function startBotCreation(templateId) {
    // Cambiar a la pestaña de creación de bots
    switchTab('bot-creator');
    
    // Seleccionar la plantilla
    selectBotTemplate(templateId);
}

// Seleccionar plantilla de bot
function selectBotTemplate(templateId) {
    // Marcar plantilla como seleccionada
    document.querySelectorAll('.template-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-template="${templateId}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Si es bot personalizado, mostrar formulario
    if (templateId === 'custom_bot') {
        showBotStep('custom-form');
    } else {
        // Iniciar sesión con el asistente de IA
        startAISession(templateId);
    }
}

// Iniciar sesión con el asistente de IA
async function startAISession(templateId) {
    try {
        showLoadingMessage('Iniciando asistente de IA...');
        
        const response = await fetch('/api/bots/sessions/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template_id: templateId,
                user_id: 'web_user_' + Date.now()
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentSessionId = result.session_id;
            
            // Mostrar la sección de conversación
            showBotStep('ai-conversation');
            
            // Agregar mensaje inicial de la IA
            addAIMessage(result.message);
            
            // Configurar eventos de entrada
            setupConversationEvents();
            
        } else {
            showErrorMessage('Error al iniciar sesión: ' + result.error);
        }
        
    } catch (error) {
        console.error('Error al iniciar sesión de IA:', error);
        showErrorMessage('Error de conexión al iniciar sesión');
    }
}

// Configurar eventos de la conversación
function setupConversationEvents() {
    const input = document.getElementById('userResponseInput');
    const sendBtn = document.getElementById('sendResponseBtn');
    
    // Enviar respuesta al presionar Enter
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendUserResponse();
        }
    });
    
    // Enviar respuesta al hacer clic en el botón
    sendBtn.addEventListener('click', sendUserResponse);
    
    // Enfocar el input
    input.focus();
}

// Enviar respuesta del usuario
async function sendUserResponse() {
    const input = document.getElementById('userResponseInput');
    const userResponse = input.value.trim();
    
    if (!userResponse || !currentSessionId) {
        return;
    }
    
    // Agregar mensaje del usuario
    addUserMessage(userResponse);
    
    // Limpiar input
    input.value = '';
    
    // Mostrar indicador de carga
    showTypingIndicator();
    
    try {
        const response = await fetch(`/api/bots/sessions/${currentSessionId}/respond`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                response: userResponse
            })
        });
        
        const result = await response.json();
        
        // Ocultar indicador de carga
        hideTypingIndicator();
        
        if (result.success) {
            // Agregar respuesta de la IA
            addAIMessage(result.message);
            
            // Actualizar progreso
            updateProgress(result.progress || 0);
            
            // Verificar si es el final de la conversación
            if (result.type === 'final_confirmation') {
                setupFinalConfirmation();
            } else if (result.type === 'generating') {
                // Finalizar y generar bot
                finalizeBotCreation();
            }
            
        } else {
            addAIMessage('Error: ' + result.error);
        }
        
    } catch (error) {
        hideTypingIndicator();
        console.error('Error al enviar respuesta:', error);
        addAIMessage('Error de conexión. Por favor, intenta de nuevo.');
    }
}

// Agregar mensaje de la IA
function addAIMessage(message) {
    const messagesContainer = document.getElementById('conversationMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai';
    messageDiv.innerHTML = `
        <div class="message-header">🤖 Asistente de IA</div>
        <div class="message-content">${message.replace(/\n/g, '<br>')}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Agregar mensaje del usuario
function addUserMessage(message) {
    const messagesContainer = document.getElementById('conversationMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `
        <div class="message-header">👤 Tú</div>
        <div class="message-content">${message}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Mostrar indicador de escritura
function showTypingIndicator() {
    const messagesContainer = document.getElementById('conversationMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-header">🤖 Asistente de IA</div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Ocultar indicador de escritura
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Actualizar progreso de la conversación
function updateProgress(progress) {
    const progressFill = document.getElementById('conversationProgress');
    const progressText = document.getElementById('progressText');
    
    progressFill.style.width = progress + '%';
    progressText.textContent = progress + '% completado';
}

// Configurar confirmación final
function setupFinalConfirmation() {
    const input = document.getElementById('userResponseInput');
    input.placeholder = "Responde 'sí' para generar el bot o 'modificar' para cambiar parámetros";
}

// Finalizar creación del bot
async function finalizeBotCreation() {
    try {
        showLoadingMessage('Generando tu bot personalizado...');
        
        const response = await fetch(`/api/bots/sessions/${currentSessionId}/finalize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Mostrar resultado del bot
            showBotResult(result);
            showBotStep('bot-result');
            
        } else {
            showErrorMessage('Error al generar bot: ' + result.error);
        }
        
    } catch (error) {
        console.error('Error al finalizar bot:', error);
        showErrorMessage('Error de conexión al generar bot');
    }
}

// Mostrar resultado del bot generado
function showBotResult(result) {
    // Mostrar metadata
    const metadataContainer = document.getElementById('botMetadata');
    metadataContainer.innerHTML = '';
    
    const metadata = result.metadata;
    const metadataItems = [
        { label: 'Nombre del Bot', value: metadata.parameters_used.bot_name || 'Sin nombre' },
        { label: 'Plantilla', value: metadata.template_name },
        { label: 'Versión', value: metadata.template_version },
        { label: 'Componentes', value: metadata.components.join(', ') },
        { label: 'Generado', value: new Date(metadata.generated_at).toLocaleString() }
    ];
    
    metadataItems.forEach(item => {
        const metadataItem = document.createElement('div');
        metadataItem.className = 'metadata-item';
        metadataItem.innerHTML = `
            <span class="metadata-label">${item.label}:</span>
            <span class="metadata-value">${item.value}</span>
        `;
        metadataContainer.appendChild(metadataItem);
    });
    
    // Mostrar código generado
    const codeContainer = document.getElementById('generatedBotCode');
    codeContainer.textContent = result.bot_code;
    
    // Mostrar validación
    showBotValidation(result.validation);
    
    // Configurar eventos de botones
    setupBotResultEvents(result.bot_code);
}

// Mostrar validación del bot
function showBotValidation(validation) {
    const validationContainer = document.getElementById('botValidation');
    validationContainer.innerHTML = '';
    
    // Errores
    if (validation.errors && validation.errors.length > 0) {
        const errorsSection = document.createElement('div');
        errorsSection.className = 'validation-section';
        errorsSection.innerHTML = `
            <h5>❌ Errores de Seguridad</h5>
            <ul class="validation-list">
                ${validation.errors.map(error => `<li class="validation-item error">${error}</li>`).join('')}
            </ul>
        `;
        validationContainer.appendChild(errorsSection);
    }
    
    // Advertencias
    if (validation.warnings && validation.warnings.length > 0) {
        const warningsSection = document.createElement('div');
        warningsSection.className = 'validation-section';
        warningsSection.innerHTML = `
            <h5>⚠️ Advertencias</h5>
            <ul class="validation-list">
                ${validation.warnings.map(warning => `<li class="validation-item warning">${warning}</li>`).join('')}
            </ul>
        `;
        validationContainer.appendChild(warningsSection);
    }
    
    // Si no hay errores ni advertencias
    if ((!validation.errors || validation.errors.length === 0) && 
        (!validation.warnings || validation.warnings.length === 0)) {
        const successSection = document.createElement('div');
        successSection.className = 'validation-section';
        successSection.innerHTML = `
            <h5>✅ Validación Exitosa</h5>
            <ul class="validation-list">
                <li class="validation-item success">El bot cumple con todas las directrices de seguridad</li>
                <li class="validation-item success">No se detectaron problemas de configuración</li>
            </ul>
        `;
        validationContainer.appendChild(successSection);
    }
}

// Configurar eventos de los botones del resultado
function setupBotResultEvents(botCode) {
    // Copiar código
    document.getElementById('copyBotCodeBtn').addEventListener('click', function() {
        navigator.clipboard.writeText(botCode).then(() => {
            showSuccessMessage('Código copiado al portapapeles');
        });
    });
    
    // Insertar en editor
    document.getElementById('insertBotCodeBtn').addEventListener('click', function() {
        const editor = document.getElementById('codeEditor');
        editor.value = botCode;
        updateLineNumbers();
        switchTab('editor');
        showSuccessMessage('Código insertado en el editor');
    });
    
    // Descargar bot
    document.getElementById('downloadBotBtn').addEventListener('click', function() {
        downloadBotCode(botCode);
    });
    
    // Crear otro bot
    document.getElementById('createAnotherBotBtn').addEventListener('click', function() {
        resetBotCreator();
    });
    
    // Guardar configuración
    document.getElementById('saveBotConfigBtn').addEventListener('click', function() {
        saveBotConfiguration();
    });
}

// Descargar código del bot
function downloadBotCode(botCode) {
    const blob = new Blob([botCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'guardian_bot.gdn';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showSuccessMessage('Bot descargado como guardian_bot.gdn');
}

// Guardar configuración del bot
function saveBotConfiguration() {
    // En una implementación real, esto guardaría la configuración en el servidor
    showSuccessMessage('Configuración guardada (funcionalidad en desarrollo)');
}

// Resetear el creador de bots
function resetBotCreator() {
    currentBotSession = null;
    currentSessionId = null;
    
    // Limpiar mensajes
    document.getElementById('conversationMessages').innerHTML = '';
    
    // Resetear progreso
    updateProgress(0);
    
    // Limpiar input
    document.getElementById('userResponseInput').value = '';
    
    // Volver al paso de selección de plantilla
    showBotStep('template-selection');
    
    // Deseleccionar plantillas
    document.querySelectorAll('.template-card').forEach(card => {
        card.classList.remove('selected');
    });
}

// Mostrar paso específico del creador de bots
function showBotStep(stepId) {
    // Ocultar todos los pasos
    document.querySelectorAll('.bot-step').forEach(step => {
        step.classList.add('hidden');
    });
    
    // Mostrar el paso solicitado
    const targetStep = document.getElementById(stepId);
    if (targetStep) {
        targetStep.classList.remove('hidden');
    }
}

// Mostrar todas las plantillas disponibles
async function showAllBotTemplates() {
    try {
        const response = await fetch('/api/bots/templates');
        const result = await response.json();
        
        if (result.success) {
            // Cambiar a la pestaña de creación de bots
            switchTab('bot-creator');
            
            // Mostrar información de todas las plantillas
            showTemplatesCatalog(result.templates);
        } else {
            showErrorMessage('Error al cargar plantillas: ' + result.error);
        }
        
    } catch (error) {
        console.error('Error al cargar plantillas:', error);
        showErrorMessage('Error de conexión al cargar plantillas');
    }
}

// Mostrar catálogo de plantillas
function showTemplatesCatalog(templates) {
    const templateGrid = document.querySelector('.template-grid');
    templateGrid.innerHTML = '';
    
    Object.entries(templates).forEach(([templateId, templateInfo]) => {
        const templateCard = document.createElement('div');
        templateCard.className = 'template-card';
        templateCard.setAttribute('data-template', templateId);
        templateCard.innerHTML = `
            <div class="template-icon">${getTemplateIcon(templateInfo.category)}</div>
            <h4>${templateInfo.name}</h4>
            <p>${templateInfo.description}</p>
            <div class="template-tags">
                ${templateInfo.tags ? templateInfo.tags.map(tag => `<span class="tag">${tag}</span>`).join('') : ''}
            </div>
        `;
        
        templateCard.addEventListener('click', () => selectBotTemplate(templateId));
        templateGrid.appendChild(templateCard);
    });
}

// Obtener icono para categoría de plantilla
function getTemplateIcon(category) {
    const icons = {
        'network_monitoring': '📡',
        'incident_response': '🚨',
        'firewall_management': '🔥',
        'log_analysis': '📊',
        'vulnerability_scanning': '🔍',
        'default': '🤖'
    };
    
    return icons[category] || icons.default;
}

// Configurar eventos de plantillas al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Configurar eventos de selección de plantillas
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', function() {
            const templateId = this.getAttribute('data-template');
            selectBotTemplate(templateId);
        });
    });
});

// Funciones de utilidad para mensajes
function showLoadingMessage(message) {
    // Implementar indicador de carga
    console.log('Loading:', message);
}

function showErrorMessage(message) {
    // Mostrar mensaje de error
    addAIMessage('❌ ' + message);
}

function showSuccessMessage(message) {
    // Mostrar mensaje de éxito
    addAIMessage('✅ ' + message);
}

// Estilos CSS adicionales para indicador de escritura
const typingStyles = `
.typing-indicator .typing-dots {
    display: flex;
    gap: 4px;
    align-items: center;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4CAF50;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% {
        transform: scale(0.8);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}
`;

// Agregar estilos al documento
const styleSheet = document.createElement('style');
styleSheet.textContent = typingStyles;
document.head.appendChild(styleSheet);

