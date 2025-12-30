/**
 * Sistema de Validación en Tiempo Real para Guardián IDE
 * Proporciona resaltado de sintaxis, detección de errores y sugerencias
 */

class RealTimeValidator {
    constructor(editorElement, outputElement) {
        this.editor = editorElement;
        this.output = outputElement;
        this.validationTimeout = null;
        this.lastValidation = null;
        
        // Palabras clave del lenguaje
        this.keywords = new Set([
            'analizar', 'crear', 'listar', 'mostrar', 'responder', 'cancelar',
            'leer', 'monitorear', 'alertar', 'ver', 'detectar', 'evaluar',
            'predecir', 'generar', 'optimizar', 'recomendar'
        ]);
        
        // Subcomandos
        this.subcommands = {
            'analizar': ['puertos', 'amenazas', 'trafico'],
            'crear': ['regla', 'firewall', 'bot'],
            'generar': ['reglas', 'informe'],
            'monitorear': ['trafico', 'con'],
            'detectar': ['anomalias'],
            'evaluar': ['vulnerabilidades'],
            'predecir': ['ataques'],
            'optimizar': ['politicas'],
            'recomendar': ['acciones'],
            'leer': ['logs'],
            'ver': ['procesos'],
            'alertar': ['con']
        };
        
        // Parámetros válidos
        this.parameters = new Set([
            'de', 'en', 'puerto', 'protocolo', 'accion', 'nivel',
            'basado', 'patrones', 'historicos', 'para', 'inteligentes',
            'con', 'ia', 'tiempo', 'real'
        ]);
        
        // Inicializar listeners
        this.init();
    }
    
    init() {
        // Validar mientras se escribe
        this.editor.addEventListener('input', () => this.onInput());
        this.editor.addEventListener('keyup', () => this.onKeyUp());
        
        // Mostrar sugerencias con Ctrl+Space
        this.editor.addEventListener('keydown', (e) => this.onKeyDown(e));
    }
    
    onInput() {
        // Debounce la validación
        clearTimeout(this.validationTimeout);
        this.validationTimeout = setTimeout(() => {
            this.validate();
        }, 300);
    }
    
    onKeyUp() {
        // Resaltar sintaxis mientras se escribe
        this.highlightSyntax();
    }
    
    onKeyDown(e) {
        // Ctrl+Space para autocompletado
        if (e.ctrlKey && e.code === 'Space') {
            e.preventDefault();
            this.showAutocompleteSuggestions();
        }
    }
    
    validate() {
        const text = this.editor.value;
        
        if (!text.trim()) {
            this.clearValidationDisplay();
            return;
        }
        
        // Enviar al servidor para validación
        fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: text })
        })
        .then(response => response.json())
        .then(data => {
            this.lastValidation = data;
            this.displayValidationResults(data);
            this.highlightErrors(data);
        })
        .catch(error => console.error('Error en validación:', error));
    }
    
    displayValidationResults(validationData) {
        const container = document.getElementById('validationContainer') || this.createValidationContainer();
        
        // Limpiar contenido anterior
        container.innerHTML = '';
        
        // Mostrar estado general
        const statusDiv = document.createElement('div');
        statusDiv.className = validationData.valid ? 'validation-status valid' : 'validation-status invalid';
        statusDiv.innerHTML = validationData.valid ? 
            '<i class="fas fa-check-circle"></i> Sintaxis correcta' :
            '<i class="fas fa-exclamation-circle"></i> Errores encontrados';
        container.appendChild(statusDiv);
        
        // Mostrar errores
        if (validationData.errors && validationData.errors.length > 0) {
            const errorsDiv = document.createElement('div');
            errorsDiv.className = 'validation-errors';
            errorsDiv.innerHTML = '<h4>Errores:</h4>';
            
            validationData.errors.forEach(error => {
                const errorItem = document.createElement('div');
                errorItem.className = 'error-item';
                errorItem.innerHTML = `
                    <span class="error-type">${error.type}</span>
                    <span class="error-message">${error.message}</span>
                    <span class="error-location">Línea ${error.line}, Col ${error.column}</span>
                `;
                errorsDiv.appendChild(errorItem);
            });
            
            container.appendChild(errorsDiv);
        }
        
        // Mostrar advertencias
        if (validationData.warnings && validationData.warnings.length > 0) {
            const warningsDiv = document.createElement('div');
            warningsDiv.className = 'validation-warnings';
            warningsDiv.innerHTML = '<h4>Advertencias:</h4>';
            
            validationData.warnings.forEach(warning => {
                const warningItem = document.createElement('div');
                warningItem.className = 'warning-item';
                warningItem.innerHTML = `
                    <span class="warning-type">${warning.type}</span>
                    <span class="warning-message">${warning.message}</span>
                `;
                warningsDiv.appendChild(warningItem);
            });
            
            container.appendChild(warningsDiv);
        }
        
        // Mostrar sugerencias
        if (validationData.suggestions && validationData.suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'validation-suggestions';
            suggestionsDiv.innerHTML = '<h4>Sugerencias:</h4>';
            
            validationData.suggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.innerHTML = `<i class="fas fa-lightbulb"></i> ${suggestion}`;
                suggestionsDiv.appendChild(suggestionItem);
            });
            
            container.appendChild(suggestionsDiv);
        }
    }
    
    createValidationContainer() {
        const container = document.createElement('div');
        container.id = 'validationContainer';
        container.className = 'validation-container';
        
        // Insertar después del editor
        this.editor.parentElement.insertAdjacentElement('afterend', container);
        
        return container;
    }
    
    highlightSyntax() {
        const text = this.editor.value;
        const lines = text.split('\n');
        
        // Crear HTML con resaltado
        let highlightedHTML = '';
        
        lines.forEach((line, lineNum) => {
            let highlightedLine = this.highlightLine(line);
            highlightedHTML += `<div class="code-line" data-line="${lineNum + 1}">${highlightedLine}</div>`;
        });
        
        // Actualizar elemento de resaltado si existe
        const highlighter = document.getElementById('syntaxHighlighter');
        if (highlighter) {
            highlighter.innerHTML = highlightedHTML;
        }
    }
    
    highlightLine(line) {
        // Resaltar palabras clave
        let highlighted = line;
        
        // Resaltar palabras clave
        this.keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            highlighted = highlighted.replace(regex, `<span class="keyword">${keyword}</span>`);
        });
        
        // Resaltar parámetros
        this.parameters.forEach(param => {
            const regex = new RegExp(`\\b${param}\\b`, 'gi');
            highlighted = highlighted.replace(regex, `<span class="parameter">${param}</span>`);
        });
        
        // Resaltar IPs
        highlighted = highlighted.replace(/\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/g, 
            '<span class="ip">$1</span>');
        
        // Resaltar números
        highlighted = highlighted.replace(/\b(\d+)\b/g, '<span class="number">$1</span>');
        
        // Resaltar strings
        highlighted = highlighted.replace(/"([^"]*)"/g, '<span class="string">"$1"</span>');
        
        return highlighted;
    }
    
    highlightErrors(validationData) {
        // Limpiar resaltado anterior
        this.editor.classList.remove('has-errors');
        
        if (validationData.errors && validationData.errors.length > 0) {
            this.editor.classList.add('has-errors');
            
            // Resaltar líneas con errores
            validationData.errors.forEach(error => {
                const lineNum = error.line;
                const lineElement = document.querySelector(`[data-line="${lineNum}"]`);
                if (lineElement) {
                    lineElement.classList.add('error-line');
                }
            });
        }
    }
    
    clearValidationDisplay() {
        const container = document.getElementById('validationContainer');
        if (container) {
            container.innerHTML = '';
        }
        
        this.editor.classList.remove('has-errors');
        document.querySelectorAll('.error-line').forEach(el => {
            el.classList.remove('error-line');
        });
    }
    
    showAutocompleteSuggestions() {
        const text = this.editor.value;
        const cursorPos = this.editor.selectionStart;
        
        // Obtener palabra actual
        const wordStart = text.lastIndexOf(' ', cursorPos) + 1;
        const currentWord = text.substring(wordStart, cursorPos);
        
        // Obtener tokens antes del cursor
        const tokens = this.tokenize(text.substring(0, cursorPos));
        
        let suggestions = [];
        
        if (tokens.length === 0) {
            // Sugerir palabras clave
            suggestions = Array.from(this.keywords).map(kw => ({
                text: kw,
                type: 'keyword',
                description: `Comando: ${kw}`
            }));
        } else {
            const firstToken = tokens[0];
            
            // Sugerir subcomandos
            if (this.subcommands[firstToken]) {
                suggestions = this.subcommands[firstToken].map(sc => ({
                    text: sc,
                    type: 'subcommand',
                    description: `Subcomando de ${firstToken}`
                }));
            }
            
            // Sugerir parámetros
            this.parameters.forEach(param => {
                suggestions.push({
                    text: param,
                    type: 'parameter',
                    description: `Parámetro: ${param}`
                });
            });
        }
        
        // Filtrar por palabra actual
        suggestions = suggestions.filter(s => 
            s.text.toLowerCase().startsWith(currentWord.toLowerCase())
        );
        
        // Mostrar sugerencias
        if (suggestions.length > 0) {
            this.displayAutocompleteSuggestions(suggestions, wordStart, currentWord);
        }
    }
    
    displayAutocompleteSuggestions(suggestions, insertPos, currentWord) {
        // Crear popup de autocompletado
        const popup = document.getElementById('autocompletePopup') || this.createAutocompletePopup();
        popup.innerHTML = '';
        
        suggestions.slice(0, 10).forEach((suggestion, index) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.innerHTML = `
                <span class="autocomplete-text">${suggestion.text}</span>
                <span class="autocomplete-type">${suggestion.type}</span>
            `;
            
            item.addEventListener('click', () => {
                this.insertSuggestion(suggestion.text, insertPos, currentWord);
                popup.style.display = 'none';
            });
            
            popup.appendChild(item);
        });
        
        // Posicionar popup
        const cursorCoords = this.getCursorCoordinates();
        popup.style.top = (cursorCoords.top + 20) + 'px';
        popup.style.left = cursorCoords.left + 'px';
        popup.style.display = 'block';
    }
    
    createAutocompletePopup() {
        const popup = document.createElement('div');
        popup.id = 'autocompletePopup';
        popup.className = 'autocomplete-popup';
        document.body.appendChild(popup);
        return popup;
    }
    
    insertSuggestion(text, insertPos, currentWord) {
        const before = this.editor.value.substring(0, insertPos);
        const after = this.editor.value.substring(insertPos + currentWord.length);
        
        this.editor.value = before + text + after;
        
        // Mover cursor
        const newPos = insertPos + text.length;
        this.editor.setSelectionRange(newPos, newPos);
        
        // Validar nuevamente
        this.validate();
    }
    
    tokenize(text) {
        const pattern = /\b\w+\b/g;
        const tokens = [];
        let match;
        
        while ((match = pattern.exec(text)) !== null) {
            tokens.push(match[0]);
        }
        
        return tokens;
    }
    
    getCursorCoordinates() {
        const textarea = this.editor;
        const div = document.createElement('div');
        const span = document.createElement('span');
        
        div.style.position = 'absolute';
        div.style.visibility = 'hidden';
        div.style.whiteSpace = 'pre-wrap';
        div.style.wordWrap = 'break-word';
        
        // Copiar estilos del textarea
        const style = window.getComputedStyle(textarea);
        ['direction', 'boxSizing', 'width', 'height', 'overflowX', 'overflowY',
         'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
         'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
         'fontStyle', 'fontVariant', 'fontWeight', 'fontStretch', 'fontSize',
         'fontSizeAdjust', 'lineHeight', 'fontFamily', 'textAlign',
         'textTransform', 'textIndent', 'textDecoration', 'letterSpacing',
         'wordSpacing', 'tabSize'].forEach(prop => {
            div.style[prop] = style[prop];
        });
        
        div.textContent = textarea.value.substring(0, textarea.selectionStart);
        span.textContent = textarea.value.substring(textarea.selectionStart) || '.';
        
        div.appendChild(span);
        document.body.appendChild(div);
        
        const coordinates = {
            top: textarea.offsetTop + span.offsetTop,
            left: textarea.offsetLeft + span.offsetLeft
        };
        
        document.body.removeChild(div);
        
        return coordinates;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const editor = document.getElementById('codeEditor');
    const output = document.getElementById('output');
    
    if (editor && output) {
        window.validator = new RealTimeValidator(editor, output);
    }
});
