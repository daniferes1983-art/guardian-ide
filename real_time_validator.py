"""
Validador en Tiempo Real para el Lenguaje Guardián
Proporciona validación de sintaxis mientras el usuario escribe
"""

import re
from typing import List, Dict, Tuple

class RealTimeValidator:
    """Validador que proporciona feedback en tiempo real"""
    
    def __init__(self):
        # Palabras clave del lenguaje Guardián
        self.keywords = {
            'analizar', 'crear', 'listar', 'mostrar', 'responder', 'cancelar',
            'leer', 'monitorear', 'alertar', 'ver', 'detectar', 'evaluar',
            'predecir', 'generar', 'optimizar', 'recomendar'
        }
        
        # Subcomandos
        self.subcommands = {
            'analizar': ['puertos', 'amenazas', 'trafico'],
            'crear': ['regla', 'firewall', 'bot', 'alerta'],
            'generar': ['reglas', 'informe', 'recomendaciones'],
            'monitorear': ['trafico', 'con'],
            'detectar': ['anomalias'],
            'evaluar': ['vulnerabilidades'],
            'predecir': ['ataques'],
            'optimizar': ['politicas'],
            'recomendar': ['acciones'],
            'leer': ['logs'],
            'ver': ['procesos'],
            'alertar': ['con']
        }
        
        # Parámetros válidos
        self.parameters = {
            'de', 'en', 'puerto', 'protocolo', 'accion', 'nivel',
            'basado', 'en', 'patrones', 'historicos', 'para',
            'inteligentes', 'con', 'ia', 'tiempo', 'real'
        }
        
        # Valores válidos para parámetros
        self.valid_values = {
            'protocolo': ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS'],
            'accion': ['bloquear', 'permitir', 'registrar'],
            'nivel': ['bajo', 'medio', 'alto', 'critico'],
            'estado': ['activo', 'inactivo', 'pausado']
        }
        
        # Patrones de error comunes
        self.error_patterns = {
            'missing_parameter': r'(\w+)\s+(?!de|en|puerto|protocolo|accion|nivel)',
            'invalid_ip': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
            'invalid_port': r'puerto:\s*(\d+)',
            'missing_value': r'(\w+):\s*(?!\w)'
        }
    
    def validate(self, text: str) -> Dict:
        """
        Valida el texto en tiempo real
        
        Returns:
            Dict con:
            - valid: bool - Si el código es válido
            - errors: List[Dict] - Lista de errores encontrados
            - warnings: List[Dict] - Lista de advertencias
            - suggestions: List[str] - Sugerencias de corrección
            - syntax_info: Dict - Información de sintaxis
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': [],
            'syntax_info': {},
            'tokens': []
        }
        
        if not text.strip():
            return result
        
        # Tokenizar
        tokens = self._tokenize(text)
        result['tokens'] = tokens
        
        # Validar estructura
        errors = self._validate_structure(text, tokens)
        result['errors'].extend(errors)
        
        # Validar sintaxis
        syntax_errors = self._validate_syntax(text, tokens)
        result['errors'].extend(syntax_errors)
        
        # Validar parámetros
        param_errors = self._validate_parameters(text, tokens)
        result['errors'].extend(param_errors)
        
        # Detectar advertencias
        warnings = self._detect_warnings(text, tokens)
        result['warnings'].extend(warnings)
        
        # Generar sugerencias
        if result['errors']:
            suggestions = self._generate_suggestions(text, result['errors'])
            result['suggestions'].extend(suggestions)
        
        # Actualizar estado de validez
        result['valid'] = len(result['errors']) == 0
        
        return result
    
    def _tokenize(self, text: str) -> List[Dict]:
        """Tokeniza el texto en palabras y símbolos"""
        tokens = []
        pattern = r'\b\w+\b|[:\.,]|"[^"]*"'
        
        for match in re.finditer(pattern, text):
            token = match.group()
            pos = match.start()
            line = text[:pos].count('\n') + 1
            col = pos - text.rfind('\n', 0, pos)
            
            tokens.append({
                'value': token,
                'type': self._get_token_type(token),
                'position': pos,
                'line': line,
                'column': col
            })
        
        return tokens
    
    def _get_token_type(self, token: str) -> str:
        """Determina el tipo de token"""
        if token in self.keywords:
            return 'KEYWORD'
        elif token in self.parameters:
            return 'PARAMETER'
        elif token.startswith('"') and token.endswith('"'):
            return 'STRING'
        elif token.isdigit():
            return 'NUMBER'
        elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', token):
            return 'IP'
        elif token in ':.,:':
            return 'SYMBOL'
        else:
            return 'IDENTIFIER'
    
    def _validate_structure(self, text: str, tokens: List[Dict]) -> List[Dict]:
        """Valida la estructura general del comando"""
        errors = []
        
        if not tokens:
            return errors
        
        first_token = tokens[0]['value']
        
        # Validar que comience con palabra clave
        if first_token not in self.keywords:
            errors.append({
                'type': 'INVALID_COMMAND',
                'message': f'El comando debe comenzar con una palabra clave válida. "{first_token}" no es reconocido.',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_syntax(self, text: str, tokens: List[Dict]) -> List[Dict]:
        """Valida la sintaxis del comando"""
        errors = []
        
        if not tokens:
            return errors
        
        command = tokens[0]['value']
        
        # Validar según el comando
        if command == 'analizar':
            errors.extend(self._validate_analizar(tokens))
        elif command == 'crear':
            errors.extend(self._validate_crear(tokens))
        elif command == 'monitorear':
            errors.extend(self._validate_monitorear(tokens))
        elif command == 'detectar':
            errors.extend(self._validate_detectar(tokens))
        elif command == 'evaluar':
            errors.extend(self._validate_evaluar(tokens))
        elif command == 'predecir':
            errors.extend(self._validate_predecir(tokens))
        elif command == 'generar':
            errors.extend(self._validate_generar(tokens))
        
        return errors
    
    def _validate_analizar(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'analizar'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "analizar" requiere un subcomando (puertos, amenazas, etc.)',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
            return errors
        
        subcommand = tokens[1]['value']
        if subcommand not in ['puertos', 'amenazas', 'trafico']:
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Subcomando inválido: "{subcommand}". Use: puertos, amenazas, trafico',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        # Validar que tenga parámetro "de"
        if len(tokens) < 3 or tokens[2]['value'] != 'de':
            errors.append({
                'type': 'MISSING_PARAMETER',
                'message': 'Se requiere parámetro "de" después del subcomando',
                'line': tokens[1]['line'] if len(tokens) > 1 else 1,
                'column': tokens[1]['column'] if len(tokens) > 1 else 0,
                'severity': 'error'
            })
        
        return errors
    
    def _validate_crear(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'crear'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "crear" requiere un subcomando (regla, firewall, bot)',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
            return errors
        
        subcommand = tokens[1]['value']
        if subcommand not in ['regla', 'firewall', 'bot']:
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Subcomando inválido: "{subcommand}". Use: regla, firewall, bot',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_monitorear(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'monitorear'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "monitorear" requiere un parámetro (trafico, con)',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_detectar(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'detectar'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "detectar" requiere "anomalias"',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        elif tokens[1]['value'] != 'anomalias':
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Se esperaba "anomalias", se encontró "{tokens[1]["value"]}"',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_evaluar(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'evaluar'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "evaluar" requiere "vulnerabilidades"',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        elif tokens[1]['value'] != 'vulnerabilidades':
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Se esperaba "vulnerabilidades", se encontró "{tokens[1]["value"]}"',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_predecir(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'predecir'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "predecir" requiere "ataques"',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        elif tokens[1]['value'] != 'ataques':
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Se esperaba "ataques", se encontró "{tokens[1]["value"]}"',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_generar(self, tokens: List[Dict]) -> List[Dict]:
        """Valida comando 'generar'"""
        errors = []
        
        if len(tokens) < 2:
            errors.append({
                'type': 'INCOMPLETE_COMMAND',
                'message': 'El comando "generar" requiere un subcomando (reglas, informe)',
                'line': tokens[0]['line'],
                'column': tokens[0]['column'],
                'severity': 'error'
            })
        elif tokens[1]['value'] not in ['reglas', 'informe']:
            errors.append({
                'type': 'INVALID_SUBCOMMAND',
                'message': f'Subcomando inválido: "{tokens[1]["value"]}". Use: reglas, informe',
                'line': tokens[1]['line'],
                'column': tokens[1]['column'],
                'severity': 'error'
            })
        
        return errors
    
    def _validate_parameters(self, text: str, tokens: List[Dict]) -> List[Dict]:
        """Valida los parámetros del comando"""
        errors = []
        
        # Buscar parámetros con formato "clave: valor"
        param_pattern = r'(\w+):\s*(\w+)'
        for match in re.finditer(param_pattern, text):
            key, value = match.groups()
            
            # Validar que el valor no esté vacío
            if not value:
                errors.append({
                    'type': 'MISSING_VALUE',
                    'message': f'El parámetro "{key}" requiere un valor',
                    'line': text[:match.start()].count('\n') + 1,
                    'column': match.start(),
                    'severity': 'error'
                })
            
            # Validar valores específicos
            if key in self.valid_values:
                if value not in self.valid_values[key]:
                    errors.append({
                        'type': 'INVALID_VALUE',
                        'message': f'Valor inválido para "{key}": "{value}". Valores válidos: {", ".join(self.valid_values[key])}',
                        'line': text[:match.start()].count('\n') + 1,
                        'column': match.start(),
                        'severity': 'warning'
                    })
        
        return errors
    
    def _detect_warnings(self, text: str, tokens: List[Dict]) -> List[Dict]:
        """Detecta advertencias y mejoras sugeridas"""
        warnings = []
        
        # Advertencia: Comando muy largo
        if len(tokens) > 10:
            warnings.append({
                'type': 'LONG_COMMAND',
                'message': 'El comando es muy largo. Considera dividirlo en varios comandos.',
                'line': 1,
                'column': 0,
                'severity': 'info'
            })
        
        # Advertencia: Parámetros redundantes
        param_counts = {}
        for token in tokens:
            if token['type'] == 'PARAMETER':
                param_counts[token['value']] = param_counts.get(token['value'], 0) + 1
        
        for param, count in param_counts.items():
            if count > 1:
                warnings.append({
                    'type': 'DUPLICATE_PARAMETER',
                    'message': f'El parámetro "{param}" aparece {count} veces. Solo se usará la primera.',
                    'line': 1,
                    'column': 0,
                    'severity': 'warning'
                })
        
        return warnings
    
    def _generate_suggestions(self, text: str, errors: List[Dict]) -> List[str]:
        """Genera sugerencias de corrección basadas en errores"""
        suggestions = []
        
        for error in errors:
            if error['type'] == 'INVALID_COMMAND':
                suggestions.append('Comienza con una palabra clave válida: analizar, crear, monitorear, etc.')
            
            elif error['type'] == 'INCOMPLETE_COMMAND':
                suggestions.append('Completa el comando con los parámetros requeridos.')
            
            elif error['type'] == 'INVALID_SUBCOMMAND':
                suggestions.append('Verifica la ortografía del subcomando.')
            
            elif error['type'] == 'MISSING_PARAMETER':
                suggestions.append('Agrega el parámetro faltante (de, en, puerto, etc.)')
            
            elif error['type'] == 'MISSING_VALUE':
                suggestions.append('Proporciona un valor para el parámetro.')
            
            elif error['type'] == 'INVALID_VALUE':
                suggestions.append('Usa uno de los valores válidos sugeridos.')
        
        return list(set(suggestions))  # Eliminar duplicados
    
    def get_autocomplete_suggestions(self, text: str, cursor_pos: int) -> List[Dict]:
        """
        Proporciona sugerencias de autocompletado basadas en el contexto
        
        Returns:
            List[Dict] con sugerencias
        """
        suggestions = []
        
        # Obtener la palabra actual
        word_start = text.rfind(' ', 0, cursor_pos) + 1
        current_word = text[word_start:cursor_pos]
        
        # Obtener tokens antes del cursor
        tokens = self._tokenize(text[:cursor_pos])
        
        if not tokens:
            # Sugerir palabras clave
            for keyword in sorted(self.keywords):
                suggestions.append({
                    'text': keyword,
                    'type': 'keyword',
                    'description': f'Comando: {keyword}'
                })
        else:
            first_token = tokens[0]['value']
            
            # Sugerir subcomandos según el comando
            if first_token in self.subcommands:
                for subcommand in self.subcommands[first_token]:
                    if subcommand.startswith(current_word.lower()):
                        suggestions.append({
                            'text': subcommand,
                            'type': 'subcommand',
                            'description': f'Subcomando de {first_token}'
                        })
            
            # Sugerir parámetros
            for param in self.parameters:
                if param.startswith(current_word.lower()):
                    suggestions.append({
                        'text': param,
                        'type': 'parameter',
                        'description': f'Parámetro: {param}'
                    })
        
        return suggestions


def validate_guardian_command(text: str) -> Dict:
    """Función auxiliar para validar un comando Guardián"""
    validator = RealTimeValidator()
    return validator.validate(text)
