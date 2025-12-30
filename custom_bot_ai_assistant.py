#!/usr/bin/env python3
"""
Asistente de IA para creación de bots personalizados
Proporciona sugerencias inteligentes basadas en la configuración del usuario
"""

import json
from typing import Dict, List, Any

class CustomBotAIAssistant:
    """Asistente de IA para guiar la creación de bots personalizados"""
    
    def __init__(self):
        self.suggestions_database = self._load_suggestions_database()
        self.code_templates = self._load_code_templates()
    
    def _load_suggestions_database(self) -> Dict[str, Any]:
        """Carga la base de datos de sugerencias de IA"""
        return {
            'functionality': {
                'monitoring': {
                    'description': 'Monitoreo en tiempo real',
                    'suggestions': [
                        'Utiliza interfaces de red para capturar tráfico',
                        'Implementa alertas en tiempo real',
                        'Considera usar machine learning para detección de patrones'
                    ],
                    'related_inputs': ['network', 'logs'],
                    'related_actions': ['alert', 'log', 'report']
                },
                'detection': {
                    'description': 'Detección de amenazas',
                    'suggestions': [
                        'Implementa firmas de malware conocidas',
                        'Usa análisis heurístico para amenazas desconocidas',
                        'Integra con bases de datos de amenazas (VirusTotal, etc.)',
                        'Considera usar deep learning para detección avanzada'
                    ],
                    'related_inputs': ['network', 'logs', 'api'],
                    'related_actions': ['alert', 'block', 'notify']
                },
                'response': {
                    'description': 'Respuesta automática',
                    'suggestions': [
                        'Define escalas de respuesta según severidad',
                        'Implementa contención automática de amenazas',
                        'Crea flujos de respuesta personalizados',
                        'Integra con sistemas de remedación'
                    ],
                    'related_inputs': ['network', 'logs', 'system'],
                    'related_actions': ['block', 'remediate', 'notify']
                },
                'analysis': {
                    'description': 'Análisis y reportes',
                    'suggestions': [
                        'Genera reportes automáticos diarios/semanales',
                        'Implementa análisis de tendencias',
                        'Crea dashboards visuales',
                        'Exporta datos en múltiples formatos'
                    ],
                    'related_inputs': ['logs', 'database'],
                    'related_actions': ['report', 'log']
                },
                'prediction': {
                    'description': 'Predicción con IA',
                    'suggestions': [
                        'Usa modelos de machine learning para predicción',
                        'Implementa análisis de patrones históricos',
                        'Crea alertas predictivas',
                        'Integra con sistemas de IA generativa'
                    ],
                    'related_inputs': ['logs', 'database', 'api'],
                    'related_actions': ['alert', 'report', 'notify']
                },
                'automation': {
                    'description': 'Automatización',
                    'suggestions': [
                        'Automatiza tareas repetitivas',
                        'Crea flujos de trabajo sin intervención manual',
                        'Implementa reglas de negocio complejas',
                        'Integra con sistemas externos'
                    ],
                    'related_inputs': ['api', 'database', 'system'],
                    'related_actions': ['block', 'remediate', 'log']
                }
            },
            'input_sources': {
                'network': {
                    'description': 'Tráfico de red',
                    'tools': ['Wireshark', 'tcpdump', 'Zeek', 'Suricata'],
                    'suggestions': [
                        'Usa libpcap para captura de paquetes',
                        'Implementa análisis de flujos de red',
                        'Considera usar PCAP remoto para monitoreo distribuido'
                    ]
                },
                'logs': {
                    'description': 'Archivos de log',
                    'tools': ['ELK Stack', 'Splunk', 'Graylog', 'Loki'],
                    'suggestions': [
                        'Implementa parsers para diferentes formatos de log',
                        'Usa expresiones regulares para extracción de datos',
                        'Considera centralizar logs en un servidor'
                    ]
                },
                'api': {
                    'description': 'APIs externas',
                    'tools': ['requests', 'httpx', 'aiohttp'],
                    'suggestions': [
                        'Implementa reintentos y timeout',
                        'Usa autenticación segura (OAuth, API keys)',
                        'Considera rate limiting y caché'
                    ]
                },
                'database': {
                    'description': 'Base de datos',
                    'tools': ['SQLite', 'PostgreSQL', 'MongoDB', 'InfluxDB'],
                    'suggestions': [
                        'Usa índices para optimizar consultas',
                        'Implementa backups automáticos',
                        'Considera usar time-series DB para métricas'
                    ]
                },
                'system': {
                    'description': 'Eventos del sistema',
                    'tools': ['syslog', 'Windows Event Log', 'auditd'],
                    'suggestions': [
                        'Monitorea eventos de seguridad del SO',
                        'Implementa auditoría de cambios',
                        'Usa webhooks para notificaciones en tiempo real'
                    ]
                }
            },
            'actions': {
                'alert': {
                    'description': 'Enviar alertas',
                    'channels': ['Email', 'SMS', 'Slack', 'Teams', 'Webhook'],
                    'suggestions': [
                        'Personaliza plantillas de alerta',
                        'Implementa escalado de alertas',
                        'Usa correlación para reducir falsos positivos'
                    ]
                },
                'block': {
                    'description': 'Bloquear amenazas',
                    'methods': ['Firewall rules', 'IP blacklist', 'Domain block', 'User disable'],
                    'suggestions': [
                        'Implementa whitelist/blacklist dinámicas',
                        'Usa reglas de firewall granulares',
                        'Considera reversión automática de bloqueos'
                    ]
                },
                'log': {
                    'description': 'Registrar eventos',
                    'formats': ['JSON', 'CSV', 'Syslog', 'CEF'],
                    'suggestions': [
                        'Implementa rotación de logs',
                        'Usa compresión para logs antiguos',
                        'Centraliza logs para análisis'
                    ]
                },
                'report': {
                    'description': 'Generar reportes',
                    'formats': ['PDF', 'HTML', 'Excel', 'JSON'],
                    'suggestions': [
                        'Crea reportes ejecutivos y técnicos',
                        'Implementa programación de reportes',
                        'Usa visualizaciones claras'
                    ]
                },
                'notify': {
                    'description': 'Notificar a usuarios',
                    'methods': ['Email', 'SMS', 'Push', 'Dashboard'],
                    'suggestions': [
                        'Personaliza notificaciones por rol',
                        'Implementa confirmación de lectura',
                        'Usa prioridades para escalado'
                    ]
                },
                'remediate': {
                    'description': 'Remediar automáticamente',
                    'actions': ['Kill process', 'Delete file', 'Restore backup', 'Isolate system'],
                    'suggestions': [
                        'Implementa confirmación antes de remediar',
                        'Mantén registro de remediaciones',
                        'Crea rollback automático si es necesario'
                    ]
                }
            },
            'ai_levels': {
                'basic': {
                    'description': 'Reglas simples',
                    'complexity': 'Baja',
                    'suggestions': [
                        'Usa reglas if/then simples',
                        'Implementa lógica booleana básica',
                        'Ideal para principiantes'
                    ]
                },
                'intermediate': {
                    'description': 'Machine Learning',
                    'complexity': 'Media',
                    'suggestions': [
                        'Usa sklearn para clasificación',
                        'Implementa detección de anomalías',
                        'Requiere datos de entrenamiento'
                    ]
                },
                'advanced': {
                    'description': 'Deep Learning',
                    'complexity': 'Alta',
                    'suggestions': [
                        'Usa TensorFlow o PyTorch',
                        'Implementa redes neuronales',
                        'Requiere GPU para mejor rendimiento'
                    ]
                },
                'expert': {
                    'description': 'IA Generativa',
                    'complexity': 'Muy Alta',
                    'suggestions': [
                        'Integra con GPT-4 o Claude',
                        'Implementa prompt engineering',
                        'Usa fine-tuning para casos específicos'
                    ]
                }
            }
        }
    
    def _load_code_templates(self) -> Dict[str, str]:
        """Carga plantillas de código para diferentes tipos de bots"""
        return {
            'monitoring_basic': '''
# Bot de Monitoreo Básico
import time
from datetime import datetime

class MonitoringBot:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.running = False
    
    def start(self):
        self.running = True
        while self.running:
            self.check_traffic()
            time.sleep(5)
    
    def check_traffic(self):
        # Implementar lógica de monitoreo
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] Monitoreando {self.interface}")
    
    def stop(self):
        self.running = False

# Uso
bot = MonitoringBot()
bot.start()
            ''',
            'detection_basic': '''
# Bot de Detección Básico
import re
from datetime import datetime

class DetectionBot:
    def __init__(self):
        self.threats = []
        self.signatures = self._load_signatures()
    
    def _load_signatures(self):
        return {
            'sql_injection': r"(union|select|insert|delete|drop).*from",
            'xss': r"<script|javascript:|onerror=",
            'command_injection': r"(;|\\|&|\\||>|<|\\$\\(|`)"
        }
    
    def analyze(self, data):
        for threat_type, pattern in self.signatures.items():
            if re.search(pattern, data, re.IGNORECASE):
                self.threats.append({
                    'type': threat_type,
                    'timestamp': datetime.now().isoformat(),
                    'data': data[:100]
                })
                return True
        return False
    
    def get_threats(self):
        return self.threats

# Uso
bot = DetectionBot()
if bot.analyze("SELECT * FROM users"):
    print("¡Amenaza detectada!")
            ''',
            'response_basic': '''
# Bot de Respuesta Básico
from datetime import datetime

class ResponseBot:
    def __init__(self):
        self.blocked_ips = set()
        self.alerts = []
    
    def respond_to_threat(self, threat_data):
        severity = self._calculate_severity(threat_data)
        
        if severity == 'critical':
            self._block_source(threat_data['source_ip'])
            self._send_alert(threat_data, 'CRÍTICO')
        elif severity == 'high':
            self._send_alert(threat_data, 'ALTO')
        else:
            self._log_threat(threat_data)
    
    def _calculate_severity(self, threat_data):
        # Implementar lógica de cálculo de severidad
        return 'medium'
    
    def _block_source(self, ip):
        self.blocked_ips.add(ip)
        print(f"IP bloqueada: {ip}")
    
    def _send_alert(self, threat_data, level):
        alert = {
            'level': level,
            'timestamp': datetime.now().isoformat(),
            'threat': threat_data
        }
        self.alerts.append(alert)
        print(f"[{level}] Alerta enviada")
    
    def _log_threat(self, threat_data):
        print(f"Amenaza registrada: {threat_data}")

# Uso
bot = ResponseBot()
bot.respond_to_threat({'source_ip': '192.168.1.100', 'type': 'scan'})
            '''
        }
    
    def get_suggestions(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera sugerencias de IA basadas en la configuración del formulario
        
        Args:
            form_data: Datos del formulario del usuario
        
        Returns:
            Diccionario con sugerencias de IA
        """
        suggestions = {
            'general': [],
            'functionality': [],
            'architecture': [],
            'security': [],
            'performance': [],
            'code_template': None
        }
        
        # Análisis de funcionalidades seleccionadas
        functionalities = form_data.get('functionality', [])
        input_sources = form_data.get('input_source', [])
        actions = form_data.get('actions', [])
        ai_level = form_data.get('ai_level', 'basic')
        
        # Sugerencias generales
        if not functionalities:
            suggestions['general'].append('Selecciona al menos una funcionalidad para tu bot')
        
        if not input_sources:
            suggestions['general'].append('Especifica de dónde obtendrá datos tu bot')
        
        if not actions:
            suggestions['general'].append('Define qué acciones realizará tu bot')
        
        # Sugerencias por funcionalidad
        for func in functionalities:
            if func in self.suggestions_database['functionality']:
                func_data = self.suggestions_database['functionality'][func]
                suggestions['functionality'].extend(func_data['suggestions'][:2])
        
        # Sugerencias de arquitectura
        if len(input_sources) > 1:
            suggestions['architecture'].append('Considera usar un patrón de productor-consumidor para múltiples fuentes')
        
        if 'prediction' in functionalities:
            suggestions['architecture'].append('Implementa un pipeline de ML con entrenamiento y predicción separados')
        
        if 'automation' in functionalities:
            suggestions['architecture'].append('Usa un sistema de colas (Redis, RabbitMQ) para tareas asincrónicas')
        
        # Sugerencias de seguridad
        if 'block' in actions or 'remediate' in actions:
            suggestions['security'].append('Implementa confirmación de dos factores para acciones destructivas')
            suggestions['security'].append('Mantén un registro de auditoría detallado de todas las acciones')
        
        if 'api' in input_sources:
            suggestions['security'].append('Usa HTTPS y valida certificados SSL/TLS')
            suggestions['security'].append('Implementa rate limiting y autenticación robusta')
        
        # Sugerencias de rendimiento
        if 'monitoring' in functionalities:
            suggestions['performance'].append('Usa caché para datos frecuentemente accedidos')
            suggestions['performance'].append('Implementa procesamiento asincrónico para no bloquear')
        
        if ai_level in ['advanced', 'expert']:
            suggestions['performance'].append('Considera usar GPU para aceleración de cálculos')
        
        # Seleccionar plantilla de código
        if 'monitoring' in functionalities:
            suggestions['code_template'] = self.code_templates['monitoring_basic']
        elif 'detection' in functionalities:
            suggestions['code_template'] = self.code_templates['detection_basic']
        elif 'response' in functionalities:
            suggestions['code_template'] = self.code_templates['response_basic']
        
        return suggestions
    
    def generate_bot_code(self, form_data: Dict[str, Any]) -> str:
        """
        Genera código del bot basado en la configuración
        
        Args:
            form_data: Datos del formulario del usuario
        
        Returns:
            Código generado del bot
        """
        bot_name = form_data.get('bot_name', 'CustomBot')
        description = form_data.get('bot_description', 'Bot personalizado')
        functionalities = form_data.get('functionality', [])
        ai_level = form_data.get('ai_level', 'basic')
        
        code = f'''#!/usr/bin/env python3
"""
{bot_name}
{description}

Generado automáticamente por Guardián IDE
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class {bot_name}:
    """Bot de seguridad personalizado"""
    
    def __init__(self):
        self.name = "{bot_name}"
        self.description = "{description}"
        self.running = False
        self.events = []
        self.alerts = []
        self.ai_level = "{ai_level}"
        logger.info(f"Inicializando {{self.name}}")
    
    def start(self):
        """Inicia el bot"""
        self.running = True
        logger.info(f"{{self.name}} iniciado")
    
    def stop(self):
        """Detiene el bot"""
        self.running = False
        logger.info(f"{{self.name}} detenido")
    
    def process_event(self, event: Dict[str, Any]):
        """Procesa un evento"""
        self.events.append(event)
        logger.info(f"Evento procesado: {{event}}")
    
    def send_alert(self, alert_data: Dict[str, Any]):
        """Envía una alerta"""
        alert = {{
            'timestamp': datetime.now().isoformat(),
            'bot': self.name,
            'data': alert_data
        }}
        self.alerts.append(alert)
        logger.warning(f"Alerta enviada: {{alert}}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna el estado del bot"""
        return {{
            'name': self.name,
            'running': self.running,
            'events_processed': len(self.events),
            'alerts_sent': len(self.alerts),
            'ai_level': self.ai_level
        }}

# Punto de entrada
if __name__ == "__main__":
    bot = {bot_name}()
    bot.start()
    
    # Ejemplo de uso
    bot.process_event({{'type': 'test', 'data': 'evento de prueba'}})
    print(json.dumps(bot.get_status(), indent=2))
    
    bot.stop()
'''
        
        return code
    
    def validate_configuration(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida la configuración del formulario
        
        Args:
            form_data: Datos del formulario
        
        Returns:
            Diccionario con resultados de validación
        """
        errors = []
        warnings = []
        
        # Validaciones requeridas
        if not form_data.get('bot_name'):
            errors.append('El nombre del bot es requerido')
        
        if not form_data.get('bot_description'):
            errors.append('La descripción del bot es requerida')
        
        if not form_data.get('functionality'):
            errors.append('Selecciona al menos una funcionalidad')
        
        if not form_data.get('input_source'):
            errors.append('Especifica al menos una fuente de datos')
        
        if not form_data.get('actions'):
            errors.append('Define al menos una acción')
        
        # Advertencias
        if len(form_data.get('functionality', [])) > 5:
            warnings.append('Demasiadas funcionalidades seleccionadas. Considera simplificar.')
        
        if form_data.get('ai_level') == 'expert' and not form_data.get('bot_description'):
            warnings.append('Para IA Experta, proporciona una descripción detallada')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


# Función auxiliar para uso en API
def get_ai_suggestions(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Obtiene sugerencias de IA para un formulario"""
    assistant = CustomBotAIAssistant()
    return assistant.get_suggestions(form_data)


def generate_custom_bot(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Genera un bot personalizado"""
    assistant = CustomBotAIAssistant()
    
    # Validar configuración
    validation = assistant.validate_configuration(form_data)
    if not validation['valid']:
        return {
            'success': False,
            'errors': validation['errors'],
            'warnings': validation['warnings']
        }
    
    # Generar código
    code = assistant.generate_bot_code(form_data)
    
    # Obtener sugerencias
    suggestions = assistant.get_suggestions(form_data)
    
    return {
        'success': True,
        'bot_name': form_data.get('bot_name'),
        'code': code,
        'suggestions': suggestions,
        'warnings': validation['warnings']
    }
