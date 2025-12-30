"""
Asistente de IA Conversacional para Creación de Bots en Guardián
Guía al usuario a través de un proceso interactivo para crear bots personalizados.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from bot_template_engine import GuardianBotTemplateEngine
import openai
import os


class GuardianBotAIAssistant:
    """Asistente de IA para la creación interactiva de bots de ciberseguridad"""
    
    def __init__(self):
        """Inicializa el asistente de IA"""
        self.template_engine = GuardianBotTemplateEngine()
        self.conversation_history = []
        self.current_session = None
        
        # Configurar OpenAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_base = os.getenv('OPENAI_API_BASE')
    
    def start_bot_creation_session(self, template_id: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Inicia una nueva sesión de creación de bot
        
        Args:
            template_id: ID de la plantilla seleccionada
            user_id: ID del usuario (para sesiones múltiples)
            
        Returns:
            Diccionario con información de la sesión iniciada
        """
        # Validar que la plantilla existe
        template = self.template_engine.get_template_details(template_id)
        if not template:
            return {
                'success': False,
                'error': f'Plantilla {template_id} no encontrada',
                'message': None
            }
        
        # Crear nueva sesión
        self.current_session = {
            'session_id': f"{user_id}_{template_id}_{self._get_timestamp()}",
            'user_id': user_id,
            'template_id': template_id,
            'template_info': template['template_info'],
            'parameters': {},
            'current_question_index': 0,
            'questions': self.template_engine.get_ai_questions_for_template(template_id),
            'conversation_history': [],
            'status': 'active'
        }
        
        # Obtener mensaje inicial
        initial_message = self._get_initial_message()
        
        return {
            'success': True,
            'session_id': self.current_session['session_id'],
            'message': initial_message,
            'template_info': template['template_info']
        }
    
    def process_user_response(self, session_id: str, user_response: str) -> Dict[str, Any]:
        """
        Procesa la respuesta del usuario y genera la siguiente pregunta o acción
        
        Args:
            session_id: ID de la sesión
            user_response: Respuesta del usuario
            
        Returns:
            Diccionario con la respuesta de la IA y el estado de la sesión
        """
        if not self.current_session or self.current_session['session_id'] != session_id:
            return {
                'success': False,
                'error': 'Sesión no válida o expirada',
                'message': None
            }
        
        # Agregar respuesta del usuario al historial
        self.current_session['conversation_history'].append({
            'type': 'user',
            'content': user_response,
            'timestamp': self._get_timestamp()
        })
        
        # Procesar la respuesta según el estado actual
        current_question = self._get_current_question()
        
        if current_question:
            # Extraer y validar parámetro de la respuesta
            extraction_result = self._extract_parameter_from_response(
                user_response, current_question
            )
            
            if extraction_result['success']:
                # Guardar parámetro extraído
                param_name = current_question['parameter']
                if param_name:
                    self.current_session['parameters'][param_name] = extraction_result['value']
                
                # Avanzar a la siguiente pregunta
                self.current_session['current_question_index'] += 1
                
                # Generar respuesta de la IA
                ai_response = self._generate_next_response()
                
            else:
                # Error en la extracción - pedir clarificación
                ai_response = self._generate_clarification_request(extraction_result['error'])
        
        else:
            # No hay más preguntas - finalizar creación del bot
            ai_response = self._finalize_bot_creation()
        
        # Agregar respuesta de la IA al historial
        self.current_session['conversation_history'].append({
            'type': 'assistant',
            'content': ai_response['message'],
            'timestamp': self._get_timestamp()
        })
        
        return ai_response
    
    def _get_initial_message(self) -> str:
        """Genera el mensaje inicial de la sesión"""
        template_info = self.current_session['template_info']
        questions = self.current_session['questions']
        
        # Buscar pregunta inicial en las preguntas de la plantilla
        initial_question = None
        for question in questions:
            if question['type'] == 'initial':
                initial_question = question['question']
                break
        
        if initial_question:
            return initial_question
        else:
            return f"¡Hola! Voy a ayudarte a crear un {template_info['name']}. {template_info['description']} ¿Estás listo para comenzar?"
    
    def _get_current_question(self) -> Optional[Dict]:
        """Obtiene la pregunta actual basándose en el índice"""
        questions = self.current_session['questions']
        index = self.current_session['current_question_index']
        
        # Filtrar solo preguntas de parámetros (saltar inicial y follow-up por ahora)
        parameter_questions = [q for q in questions if q['type'] == 'parameter']
        
        if index < len(parameter_questions):
            return parameter_questions[index]
        
        return None
    
    def _extract_parameter_from_response(self, user_response: str, question: Dict) -> Dict[str, Any]:
        """
        Extrae el valor del parámetro de la respuesta del usuario usando IA
        
        Args:
            user_response: Respuesta del usuario
            question: Información de la pregunta actual
            
        Returns:
            Diccionario con el resultado de la extracción
        """
        param_type = question['param_type']
        param_name = question['parameter']
        suggestions = question.get('suggestions', [])
        validation = question.get('validation', {})
        
        # Usar IA para extraer y validar el parámetro
        extraction_prompt = self._build_extraction_prompt(
            user_response, param_name, param_type, suggestions, validation
        )
        
        try:
            # Llamar a OpenAI para extraer el parámetro
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en ciberseguridad que ayuda a extraer parámetros técnicos de respuestas de usuarios. Responde solo con JSON válido."
                    },
                    {
                        "role": "user",
                        "content": extraction_prompt
                    }
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            # Parsear respuesta de la IA
            ai_response = response.choices[0].message.content.strip()
            result = json.loads(ai_response)
            
            # Validar el resultado
            if result.get('success', False):
                extracted_value = result.get('value')
                
                # Validación adicional según el tipo
                type_validation = self._validate_extracted_value(extracted_value, param_type, validation)
                
                if type_validation['valid']:
                    return {
                        'success': True,
                        'value': extracted_value,
                        'confidence': result.get('confidence', 0.8)
                    }
                else:
                    return {
                        'success': False,
                        'error': type_validation['error']
                    }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'No se pudo extraer el parámetro')
                }
                
        except Exception as e:
            # Fallback: extracción simple basada en patrones
            return self._fallback_parameter_extraction(user_response, param_type, suggestions)
    
    def _build_extraction_prompt(self, user_response: str, param_name: str, param_type: str, 
                                suggestions: List[str], validation: Dict) -> str:
        """Construye el prompt para extraer parámetros usando IA"""
        prompt = f"""
Extrae el valor del parámetro '{param_name}' de tipo '{param_type}' de la siguiente respuesta del usuario:

Respuesta del usuario: "{user_response}"

Información del parámetro:
- Nombre: {param_name}
- Tipo: {param_type}
- Sugerencias disponibles: {suggestions}
- Validaciones: {validation}

Instrucciones:
1. Analiza la respuesta del usuario para extraer el valor del parámetro
2. Si el usuario menciona una de las sugerencias, úsala
3. Si el usuario da una respuesta ambigua, intenta inferir la intención
4. Valida que el valor extraído sea del tipo correcto
5. Responde SOLO con JSON en este formato:

{{
    "success": true/false,
    "value": valor_extraído,
    "confidence": 0.0-1.0,
    "error": "mensaje de error si success es false"
}}

Ejemplos de tipos:
- string: cualquier texto
- integer: número entero
- array: lista de valores separados por comas
- ip_address: dirección IP válida
- interface: nombre de interfaz de red (eth0, wlan0, etc.)
"""
        return prompt
    
    def _validate_extracted_value(self, value: Any, param_type: str, validation: Dict) -> Dict[str, Any]:
        """Valida el valor extraído según el tipo y restricciones"""
        # Usar el validador del motor de plantillas
        if param_type == 'array' and isinstance(value, str):
            # Convertir string separado por comas a array
            value = [item.strip() for item in value.split(',') if item.strip()]
        
        # Validaciones básicas de tipo
        type_valid = self.template_engine._validate_parameter_type(value, param_type)
        if not type_valid:
            return {
                'valid': False,
                'error': f'Valor no válido para tipo {param_type}'
            }
        
        # Validaciones de restricciones
        constraint_errors = self.template_engine._validate_parameter_constraints(
            'param', value, validation
        )
        
        if constraint_errors:
            return {
                'valid': False,
                'error': constraint_errors[0]  # Primer error
            }
        
        return {'valid': True, 'error': None}
    
    def _fallback_parameter_extraction(self, user_response: str, param_type: str, 
                                     suggestions: List[str]) -> Dict[str, Any]:
        """Extracción de parámetros usando patrones simples como fallback"""
        user_response_lower = user_response.lower().strip()
        
        # Buscar en sugerencias primero
        for suggestion in suggestions:
            if suggestion.lower() in user_response_lower:
                return {
                    'success': True,
                    'value': suggestion,
                    'confidence': 0.9
                }
        
        # Patrones específicos por tipo
        if param_type == 'string':
            # Para strings, aceptar cualquier respuesta no vacía
            if user_response.strip():
                return {
                    'success': True,
                    'value': user_response.strip(),
                    'confidence': 0.8
                }
        
        elif param_type == 'integer':
            numbers = re.findall(r'\d+', user_response)
            if numbers:
                return {
                    'success': True,
                    'value': int(numbers[0]),
                    'confidence': 0.7
                }
        
        elif param_type == 'array':
            # Para arrays, dividir por comas
            if ',' in user_response:
                items = [item.strip() for item in user_response.split(',') if item.strip()]
                return {
                    'success': True,
                    'value': items,
                    'confidence': 0.8
                }
            elif user_response.strip():
                # Un solo elemento
                return {
                    'success': True,
                    'value': [user_response.strip()],
                    'confidence': 0.7
                }
        
        elif param_type == 'ip_address':
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ips = re.findall(ip_pattern, user_response)
            if ips:
                return {
                    'success': True,
                    'value': ips[0],
                    'confidence': 0.8
                }
        
        elif param_type == 'interface':
            interface_pattern = r'\b(eth\d+|wlan\d+|enp\d+s\d+|lo)\b'
            interfaces = re.findall(interface_pattern, user_response)
            if interfaces:
                return {
                    'success': True,
                    'value': interfaces[0],
                    'confidence': 0.8
                }
        
        elif param_type == 'boolean':
            if any(word in user_response_lower for word in ['sí', 'si', 'yes', 'true', 'verdadero']):
                return {'success': True, 'value': True, 'confidence': 0.9}
            elif any(word in user_response_lower for word in ['no', 'false', 'falso']):
                return {'success': True, 'value': False, 'confidence': 0.9}
        
        # Si no se puede extraer, devolver error
        return {
            'success': False,
            'error': f'No se pudo extraer un valor válido de tipo {param_type} de la respuesta'
        }
    
    def _generate_next_response(self) -> Dict[str, Any]:
        """Genera la siguiente respuesta de la IA"""
        current_question = self._get_current_question()
        
        if current_question:
            # Hay más preguntas - hacer la siguiente
            message = self._format_question_with_context(current_question)
            
            return {
                'success': True,
                'message': message,
                'type': 'question',
                'question_info': current_question,
                'progress': self._calculate_progress()
            }
        else:
            # No hay más preguntas - generar recomendaciones finales
            return self._generate_final_recommendations()
    
    def _format_question_with_context(self, question: Dict) -> str:
        """Formatea una pregunta con contexto adicional"""
        base_question = question['question']
        suggestions = question.get('suggestions', [])
        
        # Agregar sugerencias si las hay
        if suggestions:
            suggestions_text = "\\n".join([f"  • {suggestion}" for suggestion in suggestions])
            return f"{base_question}\\n\\nSugerencias:\\n{suggestions_text}"
        
        return base_question
    
    def _generate_final_recommendations(self) -> Dict[str, Any]:
        """Genera recomendaciones finales antes de crear el bot"""
        template_id = self.current_session['template_id']
        parameters = self.current_session['parameters']
        
        # Obtener recomendaciones de la plantilla
        template_recommendations = self.template_engine.get_ai_recommendations_for_template(template_id)
        
        # Generar recomendaciones personalizadas usando IA
        personalized_recommendations = self._generate_personalized_recommendations(parameters)
        
        all_recommendations = template_recommendations + personalized_recommendations
        
        recommendations_text = "\\n".join([f"💡 {rec}" for rec in all_recommendations[:5]])
        
        message = f"""¡Excelente! He recopilado toda la información necesaria para crear tu bot. 

📋 **Resumen de configuración:**
{self._format_parameters_summary()}

🎯 **Recomendaciones finales:**
{recommendations_text}

¿Estás listo para generar el bot? Responde 'sí' para continuar o 'modificar' si quieres cambiar algún parámetro."""
        
        return {
            'success': True,
            'message': message,
            'type': 'final_confirmation',
            'parameters_summary': self.current_session['parameters'],
            'recommendations': all_recommendations,
            'progress': 100
        }
    
    def _generate_personalized_recommendations(self, parameters: Dict) -> List[str]:
        """Genera recomendaciones personalizadas usando IA"""
        try:
            # Construir prompt para recomendaciones personalizadas
            prompt = f"""
Basándote en los siguientes parámetros de configuración de un bot de ciberseguridad, 
genera 3 recomendaciones específicas y prácticas:

Parámetros: {json.dumps(parameters, indent=2)}

Las recomendaciones deben ser:
1. Específicas para esta configuración
2. Orientadas a mejorar la seguridad
3. Prácticas y implementables

Responde con una lista JSON de strings:
["recomendación 1", "recomendación 2", "recomendación 3"]
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en ciberseguridad que proporciona recomendaciones prácticas y específicas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            ai_response = response.choices[0].message.content.strip()
            recommendations = json.loads(ai_response)
            
            return recommendations if isinstance(recommendations, list) else []
            
        except Exception as e:
            # Fallback: recomendaciones genéricas
            return [
                "Considera implementar logging detallado para auditoría",
                "Asegúrate de tener un plan de respaldo antes de activar el bot",
                "Prueba el bot en un entorno de desarrollo primero"
            ]
    
    def _format_parameters_summary(self) -> str:
        """Formatea un resumen de los parámetros configurados"""
        parameters = self.current_session['parameters']
        summary_lines = []
        
        for param_name, param_value in parameters.items():
            # Formatear el nombre del parámetro
            formatted_name = param_name.replace('_', ' ').title()
            
            # Formatear el valor
            if isinstance(param_value, list):
                formatted_value = ', '.join(str(v) for v in param_value)
            else:
                formatted_value = str(param_value)
            
            summary_lines.append(f"  • {formatted_name}: {formatted_value}")
        
        return "\\n".join(summary_lines)
    
    def _generate_clarification_request(self, error: str) -> Dict[str, Any]:
        """Genera una solicitud de clarificación cuando hay errores"""
        current_question = self._get_current_question()
        
        message = f"""Lo siento, no pude entender tu respuesta. {error}

¿Podrías proporcionar la información de otra manera?

Pregunta original: {current_question['question']}"""
        
        if current_question.get('suggestions'):
            suggestions_text = "\\n".join([f"  • {s}" for s in current_question['suggestions']])
            message += f"\\n\\nSugerencias:\\n{suggestions_text}"
        
        return {
            'success': True,
            'message': message,
            'type': 'clarification',
            'question_info': current_question,
            'progress': self._calculate_progress()
        }
    
    def _calculate_progress(self) -> int:
        """Calcula el progreso de la sesión como porcentaje"""
        total_questions = len([q for q in self.current_session['questions'] if q['type'] == 'parameter'])
        current_index = self.current_session['current_question_index']
        
        if total_questions == 0:
            return 100
        
        return min(int((current_index / total_questions) * 100), 100)
    
    def finalize_and_generate_bot(self, session_id: str) -> Dict[str, Any]:
        """
        Finaliza la sesión y genera el código del bot
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Diccionario con el bot generado y metadata
        """
        if not self.current_session or self.current_session['session_id'] != session_id:
            return {
                'success': False,
                'error': 'Sesión no válida o expirada'
            }
        
        template_id = self.current_session['template_id']
        parameters = self.current_session['parameters']
        
        # Generar el bot usando el motor de plantillas
        generation_result = self.template_engine.generate_bot_code(template_id, parameters)
        
        if generation_result['success']:
            # Validar el bot generado
            validation_result = self.template_engine.validate_generated_bot(
                template_id, generation_result['code'], parameters
            )
            
            # Marcar sesión como completada
            self.current_session['status'] = 'completed'
            
            return {
                'success': True,
                'bot_code': generation_result['code'],
                'metadata': generation_result['metadata'],
                'validation': validation_result,
                'session_summary': self._generate_session_summary()
            }
        else:
            return {
                'success': False,
                'error': 'Error al generar el bot',
                'details': generation_result['errors']
            }
    
    def _finalize_bot_creation(self) -> Dict[str, Any]:
        """Finaliza el proceso de creación del bot"""
        return {
            'success': True,
            'message': "¡Perfecto! Tengo toda la información necesaria. Generando tu bot personalizado...",
            'type': 'generating',
            'progress': 100
        }
    
    def _generate_session_summary(self) -> Dict[str, Any]:
        """Genera un resumen de la sesión completada"""
        return {
            'session_id': self.current_session['session_id'],
            'template_used': self.current_session['template_info']['name'],
            'parameters_configured': len(self.current_session['parameters']),
            'conversation_turns': len(self.current_session['conversation_history']),
            'created_at': self.current_session.get('created_at', self._get_timestamp())
        }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Obtiene el estado actual de una sesión"""
        if not self.current_session or self.current_session['session_id'] != session_id:
            return {
                'exists': False,
                'error': 'Sesión no encontrada'
            }
        
        return {
            'exists': True,
            'session_id': session_id,
            'template_id': self.current_session['template_id'],
            'template_name': self.current_session['template_info']['name'],
            'progress': self._calculate_progress(),
            'status': self.current_session['status'],
            'parameters_collected': len(self.current_session['parameters']),
            'total_parameters': len([q for q in self.current_session['questions'] if q['type'] == 'parameter'])
        }
    
    def _get_timestamp(self) -> str:
        """Obtiene timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()


# Funciones de utilidad para el asistente
def create_ai_assistant() -> GuardianBotAIAssistant:
    """Crea una instancia del asistente de IA"""
    return GuardianBotAIAssistant()


if __name__ == "__main__":
    # Prueba básica del asistente de IA
    print("🤖 Probando Asistente de IA para Bots de Guardián...")
    
    assistant = create_ai_assistant()
    
    # Iniciar sesión de prueba
    session_result = assistant.start_bot_creation_session('network_monitoring_bot', 'test_user')
    
    if session_result['success']:
        print("✅ Sesión iniciada exitosamente!")
        print(f"📝 Mensaje inicial: {session_result['message']}")
        print(f"🆔 Session ID: {session_result['session_id']}")
        
        # Simular algunas respuestas
        test_responses = [
            "Monitor de Red Principal",  # bot_name
            "eth0",                      # interface
            "1500",                      # attack_threshold
            "192.168.1.1, 192.168.1.10", # allowed_ips
            "continuo",                  # monitoring_duration
            "alto"                       # alert_level
        ]
        
        session_id = session_result['session_id']
        
        for i, response in enumerate(test_responses):
            print(f"\\n👤 Usuario: {response}")
            
            ai_response = assistant.process_user_response(session_id, response)
            
            if ai_response['success']:
                print(f"🤖 IA: {ai_response['message']}")
                print(f"📊 Progreso: {ai_response.get('progress', 0)}%")
                
                if ai_response.get('type') == 'generating':
                    # Finalizar y generar bot
                    final_result = assistant.finalize_and_generate_bot(session_id)
                    if final_result['success']:
                        print("\\n🎉 ¡Bot generado exitosamente!")
                        print(f"📝 Código generado ({len(final_result['bot_code'])} caracteres)")
                        print(f"⚠️  Advertencias de seguridad: {len(final_result['validation']['warnings'])}")
                    break
            else:
                print(f"❌ Error: {ai_response['error']}")
                break
    else:
        print(f"❌ Error al iniciar sesión: {session_result['error']}")

