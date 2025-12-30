/**
 * Gestor de Formulario de Bot Personalizado
 * Maneja la creación de bots personalizados con asistencia de IA
 */

class CustomBotFormManager {
    constructor() {
        this.currentTemplate = null;
        this.formData = {};
        this.aiSuggestions = null;
        this.init();
    }
    
    init() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Escuchar cambios en el formulario
        document.addEventListener('change', (e) => {
            if (e.target.closest('#custom-form')) {
                this.updateFormData();
                this.updateAISuggestions();
            }
        });
        
        document.addEventListener('input', (e) => {
            if (e.target.closest('#custom-form')) {
                this.updateFormData();
                this.updateAISuggestions();
            }
        });
        
        // Botón de generar bot
        const generateBtn = document.getElementById('generateCustomBotBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateBot());
        }
        
        // Botón de volver
        const backBtn = document.getElementById('backToTemplateBtn');
        if (backBtn) {
            backBtn.addEventListener('click', () => this.backToTemplate());
        }
        
        // Slider de sensibilidad
        const sensitivitySlider = document.getElementById('sensitivity');
        if (sensitivitySlider) {
            sensitivitySlider.addEventListener('input', (e) => {
                document.getElementById('sensitivityValue').textContent = e.target.value;
            });
        }
    }
    
    updateFormData() {
        const form = document.getElementById('custom-form');
        if (!form) return;
        
        // Información básica
        this.formData.bot_name = document.getElementById('botName')?.value || '';
        this.formData.bot_description = document.getElementById('botDescription')?.value || '';
        
        // Funcionalidades
        this.formData.functionality = Array.from(
            form.querySelectorAll('input[name="functionality"]:checked')
        ).map(el => el.value);
        
        // Fuentes de datos
        this.formData.input_source = Array.from(
            form.querySelectorAll('input[name="input_source"]:checked')
        ).map(el => el.value);
        
        // Acciones
        this.formData.actions = Array.from(
            form.querySelectorAll('input[name="actions"]:checked')
        ).map(el => el.value);
        
        // Nivel de IA
        this.formData.ai_level = document.getElementById('aiLevel')?.value || 'basic';
        
        // Parámetros avanzados
        this.formData.update_frequency = document.getElementById('updateFrequency')?.value || 'realtime';
        this.formData.sensitivity = parseInt(document.getElementById('sensitivity')?.value || '5');
        this.formData.enable_logging = document.getElementById('enableLogging')?.checked || false;
        this.formData.enable_notifications = document.getElementById('enableNotifications')?.checked || false;
    }
    
    async updateAISuggestions() {
        try {
            const response = await fetch('/api/custom-bot/suggestions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.formData)
            });
            
            if (!response.ok) {
                console.error('Error al obtener sugerencias:', response.statusText);
                return;
            }
            
            const data = await response.json();
            if (data.success) {
                this.aiSuggestions = data.suggestions;
                this.displayAISuggestions();
            }
        } catch (error) {
            console.error('Error al actualizar sugerencias de IA:', error);
        }
    }
    
    displayAISuggestions() {
        const suggestionsContainer = document.getElementById('aiSuggestions');
        if (!suggestionsContainer || !this.aiSuggestions) return;
        
        let html = '';
        
        // Sugerencias generales
        if (this.aiSuggestions.general && this.aiSuggestions.general.length > 0) {
            html += '<div class="suggestion-group">';
            html += '<h5><i class="fas fa-info-circle"></i> Información</h5>';
            this.aiSuggestions.general.forEach(suggestion => {
                html += `<p class="suggestion-item">💡 ${suggestion}</p>`;
            });
            html += '</div>';
        }
        
        // Sugerencias de funcionalidad
        if (this.aiSuggestions.functionality && this.aiSuggestions.functionality.length > 0) {
            html += '<div class="suggestion-group">';
            html += '<h5><i class="fas fa-cogs"></i> Funcionalidad</h5>';
            this.aiSuggestions.functionality.forEach(suggestion => {
                html += `<p class="suggestion-item">✨ ${suggestion}</p>`;
            });
            html += '</div>';
        }
        
        // Sugerencias de arquitectura
        if (this.aiSuggestions.architecture && this.aiSuggestions.architecture.length > 0) {
            html += '<div class="suggestion-group">';
            html += '<h5><i class="fas fa-sitemap"></i> Arquitectura</h5>';
            this.aiSuggestions.architecture.forEach(suggestion => {
                html += `<p class="suggestion-item">🏗️ ${suggestion}</p>`;
            });
            html += '</div>';
        }
        
        // Sugerencias de seguridad
        if (this.aiSuggestions.security && this.aiSuggestions.security.length > 0) {
            html += '<div class="suggestion-group">';
            html += '<h5><i class="fas fa-shield-alt"></i> Seguridad</h5>';
            this.aiSuggestions.security.forEach(suggestion => {
                html += `<p class="suggestion-item">🔒 ${suggestion}</p>`;
            });
            html += '</div>';
        }
        
        // Sugerencias de rendimiento
        if (this.aiSuggestions.performance && this.aiSuggestions.performance.length > 0) {
            html += '<div class="suggestion-group">';
            html += '<h5><i class="fas fa-tachometer-alt"></i> Rendimiento</h5>';
            this.aiSuggestions.performance.forEach(suggestion => {
                html += `<p class="suggestion-item">⚡ ${suggestion}</p>`;
            });
            html += '</div>';
        }
        
        if (html === '') {
            html = '<p class="ai-message">Completa el formulario para recibir sugerencias de IA...</p>';
        }
        
        suggestionsContainer.innerHTML = html;
    }
    
    async generateBot() {
        // Validar formulario
        const form = document.getElementById('custom-form');
        if (!form.checkValidity()) {
            alert('Por favor completa todos los campos requeridos');
            return;
        }
        
        // Mostrar loading
        const generateBtn = document.getElementById('generateCustomBotBtn');
        const originalText = generateBtn.innerHTML;
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generando...';
        
        try {
            const response = await fetch('/api/custom-bot/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.formData)
            });
            
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Mostrar resultado
                this.showBotResult(data);
            } else {
                alert(`Error: ${data.errors.join(', ')}`);
            }
        } catch (error) {
            console.error('Error al generar bot:', error);
            alert(`Error al generar bot: ${error.message}`);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = originalText;
        }
    }
    
    showBotResult(data) {
        // Actualizar metadatos
        const metadataGrid = document.getElementById('botMetadata');
        if (metadataGrid) {
            metadataGrid.innerHTML = `
                <div class="metadata-item">
                    <label>Nombre</label>
                    <value>${data.bot_name}</value>
                </div>
                <div class="metadata-item">
                    <label>Tipo</label>
                    <value>Personalizado</value>
                </div>
                <div class="metadata-item">
                    <label>Nivel de IA</label>
                    <value>${this.formData.ai_level}</value>
                </div>
                <div class="metadata-item">
                    <label>Funcionalidades</label>
                    <value>${this.formData.functionality.length}</value>
                </div>
            `;
        }
        
        // Mostrar código generado
        const codeContainer = document.getElementById('generatedBotCode');
        if (codeContainer) {
            codeContainer.innerHTML = `<pre><code>${this.escapeHtml(data.code)}</code></pre>`;
        }
        
        // Mostrar sugerencias
        const validationContainer = document.getElementById('botValidation');
        if (validationContainer && data.warnings && data.warnings.length > 0) {
            let warningsHtml = '<div class="warnings-section"><h4>Advertencias</h4>';
            data.warnings.forEach(warning => {
                warningsHtml += `<p class="warning-item">⚠️ ${warning}</p>`;
            });
            warningsHtml += '</div>';
            validationContainer.innerHTML = warningsHtml;
        }
        
        // Cambiar a pestaña de resultado
        this.showStep('bot-result');
    }
    
    backToTemplate() {
        this.currentTemplate = null;
        this.formData = {};
        this.showStep('template-selection');
    }
    
    showStep(stepId) {
        // Ocultar todos los pasos
        document.querySelectorAll('.bot-step').forEach(step => {
            step.classList.add('hidden');
        });
        
        // Mostrar el paso seleccionado
        const step = document.getElementById(stepId);
        if (step) {
            step.classList.remove('hidden');
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.customBotFormManager = new CustomBotFormManager();
});
