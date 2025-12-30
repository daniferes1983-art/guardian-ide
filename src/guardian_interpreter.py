import re
import subprocess
import platform
import os
import asyncio
from guardian_ai_enhanced import guardian_ai

class GuardianInterpreter:
    def __init__(self):
        pass

    def execute(self, ast):
        command = ast["command"]
        if command == "analizar_puertos":
            self._analizar_puertos(ast["ip"])
        elif command == "crear_regla_firewall":
            self._crear_regla_firewall(ast["puerto"], ast["protocolo"], ast["accion"])
        elif command == "leer_logs":
            self._leer_logs(ast["ruta_archivo"])
        elif command == "monitorear_trafico":
            self._monitorear_trafico(ast["interfaz"])
        elif command == "alertar":
            self._alertar(ast["mensaje"])
        elif command == "ver_procesos":
            self._ver_procesos()
        # Nuevos comandos de IA
        elif command == "analizar_amenazas_tiempo_real":
            self._analizar_amenazas_tiempo_real(ast.get("interfaz", "eth0"))
        elif command == "detectar_anomalias":
            self._detectar_anomalias(ast["interfaz"])
        elif command == "evaluar_vulnerabilidades":
            self._evaluar_vulnerabilidades(ast["rango_ip"])
        elif command == "predecir_ataques":
            self._predecir_ataques()
        elif command == "generar_reglas_firewall_inteligentes":
            self._generar_reglas_firewall_inteligentes(ast["contexto"])
        elif command == "optimizar_politicas_seguridad":
            self._optimizar_politicas_seguridad()
        elif command == "monitorear_con_ia":
            self._monitorear_con_ia(ast["interfaz"])
        elif command == "alertar_con_contexto_inteligente":
            self._alertar_con_contexto_inteligente(ast["tipo_amenaza"])
        elif command == "generar_informe_riesgo_ia":
            self._generar_informe_riesgo_ia()
        elif command == "recomendar_acciones_mitigacion":
            self._recomendar_acciones_mitigacion()
        else:
            print(f"Error: Comando desconocido '{command}'")

    def _analizar_puertos(self, ip):
        print(f"Analizando puertos en {ip}...")
        print(f"Simulando nmap -p 1-1000 {ip}")
        print("Puerto 22 (SSH) abierto")
        print("Puerto 80 (HTTP) abierto")
        if ip == "192.168.1.1":
            print("Puerto 443 (HTTPS) abierto")
            print("Puerto 53 (DNS) abierto")

    def _crear_regla_firewall(self, puerto, protocolo, accion):
        print(f"Creando regla de firewall:")
        print(f"  Puerto: {puerto}")
        print(f"  Protocolo: {protocolo}")
        print(f"  Acción: {accion}")
        print(f"Simulando: iptables -A INPUT -p {protocolo.lower()} --dport {puerto} -j {accion.upper()}")

    def _leer_logs(self, ruta_archivo):
        print(f"Leyendo logs de {ruta_archivo}...")
        try:
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r') as f:
                    lines = f.readlines()
                    print(f"Mostrando las últimas 10 líneas de {len(lines)} líneas totales:")
                    for line in lines[-10:]:
                        print(line.strip())
            else:
                print(f"Archivo {ruta_archivo} no encontrado. Simulando contenido de log:")
                print("2023-12-06 10:30:15 [INFO] Sistema iniciado correctamente")
                print("2023-12-06 10:31:22 [WARNING] Intento de conexión desde IP desconocida: 192.168.1.100")
                print("2023-12-06 10:32:05 [ERROR] Fallo de autenticación para usuario 'admin'")
                print("2023-12-06 10:33:18 [INFO] Conexión SSH establecida desde 192.168.1.50")
        except Exception as e:
            print(f"Error al leer logs: {e}")

    def _monitorear_trafico(self, interfaz):
        print(f"Monitoreando tráfico en interfaz {interfaz}...")
        print("Simulando captura de paquetes...")

    def _alertar(self, mensaje):
        # Limpiar el mensaje de comillas si las tiene
        mensaje_limpio = mensaje.strip('"\'')
        print(f"🚨 ALERTA: {mensaje_limpio}")
        print(f"Timestamp: {subprocess.check_output(['date'], text=True).strip()}")
        print("Alerta enviada al sistema de monitoreo")

    def _ver_procesos(self):
        print("Procesos activos del sistema:")
        try:
            if platform.system() == "Linux":
                result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                lines = result.stdout.split('\n')[:10]  # Mostrar solo los primeros 10 procesos
                for line in lines:
                    if line.strip():
                        print(line)
            elif platform.system() == "Windows":
                subprocess.run(["tasklist"])
            else:
                print("Visualización de procesos no compatible con este sistema operativo.")
        except Exception as e:
            print(f"Error al ver procesos: {e}")

    # Métodos de IA mejorados
    def _analizar_amenazas_tiempo_real(self, interfaz):
        """Análisis de amenazas en tiempo real con IA"""
        print(f"🤖 Iniciando análisis de amenazas en tiempo real en {interfaz}...")
        try:
            # Usar asyncio para ejecutar la función asíncrona
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            resultado = loop.run_until_complete(guardian_ai.analyze_threats_real_time(interfaz))
            loop.close()
            
            print(f"📊 Métricas de red:")
            print(f"  - Tasa de paquetes: {resultado['metrics']['packet_rate']} pps")
            print(f"  - Tasa de conexiones: {resultado['metrics']['connection_rate']} cps")
            print(f"  - Conexiones activas: {resultado['metrics']['active_connections']}")
            
            print(f"\n🎯 Nivel de riesgo: {resultado['risk_level'].upper()}")
            
            if resultado['threats_detected']:
                print(f"\n⚠️  Amenazas detectadas:")
                for amenaza in resultado['threats_detected']:
                    print(f"    • {amenaza['type']}: {amenaza['description']} (Confianza: {amenaza['confidence']:.1%})")
            
            if resultado['recommendations']:
                print(f"\n💡 Recomendaciones:")
                for rec in resultado['recommendations']:
                    print(f"    • {rec}")
                    
            if 'ai_analysis' in resultado:
                print(f"\n🧠 Análisis de IA:")
                print(f"    {resultado['ai_analysis']}")
                    
        except Exception as e:
            print(f"❌ Error en análisis de amenazas: {e}")

    def _detectar_anomalias(self, interfaz):
        """Detección de anomalías con IA"""
        print(f"🔍 Detectando anomalías en {interfaz} con IA...")
        try:
            resultado = guardian_ai.detect_anomalies(interfaz)
            
            print(f"📈 Baseline de red:")
            print(f"  - Tasa promedio de paquetes: {resultado['baseline']['avg_packet_rate']}")
            print(f"  - Tasa promedio de conexiones: {resultado['baseline']['avg_connection_rate']}")
            
            print(f"\n📊 Métricas actuales:")
            print(f"  - Tasa de paquetes: {resultado['current_metrics']['packet_rate']}")
            print(f"  - Tasa de conexiones: {resultado['current_metrics']['connection_rate']}")
            
            print(f"\n🎯 Puntuación de anomalía: {resultado['anomaly_score']:.2f}")
            
            if resultado['anomalies']:
                print(f"\n⚠️  Anomalías detectadas:")
                for anomalia in resultado['anomalies']:
                    print(f"    • {anomalia['type']} ({anomalia['severity']}): {anomalia['description']}")
            else:
                print("\n✅ No se detectaron anomalías significativas")
                
        except Exception as e:
            print(f"❌ Error en detección de anomalías: {e}")

    def _evaluar_vulnerabilidades(self, rango_ip):
        """Evaluación de vulnerabilidades con IA"""
        print(f"🛡️  Evaluando vulnerabilidades en {rango_ip}...")
        try:
            resultado = guardian_ai.evaluate_vulnerabilities(rango_ip)
            
            print(f"📊 Resumen del escaneo:")
            print(f"  - Vulnerabilidades encontradas: {resultado['total_vulnerabilities']}")
            print(f"  - Puntuación de riesgo: {resultado['risk_score']}/10")
            print(f"  - Nivel de riesgo: {resultado['risk_level'].upper()}")
            
            if resultado['vulnerabilities_found']:
                print(f"\n🔍 Vulnerabilidades críticas:")
                for vuln in resultado['vulnerabilities_found'][:3]:  # Mostrar solo las primeras 3
                    print(f"    • {vuln['cve_id']}: {vuln['description']}")
                    print(f"      Severidad: {vuln['severity']} (CVSS: {vuln['cvss_score']})")
                    print(f"      Hosts afectados: {len(vuln['affected_hosts'])}")
            
            if resultado['recommendations']:
                print(f"\n💡 Recomendaciones:")
                for rec in resultado['recommendations'][:3]:  # Mostrar solo las primeras 3
                    print(f"    • {rec}")
                    
        except Exception as e:
            print(f"❌ Error en evaluación de vulnerabilidades: {e}")

    def _predecir_ataques(self):
        """Predicción de ataques con IA"""
        print(f"🔮 Prediciendo posibles ataques...")
        try:
            resultado = guardian_ai.predict_attacks()
            
            print(f"📊 Análisis predictivo:")
            print(f"  - Probabilidad de ataque en 24h: {resultado['attack_probability']:.1%}")
            print(f"  - Nivel de riesgo: {resultado['risk_level'].upper()}")
            print(f"  - Confianza del modelo: {resultado['model_confidence']:.1%}")
            
            if resultado['predicted_attack_types']:
                print(f"\n🎯 Tipos de ataque más probables:")
                for ataque in resultado['predicted_attack_types']:
                    print(f"    • {ataque['type']}: {ataque['probability']:.1%} de probabilidad")
                    print(f"      Descripción: {ataque['description']}")
            
            if resultado['recommendations']:
                print(f"\n🛡️  Medidas preventivas recomendadas:")
                for rec in resultado['recommendations']:
                    print(f"    • {rec}")
                    
        except Exception as e:
            print(f"❌ Error en predicción de ataques: {e}")

    def _generar_reglas_firewall_inteligentes(self, contexto):
        """Generación inteligente de reglas de firewall"""
        print(f"🧠 Generando reglas de firewall inteligentes para: {contexto}")
        try:
            resultado = guardian_ai.generate_intelligent_firewall_rules(contexto)
            
            print(f"📋 Reglas generadas ({len(resultado['rules'])} reglas):")
            for i, regla in enumerate(resultado['rules'][:5], 1):  # Mostrar solo las primeras 5
                print(f"  {i}. {regla['rule']}")
                print(f"     Justificación: {regla['justification']}")
                print(f"     Prioridad: {regla['priority']}")
            
            if len(resultado['rules']) > 5:
                print(f"     ... y {len(resultado['rules']) - 5} reglas más")
            
            print(f"\n📊 Estadísticas:")
            print(f"  - Reglas de bloqueo: {resultado['stats']['blocking_rules']}")
            print(f"  - Reglas de permitir: {resultado['stats']['allowing_rules']}")
            print(f"  - Reglas de logging: {resultado['stats']['logging_rules']}")
            
            if resultado['recommendations']:
                print(f"\n💡 Recomendaciones adicionales:")
                for rec in resultado['recommendations']:
                    print(f"    • {rec}")
                    
        except Exception as e:
            print(f"❌ Error en generación de reglas: {e}")

    def _optimizar_politicas_seguridad(self):
        """Optimización automática de políticas de seguridad"""
        print(f"⚙️  Optimizando políticas de seguridad...")
        try:
            resultado = guardian_ai.optimize_security_policies()
            
            print(f"📊 Análisis de políticas actuales:")
            print(f"  - Políticas analizadas: {resultado['policies_analyzed']}")
            print(f"  - Políticas redundantes: {resultado['redundant_policies']}")
            print(f"  - Políticas conflictivas: {resultado['conflicting_policies']}")
            print(f"  - Puntuación de eficiencia: {resultado['efficiency_score']:.1f}/10")
            
            if resultado['optimizations']:
                print(f"\n🔧 Optimizaciones recomendadas:")
                for opt in resultado['optimizations']:
                    print(f"    • {opt['type']}: {opt['description']}")
                    print(f"      Impacto esperado: {opt['expected_impact']}")
            
            if resultado['consolidated_rules']:
                print(f"\n📋 Reglas consolidadas:")
                for regla in resultado['consolidated_rules'][:3]:  # Mostrar solo las primeras 3
                    print(f"    • {regla}")
                    
        except Exception as e:
            print(f"❌ Error en optimización de políticas: {e}")

    def _monitorear_con_ia(self, interfaz):
        """Monitoreo avanzado con IA"""
        print(f"👁️  Iniciando monitoreo avanzado con IA en {interfaz}...")
        try:
            resultado = guardian_ai.advanced_monitoring(interfaz)
            
            print(f"📊 Estado del monitoreo:")
            print(f"  - Interfaz: {resultado['interface']}")
            print(f"  - Estado: {resultado['status']}")
            print(f"  - Tiempo de actividad: {resultado['uptime']}")
            
            print(f"\n📈 Métricas en tiempo real:")
            for metrica, valor in resultado['real_time_metrics'].items():
                print(f"  - {metrica}: {valor}")
            
            if resultado['alerts']:
                print(f"\n🚨 Alertas activas:")
                for alerta in resultado['alerts']:
                    print(f"    • {alerta['severity']}: {alerta['message']}")
            
            if resultado['ai_insights']:
                print(f"\n🧠 Insights de IA:")
                for insight in resultado['ai_insights']:
                    print(f"    • {insight}")
                    
        except Exception as e:
            print(f"❌ Error en monitoreo con IA: {e}")

    def _alertar_con_contexto_inteligente(self, tipo_amenaza):
        """Alertas con contexto inteligente"""
        print(f"🚨 Generando alerta inteligente para: {tipo_amenaza}")
        try:
            resultado = guardian_ai.generate_intelligent_alert(tipo_amenaza)
            
            print(f"📋 Detalles de la alerta:")
            print(f"  - Tipo: {resultado['alert_type']}")
            print(f"  - Severidad: {resultado['severity']}")
            print(f"  - Confianza: {resultado['confidence']:.1%}")
            print(f"  - Timestamp: {resultado['timestamp']}")
            
            print(f"\n📝 Descripción:")
            print(f"  {resultado['description']}")
            
            if resultado['context']:
                print(f"\n🔍 Contexto adicional:")
                for contexto in resultado['context']:
                    print(f"    • {contexto}")
            
            if resultado['recommended_actions']:
                print(f"\n⚡ Acciones recomendadas:")
                for accion in resultado['recommended_actions']:
                    print(f"    • {accion}")
                    
        except Exception as e:
            print(f"❌ Error en alerta inteligente: {e}")

    def _generar_informe_riesgo_ia(self):
        """Generación de informe de riesgo con IA"""
        print(f"📊 Generando informe de riesgo con IA...")
        try:
            resultado = guardian_ai.generate_risk_report()
            
            print(f"📋 Resumen ejecutivo:")
            print(f"  - Puntuación de riesgo global: {resultado['overall_risk_score']:.1f}/10")
            print(f"  - Nivel de riesgo: {resultado['risk_level'].upper()}")
            print(f"  - Tendencia: {resultado['risk_trend']}")
            
            print(f"\n🎯 Principales riesgos identificados:")
            for riesgo in resultado['top_risks']:
                print(f"    • {riesgo['category']}: {riesgo['description']} (Impacto: {riesgo['impact']})")
            
            print(f"\n📈 Métricas de seguridad:")
            for metrica, valor in resultado['security_metrics'].items():
                print(f"  - {metrica}: {valor}")
            
            if resultado['recommendations']:
                print(f"\n💡 Recomendaciones prioritarias:")
                for rec in resultado['recommendations'][:5]:  # Mostrar solo las primeras 5
                    print(f"    • {rec}")
                    
        except Exception as e:
            print(f"❌ Error en generación de informe: {e}")

    def _recomendar_acciones_mitigacion(self):
        """Recomendaciones de mitigación con IA"""
        print(f"💡 Generando recomendaciones de mitigación...")
        try:
            resultado = guardian_ai.recommend_mitigation_actions()
            
            print(f"📊 Análisis de mitigación:")
            print(f"  - Vulnerabilidades analizadas: {resultado['vulnerabilities_analyzed']}")
            print(f"  - Recomendaciones generadas: {len(resultado['recommendations'])}")
            print(f"  - Prioridad promedio: {resultado['average_priority']}")
            
            print(f"\n🎯 Recomendaciones por prioridad:")
            
            # Agrupar por prioridad
            prioridades = {}
            for rec in resultado['recommendations']:
                prioridad = rec['priority']
                if prioridad not in prioridades:
                    prioridades[prioridad] = []
                prioridades[prioridad].append(rec)
            
            for prioridad in ['CRÍTICA', 'ALTA', 'MEDIA', 'BAJA']:
                if prioridad in prioridades:
                    print(f"\n  🔴 Prioridad {prioridad}:")
                    for rec in prioridades[prioridad][:3]:  # Mostrar solo las primeras 3 por prioridad
                        print(f"    • {rec['action']}")
                        print(f"      Impacto esperado: {rec['expected_impact']}")
                        print(f"      Esfuerzo requerido: {rec['effort_required']}")
            
            if resultado['implementation_timeline']:
                print(f"\n📅 Cronograma de implementación sugerido:")
                for fase in resultado['implementation_timeline']:
                    print(f"    • {fase['phase']}: {fase['duration']} - {fase['description']}")
                    
        except Exception as e:
            print(f"❌ Error en recomendaciones de mitigación: {e}")


# Example Usage (for testing)
if __name__ == "__main__":
    from guardian_lexer import GuardianLexer
    from guardian_parser import GuardianParser

    lexer = GuardianLexer()
    parser = GuardianParser(lexer)
    interpreter = GuardianInterpreter()

    test_commands = [
        "analizar puertos de 127.0.0.1",
        "detectar anomalias en trafico de eth0",
        "predecir ataques"
    ]

    for command in test_commands:
        print(f"\n--- Ejecutando: {command} ---")
        try:
            ast = parser.parse(command)
            interpreter.execute(ast)
        except ValueError as e:
            print(f"Error al parsear o ejecutar: {e}")
