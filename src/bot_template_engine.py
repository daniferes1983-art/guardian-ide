"""
Motor de Plantillas para Bots de Guardián
Genera código de bots personalizados basándose en plantillas JSON y parámetros del usuario.
"""

import json
import os
import re
from typing import Dict, List, Any, Optional
from jinja2 import Template, Environment, BaseLoader
import jsonschema


class GuardianBotTemplateEngine:
    """Motor de plantillas para generar bots de ciberseguridad en Guardián"""
    
    def __init__(self, templates_dir: str = "bot_templates", schema_file: str = "bot_templates_schema.json"):
        """
        Inicializa el motor de plantillas
        
        Args:
            templates_dir: Directorio donde se encuentran las plantillas JSON
            schema_file: Archivo de esquema JSON para validación
        """
        self.templates_dir = templates_dir
        self.schema_file = schema_file
        self.templates = {}
        self.schema = None
        self.jinja_env = Environment(loader=BaseLoader())
        
        # Cargar esquema de validación
        self._load_schema()
        
        # Cargar todas las plantillas disponibles
        self._load_templates()
    
    def _load_schema(self):
        """Carga el esquema JSON para validación de plantillas"""
        try:
            with open(self.schema_file, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Archivo de esquema {self.schema_file} no encontrado")
            self.schema = None
        except json.JSONDecodeError as e:
            print(f"❌ Error al cargar esquema JSON: {e}")
            self.schema = None
    
    def _load_templates(self):
        """Carga todas las plantillas JSON del directorio especificado"""
        if not os.path.exists(self.templates_dir):
            print(f"⚠️  Directorio de plantillas {self.templates_dir} no encontrado")
            return
        
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                template_path = os.path.join(self.templates_dir, filename)
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    
                    # Validar plantilla contra esquema
                    if self.schema:
                        try:
                            jsonschema.validate(template_data, self.schema)
                        except jsonschema.ValidationError as e:
                            print(f"❌ Plantilla {filename} no válida: {e.message}")
                            continue
                    
                    template_id = template_data['template_info']['id']
                    self.templates[template_id] = template_data
                    print(f"✅ Plantilla cargada: {template_id}")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Error al cargar plantilla {filename}: {e}")
                except KeyError as e:
                    print(f"❌ Plantilla {filename} mal formada: falta {e}")
    
    def get_available_templates(self) -> Dict[str, Dict]:
        """
        Retorna información básica de todas las plantillas disponibles
        
        Returns:
            Diccionario con información de plantillas {template_id: template_info}
        """
        return {
            template_id: template_data['template_info'] 
            for template_id, template_data in self.templates.items()
        }
    
    def get_template_details(self, template_id: str) -> Optional[Dict]:
        """
        Obtiene los detalles completos de una plantilla específica
        
        Args:
            template_id: ID de la plantilla
            
        Returns:
            Diccionario con todos los detalles de la plantilla o None si no existe
        """
        return self.templates.get(template_id)
    
    def get_template_parameters(self, template_id: str) -> Optional[Dict]:
        """
        Obtiene los parámetros configurables de una plantilla
        
        Args:
            template_id: ID de la plantilla
            
        Returns:
            Diccionario con los parámetros de la plantilla o None si no existe
        """
        template = self.templates.get(template_id)
        if template:
            return template.get('parameters', {})
        return None
    
    def validate_parameters(self, template_id: str, user_parameters: Dict) -> Dict[str, List[str]]:
        """
        Valida los parámetros proporcionados por el usuario
        
        Args:
            template_id: ID de la plantilla
            user_parameters: Parámetros proporcionados por el usuario
            
        Returns:
            Diccionario con errores de validación {'errors': [...], 'warnings': [...]}
        """
        template = self.templates.get(template_id)
        if not template:
            return {'errors': [f'Plantilla {template_id} no encontrada'], 'warnings': []}
        
        template_params = template.get('parameters', {})
        errors = []
        warnings = []
        
        # Verificar parámetros requeridos
        for param_name, param_config in template_params.items():
            if param_config.get('required', False) and param_name not in user_parameters:
                errors.append(f'Parámetro requerido faltante: {param_name}')
        
        # Validar tipos y restricciones
        for param_name, param_value in user_parameters.items():
            if param_name in template_params:
                param_config = template_params[param_name]
                
                # Validar tipo
                expected_type = param_config['type']
                if not self._validate_parameter_type(param_value, expected_type):
                    errors.append(f'Tipo incorrecto para {param_name}: esperado {expected_type}')
                
                # Validar restricciones
                validation = param_config.get('validation', {})
                validation_errors = self._validate_parameter_constraints(param_name, param_value, validation)
                errors.extend(validation_errors)
            else:
                warnings.append(f'Parámetro desconocido: {param_name}')
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_parameter_type(self, value: Any, expected_type: str) -> bool:
        """Valida el tipo de un parámetro"""
        type_validators = {
            'string': lambda v: isinstance(v, str),
            'integer': lambda v: isinstance(v, int),
            'float': lambda v: isinstance(v, (int, float)),
            'boolean': lambda v: isinstance(v, bool),
            'array': lambda v: isinstance(v, list),
            'ip_address': lambda v: self._is_valid_ip(v),
            'port': lambda v: isinstance(v, int) and 1 <= v <= 65535,
            'interface': lambda v: isinstance(v, str) and re.match(r'^[a-zA-Z0-9]+$', v),
            'file_path': lambda v: isinstance(v, str) and os.path.isabs(v)
        }
        
        validator = type_validators.get(expected_type, lambda v: True)
        return validator(value)
    
    def _validate_parameter_constraints(self, param_name: str, value: Any, validation: Dict) -> List[str]:
        """Valida las restricciones de un parámetro"""
        errors = []
        
        if 'min' in validation and isinstance(value, (int, float)) and value < validation['min']:
            errors.append(f'{param_name} debe ser mayor o igual a {validation["min"]}')
        
        if 'max' in validation and isinstance(value, (int, float)) and value > validation['max']:
            errors.append(f'{param_name} debe ser menor o igual a {validation["max"]}')
        
        if 'pattern' in validation and isinstance(value, str):
            if not re.match(validation['pattern'], value):
                errors.append(f'{param_name} no cumple con el patrón requerido')
        
        if 'enum' in validation and value not in validation['enum']:
            errors.append(f'{param_name} debe ser uno de: {", ".join(validation["enum"])}')
        
        return errors
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Valida si una cadena es una dirección IP válida"""
        import ipaddress
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def generate_bot_code(self, template_id: str, user_parameters: Dict) -> Dict[str, Any]:
        """
        Genera el código del bot basándose en la plantilla y parámetros del usuario
        
        Args:
            template_id: ID de la plantilla a usar
            user_parameters: Parámetros proporcionados por el usuario
            
        Returns:
            Diccionario con el resultado de la generación:
            {
                'success': bool,
                'code': str,
                'errors': List[str],
                'warnings': List[str],
                'metadata': Dict
            }
        """
        # Validar que la plantilla existe
        template = self.templates.get(template_id)
        if not template:
            return {
                'success': False,
                'code': '',
                'errors': [f'Plantilla {template_id} no encontrada'],
                'warnings': [],
                'metadata': {}
            }
        
        # Validar parámetros
        validation_result = self.validate_parameters(template_id, user_parameters)
        if validation_result['errors']:
            return {
                'success': False,
                'code': '',
                'errors': validation_result['errors'],
                'warnings': validation_result['warnings'],
                'metadata': {}
            }
        
        # Combinar parámetros del usuario con valores por defecto
        final_parameters = self._merge_with_defaults(template, user_parameters)
        
        # Generar código usando reemplazo simple (más confiable que Jinja2 para este caso)
        try:
            code_template = template['code_template']
            generated_code = code_template
            
            # Reemplazar cada parámetro en el código
            for param_name, param_value in final_parameters.items():
                placeholder = f"{{{param_name}}}"
                
                # Convertir valor a string apropiado
                if isinstance(param_value, list):
                    # Para arrays, convertir a formato de lista de Guardián
                    value_str = str(param_value)
                elif isinstance(param_value, bool):
                    # Para booleanos, convertir a string
                    value_str = str(param_value).lower()
                else:
                    value_str = str(param_value)
                
                generated_code = generated_code.replace(placeholder, value_str)
            
            # Generar metadata del bot
            metadata = self._generate_bot_metadata(template, final_parameters)
            
            return {
                'success': True,
                'code': generated_code,
                'errors': [],
                'warnings': validation_result['warnings'],
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'success': False,
                'code': '',
                'errors': [f'Error al generar código: {str(e)}'],
                'warnings': validation_result['warnings'],
                'metadata': {}
            }
    
    def _merge_with_defaults(self, template: Dict, user_parameters: Dict) -> Dict:
        """Combina parámetros del usuario con valores por defecto de la plantilla"""
        template_params = template.get('parameters', {})
        final_params = {}
        
        for param_name, param_config in template_params.items():
            if param_name in user_parameters:
                final_params[param_name] = user_parameters[param_name]
            elif 'default' in param_config:
                final_params[param_name] = param_config['default']
        
        return final_params
    
    def _generate_bot_metadata(self, template: Dict, parameters: Dict) -> Dict:
        """Genera metadata del bot generado"""
        return {
            'template_id': template['template_info']['id'],
            'template_name': template['template_info']['name'],
            'template_version': template['template_info'].get('version', '1.0.0'),
            'generated_at': self._get_current_timestamp(),
            'parameters_used': parameters,
            'components': [comp['name'] for comp in template.get('components', [])],
            'triggers': [trigger['type'] for trigger in template.get('triggers', [])],
            'dependencies': self._extract_dependencies(template),
            'security_guidelines': template.get('security_guidelines', [])
        }
    
    def _extract_dependencies(self, template: Dict) -> List[str]:
        """Extrae todas las dependencias de Python de los componentes"""
        dependencies = set()
        for component in template.get('components', []):
            comp_deps = component.get('dependencies', [])
            dependencies.update(comp_deps)
        return list(dependencies)
    
    def _get_current_timestamp(self) -> str:
        """Obtiene timestamp actual en formato ISO"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_ai_questions_for_template(self, template_id: str) -> List[Dict]:
        """
        Obtiene las preguntas que la IA debe hacer para una plantilla específica
        
        Args:
            template_id: ID de la plantilla
            
        Returns:
            Lista de preguntas con metadata para la IA
        """
        template = self.templates.get(template_id)
        if not template:
            return []
        
        questions = []
        parameters = template.get('parameters', {})
        
        # Pregunta inicial
        ai_prompts = template.get('ai_prompts', {})
        if 'initial_question' in ai_prompts:
            questions.append({
                'type': 'initial',
                'question': ai_prompts['initial_question'],
                'parameter': None
            })
        
        # Preguntas por parámetro
        for param_name, param_config in parameters.items():
            if 'ai_question' in param_config:
                questions.append({
                    'type': 'parameter',
                    'question': param_config['ai_question'],
                    'parameter': param_name,
                    'param_type': param_config['type'],
                    'required': param_config.get('required', False),
                    'suggestions': param_config.get('ai_suggestions', []),
                    'validation': param_config.get('validation', {})
                })
        
        # Preguntas de seguimiento
        follow_ups = ai_prompts.get('follow_up_questions', [])
        for follow_up in follow_ups:
            questions.append({
                'type': 'follow_up',
                'question': follow_up,
                'parameter': None
            })
        
        return questions
    
    def get_ai_recommendations_for_template(self, template_id: str) -> List[str]:
        """Obtiene las recomendaciones de IA para una plantilla"""
        template = self.templates.get(template_id)
        if not template:
            return []
        
        ai_prompts = template.get('ai_prompts', {})
        return ai_prompts.get('recommendations', [])
    
    def validate_generated_bot(self, template_id: str, generated_code: str, parameters: Dict) -> Dict[str, List[str]]:
        """
        Valida el bot generado contra las directrices de seguridad
        
        Args:
            template_id: ID de la plantilla usada
            generated_code: Código generado del bot
            parameters: Parámetros usados en la generación
            
        Returns:
            Diccionario con errores y advertencias de seguridad
        """
        template = self.templates.get(template_id)
        if not template:
            return {'errors': ['Plantilla no encontrada'], 'warnings': []}
        
        errors = []
        warnings = []
        
        # Validaciones de seguridad básicas
        security_checks = [
            self._check_no_dangerous_commands,
            self._check_firewall_rules_safety,
            self._check_resource_limits,
            self._check_infinite_loops
        ]
        
        for check in security_checks:
            check_result = check(generated_code, parameters)
            errors.extend(check_result.get('errors', []))
            warnings.extend(check_result.get('warnings', []))
        
        # Validaciones específicas de la plantilla
        security_guidelines = template.get('security_guidelines', [])
        for guideline in security_guidelines:
            if not self._check_security_guideline(generated_code, guideline):
                warnings.append(f'Posible violación de directriz de seguridad: {guideline}')
        
        return {'errors': errors, 'warnings': warnings}
    
    def _check_no_dangerous_commands(self, code: str, parameters: Dict) -> Dict[str, List[str]]:
        """Verifica que no haya comandos peligrosos en el código"""
        dangerous_patterns = [
            r'rm\s+-rf\s+/',
            r'format\s+c:',
            r'del\s+/\*',
            r'shutdown\s+now',
            r'reboot\s+--force'
        ]
        
        errors = []
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                errors.append(f'Comando peligroso detectado: {pattern}')
        
        return {'errors': errors, 'warnings': []}
    
    def _check_firewall_rules_safety(self, code: str, parameters: Dict) -> Dict[str, List[str]]:
        """Verifica que las reglas de firewall no bloqueen el acceso del administrador"""
        warnings = []
        
        # Buscar reglas de bloqueo total
        if re.search(r'bloquear.*\*.*\*', code):
            warnings.append('Regla de firewall muy amplia detectada - podría bloquear acceso legítimo')
        
        # Verificar que no se bloquee SSH por defecto
        if re.search(r'bloquear.*puerto:\s*22', code):
            warnings.append('Regla que bloquea puerto SSH (22) - asegúrate de tener acceso alternativo')
        
        return {'errors': [], 'warnings': warnings}
    
    def _check_resource_limits(self, code: str, parameters: Dict) -> Dict[str, List[str]]:
        """Verifica que el bot tenga límites de recursos apropiados"""
        warnings = []
        
        # Verificar bucles sin límites de tiempo
        if 'repetir mientras activo' in code and 'esperar' not in code:
            warnings.append('Bucle sin pausa detectado - podría consumir excesivos recursos de CPU')
        
        # Verificar umbrales muy bajos
        if 'attack_threshold' in parameters and parameters['attack_threshold'] < 100:
            warnings.append('Umbral de ataque muy bajo - podría generar muchas falsas alarmas')
        
        return {'errors': [], 'warnings': warnings}
    
    def _check_infinite_loops(self, code: str, parameters: Dict) -> Dict[str, List[str]]:
        """Verifica que no haya bucles infinitos sin condiciones de salida"""
        errors = []
        
        # Buscar bucles sin condiciones de salida claras
        loop_patterns = [
            r'repetir\s+mientras\s+true',
            r'while\s+True',
            r'for\s+.*\s+in\s+.*:\s*$'
        ]
        
        for pattern in loop_patterns:
            if re.search(pattern, code, re.MULTILINE):
                if 'break' not in code and 'return' not in code and 'exit' not in code:
                    errors.append('Posible bucle infinito sin condición de salida detectado')
        
        return {'errors': errors, 'warnings': []}
    
    def _check_security_guideline(self, code: str, guideline: str) -> bool:
        """Verifica si el código cumple con una directriz de seguridad específica"""
        # Implementación básica - se puede expandir según las directrices
        guideline_lower = guideline.lower()
        
        if 'nunca bloquear' in guideline_lower and 'administrador' in guideline_lower:
            # Verificar que no se bloquee al admin
            return 'admin' not in code or 'bloquear' not in code
        
        if 'validar que la interfaz' in guideline_lower:
            # Verificar que se valide la interfaz
            return 'interfaz' in code
        
        # Por defecto, asumir que se cumple
        return True
    
    def get_testing_scenarios(self, template_id: str) -> List[Dict]:
        """Obtiene los escenarios de prueba para una plantilla"""
        template = self.templates.get(template_id)
        if not template:
            return []
        
        return template.get('testing_scenarios', [])
    
    def export_bot_configuration(self, template_id: str, parameters: Dict, generated_code: str) -> Dict:
        """
        Exporta la configuración completa del bot para guardado/carga posterior
        
        Args:
            template_id: ID de la plantilla usada
            parameters: Parámetros del bot
            generated_code: Código generado
            
        Returns:
            Diccionario con la configuración completa del bot
        """
        return {
            'bot_config': {
                'template_id': template_id,
                'parameters': parameters,
                'generated_code': generated_code,
                'created_at': self._get_current_timestamp(),
                'version': '1.0.0'
            }
        }


# Funciones de utilidad para el motor de plantillas
def create_template_engine() -> GuardianBotTemplateEngine:
    """Crea una instancia del motor de plantillas"""
    return GuardianBotTemplateEngine()


def list_available_templates() -> Dict[str, str]:
    """Lista todas las plantillas disponibles con sus descripciones"""
    engine = create_template_engine()
    templates = engine.get_available_templates()
    return {tid: info['description'] for tid, info in templates.items()}


if __name__ == "__main__":
    # Prueba básica del motor de plantillas
    print("🔧 Probando Motor de Plantillas de Guardián...")
    
    engine = create_template_engine()
    
    # Listar plantillas disponibles
    print("\n📋 Plantillas disponibles:")
    templates = engine.get_available_templates()
    for template_id, info in templates.items():
        print(f"  • {template_id}: {info['name']} ({info['category']})")
    
    # Probar generación de bot de monitoreo de red
    if 'network_monitoring_bot' in templates:
        print("\n🧪 Probando generación de bot de monitoreo de red...")
        
        test_parameters = {
            'bot_name': 'Monitor de Prueba',
            'interface': 'eth0',
            'attack_threshold': 1500,
            'allowed_ips': ['192.168.1.1', '192.168.1.10'],
            'monitoring_duration': 'continuo',
            'alert_level': 'alto'
        }
        
        result = engine.generate_bot_code('network_monitoring_bot', test_parameters)
        
        if result['success']:
            print("✅ Bot generado exitosamente!")
            print(f"📝 Código generado ({len(result['code'])} caracteres)")
            print(f"⚠️  Advertencias: {len(result['warnings'])}")
            if result['warnings']:
                for warning in result['warnings']:
                    print(f"    • {warning}")
        else:
            print("❌ Error al generar bot:")
            for error in result['errors']:
                print(f"    • {error}")

