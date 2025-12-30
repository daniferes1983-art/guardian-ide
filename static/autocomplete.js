// ===== SISTEMA DE AUTOCOMPLETADO CONTEXTUAL PARA GUARDIÁN IDE =====

// Base de conocimiento de comandos de Guardián
const GUARDIAN_COMMANDS = {
    // Comandos de Análisis y Gestión
    "analizar": {
        syntax: "analizar puertos de [IP]",
        description: "Escanear puertos de una dirección IP específica",
        parameters: ["puertos de"],
        examples: ["analizar puertos de 192.168.1.1", "analizar puertos de 10.0.0.1"],
        category: "analysis",
        icon: "fas fa-search"
    },
    "monitorear": {
        syntax: "monitorear trafico en [interfaz]",
        description: "Monitorear tráfico de red en una interfaz específica",
        parameters: ["trafico en"],
        examples: ["monitorear trafico en eth0", "monitorear trafico en wlan0"],
        category: "analysis",
        icon: "fas fa-chart-line"
    },
    "leer": {
        syntax: "leer logs de [ruta_archivo]",
        description: "Leer y analizar contenido de archivos de log",
        parameters: ["logs de"],
        examples: ["leer logs de /var/log/syslog", "leer logs de /var/log/auth.log"],
        category: "analysis",
        icon: "fas fa-file-alt"
    },
    "ver": {
        syntax: "ver procesos activos",
        description: "Listar todos los procesos activos del sistema",
        parameters: ["procesos"],
        examples: ["ver procesos activos"],
        category: "analysis",
        icon: "fas fa-list"
    },
    
    // Comandos de Escudos y Seguridad
    "crear": {
        syntax: "crear regla firewall puerto: [puerto] protocolo: [protocolo] accion: [accion]",
        description: "Crear una nueva regla de firewall",
        parameters: ["regla firewall", "puerto:", "protocolo:", "accion:"],
        examples: [
            "crear regla firewall puerto: 22 protocolo: TCP accion: bloquear",
            "crear regla firewall puerto: 80 protocolo: TCP accion: permitir"
        ],
        category: "security",
        icon: "fas fa-shield-alt"
    },
    "alertar": {
        syntax: "alertar \"[mensaje]\" nivel: [nivel]",
        description: "Enviar una alerta de seguridad con nivel específico",
        parameters: ["nivel:"],
        examples: [
            "alertar \"Intrusión detectada\" nivel: alto",
            "alertar \"Tráfico sospechoso\" nivel: medio"
        ],
        category: "security",
        icon: "fas fa-exclamation-triangle"
    },
    
    // Comandos de IA
    "detectar": {
        syntax: "detectar anomalias en trafico de [interfaz]",
        description: "Detectar anomalías en el tráfico de red usando IA",
        parameters: ["anomalias en trafico de"],
        examples: ["detectar anomalias en trafico de eth0"],
        category: "ai",
        icon: "fas fa-brain"
    },
    "evaluar": {
        syntax: "evaluar vulnerabilidades de [rango_ip]",
        description: "Evaluar vulnerabilidades en un rango de IPs usando IA",
        parameters: ["vulnerabilidades de"],
        examples: ["evaluar vulnerabilidades de 192.168.1.0/24"],
        category: "ai",
        icon: "fas fa-bug"
    },
    "predecir": {
        syntax: "predecir ataques",
        description: "Predecir posibles ataques usando análisis de IA",
        parameters: ["ataques"],
        examples: ["predecir ataques"],
        category: "ai",
        icon: "fas fa-crystal-ball"
    },
    "generar": {
        syntax: "generar [tipo] [contexto]",
        description: "Generar contenido usando IA",
        parameters: [
            "reglas firewall inteligentes para",
            "informe de riesgo con ia"
        ],
        examples: [
            "generar reglas firewall inteligentes para web_server",
            "generar informe de riesgo con ia"
        ],
        category: "ai",
        icon: "fas fa-magic"
    },
    "optimizar": {
        syntax: "optimizar politicas de seguridad",
        description: "Optimizar políticas de seguridad usando IA",
        parameters: ["politicas de seguridad"],
        examples: ["optimizar politicas de seguridad"],
        category: "ai",
        icon: "fas fa-cogs"
    },
    "recomendar": {
        syntax: "recomendar acciones de mitigacion",
        description: "Recomendar acciones de mitigación usando IA",
        parameters: ["acciones de mitigacion"],
        examples: ["recomendar acciones de mitigacion"],
        category: "ai",
        icon: "fas fa-lightbulb"
    }
};

// Snippets de código predefinidos
const CODE_SNIPPETS = {
    "firewall_basic": {
        name: "Configuración Básica de Firewall",
        description: "Plantilla para configuración básica de firewall",
        code: `# Configuración básica de firewall
crear regla firewall puerto: 22 protocolo: TCP accion: permitir
crear regla firewall puerto: 80 protocolo: TCP accion: permitir
crear regla firewall puerto: 443 protocolo: TCP accion: permitir
alertar "Firewall configurado" nivel: info`,
        category: "security"
    },
    "network_monitoring": {
        name: "Monitoreo de Red Completo",
        description: "Plantilla para monitoreo completo de red",
        code: `# Monitoreo completo de red
monitorear trafico en eth0
detectar anomalias en trafico de eth0
analizar puertos de 192.168.1.1
predecir ataques`,
        category: "analysis"
    },
    "ai_security_scan": {
        name: "Escaneo de Seguridad con IA",
        description: "Plantilla para escaneo completo con IA",
        code: `# Escaneo de seguridad con IA
evaluar vulnerabilidades de 192.168.1.0/24
detectar anomalias en trafico de eth0
predecir ataques
generar informe de riesgo con ia
recomendar acciones de mitigacion`,
        category: "ai"
    }
};

// Valores comunes para parámetros
const PARAMETER_VALUES = {
    "protocolo": ["TCP", "UDP", "ICMP"],
    "accion": ["permitir", "bloquear", "denegar"],
    "nivel": ["bajo", "medio", "alto", "critico"],
    "interfaz": ["eth0", "eth1", "wlan0", "lo"],
    "puerto": ["22", "80", "443", "21", "25", "53", "110", "143", "993", "995"]
};

class GuardianAutocomplete {
    constructor(editor) {
        this.editor = editor;
        this.dropdown = document.getElementById('autocompleteDropdown');
        this.dropdownList = this.dropdown.querySelector('.autocomplete-list');
        this.contextualHelp = document.getElementById('contextualHelp');
        this.helpContent = this.contextualHelp.querySelector('.help-content');
        
        this.selectedIndex = -1;
        this.suggestions = [];
        this.isVisible = false;
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.editor.addEventListener('input', this.handleInput.bind(this));
        this.editor.addEventListener('keydown', this.handleKeydown.bind(this));
        this.editor.addEventListener('click', this.handleClick.bind(this));
        this.editor.addEventListener('blur', this.handleBlur.bind(this));
        document.addEventListener('click', this.handleDocumentClick.bind(this));
    }

    handleInput(event) {
        const cursorPosition = this.editor.selectionStart;
        const text = this.editor.value;
        const context = this.getContext(text, cursorPosition);
        
        if (this.shouldShowAutocomplete(context)) {
            this.showSuggestions(context);
        } else {
            this.hideDropdown();
        }
        
        this.validateSyntax(text);
        this.updateContextualHelp(context);
    }

    handleKeydown(event) {
        if (!this.isVisible) {
            // Ctrl+Space para forzar autocompletado
            if (event.ctrlKey && event.code === 'Space') {
                event.preventDefault();
                this.forceAutocomplete();
                return;
            }
            return;
        }

        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                this.selectNext();
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.selectPrevious();
                break;
            case 'Enter':
            case 'Tab':
                event.preventDefault();
                this.acceptSuggestion();
                break;
            case 'Escape':
                event.preventDefault();
                this.hideDropdown();
                break;
        }
    }

    handleClick(event) {
        const cursorPosition = this.editor.selectionStart;
        const text = this.editor.value;
        const context = this.getContext(text, cursorPosition);
        this.updateContextualHelp(context);
    }

    handleBlur(event) {
        // Delay para permitir clicks en el dropdown
        setTimeout(() => {
            if (!this.dropdown.contains(document.activeElement)) {
                this.hideDropdown();
            }
        }, 150);
    }

    handleDocumentClick(event) {
        if (!this.dropdown.contains(event.target) && event.target !== this.editor) {
            this.hideDropdown();
        }
    }

    getContext(text, position) {
        const lines = text.substring(0, position).split('\n');
        const currentLine = lines[lines.length - 1];
        const words = currentLine.trim().split(/\s+/);
        const lineNumber = lines.length;
        
        return {
            currentLine: currentLine,
            words: words.filter(w => w.length > 0),
            lastWord: words[words.length - 1] || '',
            position: position,
            lineNumber: lineNumber,
            fullText: text
        };
    }

    shouldShowAutocomplete(context) {
        return context.lastWord.length > 0 || 
               context.currentLine.endsWith(' ') ||
               context.currentLine.endsWith(':');
    }

    forceAutocomplete() {
        const cursorPosition = this.editor.selectionStart;
        const text = this.editor.value;
        const context = this.getContext(text, cursorPosition);
        this.showSuggestions(context, true);
    }

    showSuggestions(context, forced = false) {
        this.suggestions = this.getSuggestions(context, forced);
        
        if (this.suggestions.length === 0) {
            this.hideDropdown();
            return;
        }

        this.renderDropdown();
        this.positionDropdown();
        this.isVisible = true;
        this.selectedIndex = -1;
    }

    getSuggestions(context, forced = false) {
        const suggestions = [];
        const { words, lastWord, currentLine } = context;
        
        // Si no hay palabras y se fuerza, mostrar comandos principales
        if (words.length === 0 && forced) {
            Object.keys(GUARDIAN_COMMANDS).forEach(command => {
                suggestions.push({
                    text: command,
                    type: 'command',
                    description: GUARDIAN_COMMANDS[command].description,
                    syntax: GUARDIAN_COMMANDS[command].syntax,
                    icon: GUARDIAN_COMMANDS[command].icon,
                    category: GUARDIAN_COMMANDS[command].category
                });
            });
        }
        
        // Sugerencias de comandos principales
        else if (words.length === 1 || (words.length === 0 && lastWord.length > 0)) {
            Object.keys(GUARDIAN_COMMANDS).forEach(command => {
                if (command.toLowerCase().startsWith(lastWord.toLowerCase())) {
                    suggestions.push({
                        text: command,
                        type: 'command',
                        description: GUARDIAN_COMMANDS[command].description,
                        syntax: GUARDIAN_COMMANDS[command].syntax,
                        icon: GUARDIAN_COMMANDS[command].icon,
                        category: GUARDIAN_COMMANDS[command].category
                    });
                }
            });
        }
        
        // Sugerencias de parámetros
        else if (words.length > 1) {
            const baseCommand = words[0].toLowerCase();
            if (GUARDIAN_COMMANDS[baseCommand]) {
                const params = GUARDIAN_COMMANDS[baseCommand].parameters;
                
                params.forEach(param => {
                    if (param.toLowerCase().includes(lastWord.toLowerCase()) || forced) {
                        suggestions.push({
                            text: param,
                            type: 'parameter',
                            description: `Parámetro para ${baseCommand}`,
                            syntax: GUARDIAN_COMMANDS[baseCommand].syntax,
                            icon: "fas fa-tag",
                            category: GUARDIAN_COMMANDS[baseCommand].category
                        });
                    }
                });
                
                // Sugerencias de valores para parámetros específicos
                if (currentLine.includes(':')) {
                    const paramType = this.getParameterType(currentLine);
                    if (PARAMETER_VALUES[paramType]) {
                        PARAMETER_VALUES[paramType].forEach(value => {
                            if (value.toLowerCase().includes(lastWord.toLowerCase()) || forced) {
                                suggestions.push({
                                    text: value,
                                    type: 'value',
                                    description: `Valor para ${paramType}`,
                                    syntax: value,
                                    icon: "fas fa-quote-right",
                                    category: 'value'
                                });
                            }
                        });
                    }
                }
            }
        }
        
        // Snippets de código si se fuerza el autocompletado
        if (forced && words.length <= 1) {
            Object.keys(CODE_SNIPPETS).forEach(snippetKey => {
                const snippet = CODE_SNIPPETS[snippetKey];
                if (snippet.name.toLowerCase().includes(lastWord.toLowerCase()) || lastWord === '') {
                    suggestions.push({
                        text: snippet.code,
                        type: 'snippet',
                        description: snippet.description,
                        syntax: snippet.name,
                        icon: "fas fa-code",
                        category: snippet.category,
                        isSnippet: true
                    });
                }
            });
        }
        
        return suggestions.slice(0, 15); // Limitar a 15 sugerencias
    }

    getParameterType(line) {
        if (line.includes('protocolo:')) return 'protocolo';
        if (line.includes('accion:')) return 'accion';
        if (line.includes('nivel:')) return 'nivel';
        if (line.includes('puerto:')) return 'puerto';
        return null;
    }

    renderDropdown() {
        this.dropdownList.innerHTML = '';
        
        this.suggestions.forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.dataset.index = index;
            
            const typeClass = suggestion.type;
            const icon = suggestion.icon || 'fas fa-code';
            
            item.innerHTML = `
                <div class="autocomplete-item-title">
                    <i class="${icon}"></i>
                    <span>${suggestion.isSnippet ? suggestion.syntax : suggestion.text}</span>
                    <span class="autocomplete-item-type ${typeClass}">${suggestion.type}</span>
                </div>
                <div class="autocomplete-item-description">${suggestion.description}</div>
                ${!suggestion.isSnippet ? `<div class="autocomplete-item-syntax">${suggestion.syntax}</div>` : ''}
            `;
            
            item.addEventListener('click', () => {
                this.selectedIndex = index;
                this.acceptSuggestion();
            });
            
            item.addEventListener('mouseenter', () => {
                this.selectedIndex = index;
                this.updateSelection();
            });
            
            this.dropdownList.appendChild(item);
        });
    }

    positionDropdown() {
        const editorRect = this.editor.getBoundingClientRect();
        const cursorPosition = this.getCursorPixelPosition();
        
        this.dropdown.style.left = `${cursorPosition.x}px`;
        this.dropdown.style.top = `${cursorPosition.y + 20}px`;
        this.dropdown.classList.remove('hidden');
    }

    getCursorPixelPosition() {
        const editorRect = this.editor.getBoundingClientRect();
        const cursorPosition = this.editor.selectionStart;
        const textBeforeCursor = this.editor.value.substring(0, cursorPosition);
        const lines = textBeforeCursor.split('\n');
        const currentLineIndex = lines.length - 1;
        const currentLineText = lines[currentLineIndex];
        
        // Estimación aproximada de la posición del cursor
        const lineHeight = 22; // Altura de línea aproximada
        const charWidth = 8.4; // Ancho de carácter aproximado
        
        return {
            x: editorRect.left + (currentLineText.length * charWidth) + 60, // +60 por el padding del line numbers
            y: editorRect.top + (currentLineIndex * lineHeight) + 16 // +16 por el padding superior
        };
    }

    selectNext() {
        this.selectedIndex = Math.min(this.selectedIndex + 1, this.suggestions.length - 1);
        this.updateSelection();
    }

    selectPrevious() {
        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
        this.updateSelection();
    }

    updateSelection() {
        const items = this.dropdownList.querySelectorAll('.autocomplete-item');
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === this.selectedIndex);
        });
        
        // Scroll al elemento seleccionado
        if (this.selectedIndex >= 0) {
            const selectedItem = items[this.selectedIndex];
            selectedItem.scrollIntoView({ block: 'nearest' });
        }
    }

    acceptSuggestion() {
        if (this.selectedIndex < 0 || this.selectedIndex >= this.suggestions.length) {
            return;
        }
        
        const suggestion = this.suggestions[this.selectedIndex];
        const cursorPosition = this.editor.selectionStart;
        const text = this.editor.value;
        const context = this.getContext(text, cursorPosition);
        
        let insertText = suggestion.text;
        let newCursorPosition = cursorPosition;
        
        if (suggestion.isSnippet) {
            // Insertar snippet completo
            const beforeCursor = text.substring(0, cursorPosition - context.lastWord.length);
            const afterCursor = text.substring(cursorPosition);
            
            this.editor.value = beforeCursor + insertText + afterCursor;
            newCursorPosition = beforeCursor.length + insertText.length;
        } else {
            // Reemplazar la palabra actual
            const beforeCursor = text.substring(0, cursorPosition - context.lastWord.length);
            const afterCursor = text.substring(cursorPosition);
            
            this.editor.value = beforeCursor + insertText + afterCursor;
            newCursorPosition = beforeCursor.length + insertText.length;
        }
        
        this.editor.setSelectionRange(newCursorPosition, newCursorPosition);
        this.editor.focus();
        this.hideDropdown();
        
        // Trigger input event para actualizar line numbers
        this.editor.dispatchEvent(new Event('input'));
    }

    hideDropdown() {
        this.dropdown.classList.add('hidden');
        this.isVisible = false;
        this.selectedIndex = -1;
    }

    validateSyntax(text) {
        // Implementación básica de validación de sintaxis
        // Esto se puede expandir con reglas más complejas
        const lines = text.split('\n');
        const errors = [];
        
        lines.forEach((line, index) => {
            const trimmedLine = line.trim();
            if (trimmedLine === '' || trimmedLine.startsWith('#')) return;
            
            const words = trimmedLine.split(/\s+/);
            const command = words[0];
            
            if (!GUARDIAN_COMMANDS[command]) {
                errors.push({
                    line: index + 1,
                    message: `Comando desconocido: ${command}`,
                    type: 'error'
                });
            }
        });
        
        // Mostrar errores (implementación básica)
        this.displaySyntaxErrors(errors);
    }

    displaySyntaxErrors(errors) {
        // Implementación básica - se puede mejorar con overlays visuales
        console.log('Errores de sintaxis:', errors);
    }

    updateContextualHelp(context) {
        if (context.words.length === 0) {
            this.helpContent.innerHTML = `
                <h4>Bienvenido al IDE Guardián</h4>
                <p>Comienza escribiendo un comando o presiona <strong>Ctrl+Space</strong> para ver todas las opciones disponibles.</p>
                <div class="syntax-example">Ejemplo: analizar puertos de 192.168.1.1</div>
            `;
            return;
        }
        
        const command = context.words[0].toLowerCase();
        if (GUARDIAN_COMMANDS[command]) {
            const cmd = GUARDIAN_COMMANDS[command];
            this.helpContent.innerHTML = `
                <h4><i class="${cmd.icon}"></i> ${command}</h4>
                <p>${cmd.description}</p>
                <div class="syntax-example">${cmd.syntax}</div>
                <h4>Ejemplos:</h4>
                <ul class="parameter-list">
                    ${cmd.examples.map(example => `<li>${example}</li>`).join('')}
                </ul>
                <h4>Categoría:</h4>
                <p>${this.getCategoryName(cmd.category)}</p>
            `;
        }
    }

    getCategoryName(category) {
        const categories = {
            'analysis': 'Análisis y Gestión',
            'security': 'Escudos y Seguridad',
            'ai': 'Programación y Gestión IA'
        };
        return categories[category] || category;
    }
}

// Inicializar el autocompletado cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    const codeEditor = document.getElementById('codeEditor');
    if (codeEditor) {
        window.guardianAutocomplete = new GuardianAutocomplete(codeEditor);
        console.log('✅ Sistema de autocompletado inicializado');
    }
});

