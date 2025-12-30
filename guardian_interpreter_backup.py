
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
            print(f"Error: Comando desconocido ")

    def _analizar_puertos(self, ip):
        print(f"Analizando puertos en {ip}...")
        try:
            # Simulate nmap for now
            print(f"Simulando nmap -p 1-1000 {ip}")
            # In a real scenario, you would run: subprocess.run(["nmap", "-p", "1-1000", ip], check=True)
            print("Puerto 22 (SSH) abierto")
            print("Puerto 80 (HTTP) abierto")
        except Exception as e:
            print(f"Error al analizar puertos: {e}")

    def _crear_regla_firewall(self, puerto, protocolo, accion):
        print(f"Creando regla de firewall: puerto={puerto}, protocolo={protocolo}, accion={accion}...")
        if platform.system() == "Linux":
            try:
                # Simulate iptables for now
                print(f"Simulando iptables -A INPUT -p {protocolo.lower()} --dport {puerto} -j {accion.upper()}")
                # In a real scenario, you would run: subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", protocolo.lower(), "--dport", str(puerto), "-j", accion.upper()], check=True)
                print("Regla de firewall creada exitosamente.")
            except Exception as e:
                print(f"Error al crear regla de firewall: {e}")
        else:
            print("La creación de reglas de firewall solo es compatible con Linux en esta simulación.")

    def _leer_logs(self, ruta_archivo):
        print(f"Leyendo logs de {ruta_archivo}...")
        try:
            # Simulate reading log file
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, "r") as f:
                    for i, line in enumerate(f):
                        print(line.strip())
                        if i >= 9: # Read first 10 lines
                            break
            else:
                print(f"Error: El archivo {ruta_archivo} no existe.")
        except Exception as e:
            print(f"Error al leer logs: {e}")

    def _monitorear_trafico(self, interfaz):
        print(f"Monitoreando tráfico en la interfaz {interfaz} (simulado)...")
        print("Simulación de tráfico de red: Paquetes entrantes y salientes.")

    def _alertar(self, mensaje):
        print(f"ALERTA: {mensaje}")
        # Simulate sound alert (platform-dependent)
        if platform.system() == "Darwin": # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Basso.aiff"])
        elif platform.system() == "Linux":
            try:
                subprocess.run(["paplay", "/usr/share/sounds/gnome/default/alerts/drip.ogg"], check=True)
            except FileNotFoundError:
                print("Advertencia: paplay no encontrado. No se pudo reproducir el sonido de alerta.")
            except Exception as e:
                print(f"Error al reproducir sonido de alerta en Linux: {e}")
        elif platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500) # Frequency, Duration

    def _ver_procesos(self):
        print("Mostrando procesos activos...")
        try:
            if platform.system() == "Linux":
                subprocess.run(["ps", "aux"])
            elif platform.system() == "Windows":
                subprocess.run(["tasklist"])
            else:
                print("Visualización de procesos no compatible con este sistema operativo.")
        except Exception as e:
            print(f"Error al ver procesos: {e}")

    # Métodos de IA mejorados
    def _analizar_amenazas_tiempo_real(self, interfaz):
    from guardian_lexer import GuardianLexer
    from guardian_parser import GuardianParser

    lexer = GuardianLexer()
    parser = GuardianParser(lexer)
    interpreter = GuardianInterpreter()

    test_commands = [
        "analizar puertos de 127.0.0.1",
        "crear regla firewall puerto: 80 protocolo: TCP accion: bloquear",
        "leer logs de /var/log/syslog", # This file might not exist in sandbox, will show error
        "monitorear trafico en eth0",
        "alertar Intrusión detectada!",
        "ver procesos activos",
        "alertar \"Mensaje con espacios\"",
        "crear regla firewall puerto: 22 protocolo: UDP accion: permitir"
    ]

    for cmd_str in test_commands:
        print(f"\n--- Ejecutando: {cmd_str} ---")
        try:
            ast = parser.parse(cmd_str)
            interpreter.execute(ast)
        except ValueError as e:
            print(f"Error al parsear o ejecutar: {e}")

    # Test with a non-existent log file
    print("\n--- Ejecutando: leer logs de /ruta/inexistente/log.txt ---")
    try:
        ast = parser.parse("leer logs de /ruta/inexistente/log.txt")
        interpreter.execute(ast)
    except ValueError as e:
        print(f"Error al parsear o ejecutar: {e}")

    # Test with an invalid command
    print("\n--- Ejecutando: comando_invalido ---")
    try:
        ast = parser.parse("comando_invalido")
        interpreter.execute(ast)
    except ValueError as e:
        print(f"Error al parsear o ejecutar: {e}")


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
            
            print(f"📊 Nivel de amenaza general: {resultado['overall_threat_level'].upper()}")
            
            if resultado['predictions']:
                print(f"\n🎯 Predicciones de ataques:")
                for pred in resultado['predictions']:
                    print(f"    • {pred['attack_type']}: {pred['probability']:.1%} probabilidad")
                    print(f"      Ventana de tiempo: {pred['time_window']}")
                    print(f"      Razón: {pred['reasoning']}")
                    print()
            
            if resultado['recommended_actions']:
                print(f"💡 Acciones preventivas recomendadas:")
                for accion in resultado['recommended_actions']:
                    print(f"    • {accion}")
                    
        except Exception as e:
            print(f"❌ Error en predicción de ataques: {e}")

    def _generar_reglas_firewall_inteligentes(self, contexto):
        """Generación inteligente de reglas de firewall"""
        print(f"🛡️  Generando reglas de firewall inteligentes para: {contexto}")
        try:
            resultado = guardian_ai.generate_intelligent_firewall_rules(contexto)
            
            print(f"📋 Configuración: {resultado['description']}")
            print(f"🔒 Nivel de seguridad: {resultado['security_level'].upper()}")
            print(f"⚡ Impacto en rendimiento: {resultado['estimated_performance_impact']}")
            
            print(f"\n🛡️  Reglas generadas ({resultado['total_rules']} total):")
            for i, regla in enumerate(resultado['rules'][:5], 1):  # Mostrar solo las primeras 5
                accion = regla['action']
                puerto = regla['port']
                protocolo = regla['protocol']
                origen = regla['source']
                
                print(f"    {i}. {accion.upper()} puerto {puerto} ({protocolo}) desde {origen}")
                if 'description' in regla:
                    print(f"       → {regla['description']}")
            
            if len(resultado['rules']) > 5:
                print(f"    ... y {len(resultado['rules']) - 5} reglas más")
            
            if resultado['implementation_notes']:
                print(f"\n📝 Notas de implementación:")
                for nota in resultado['implementation_notes'][:3]:
                    print(f"    • {nota}")
                    
        except Exception as e:
            print(f"❌ Error en generación de reglas: {e}")

    def _optimizar_politicas_seguridad(self):
        """Optimización de políticas de seguridad"""
        print(f"⚙️  Optimizando políticas de seguridad...")
        try:
            resultado = guardian_ai.optimize_security_policies()
            
            print(f"📊 Análisis de políticas actuales:")
            for politica, cantidad in resultado['current_policies'].items():
                print(f"  - {politica.replace('_', ' ').title()}: {cantidad}")
            
            print(f"\n🔍 Análisis de eficiencia:")
            for problema, cantidad in resultado['efficiency_analysis'].items():
                if cantidad > 0:
                    print(f"  - {problema.replace('_', ' ').title()}: {cantidad}")
            
            if resultado['optimizations']:
                print(f"\n💡 Optimizaciones recomendadas:")
                for opt in resultado['optimizations']:
                    print(f"    • {opt['description']} (Prioridad: {opt['priority']})")
                    print(f"      Impacto: {opt['impact']}")
            
            print(f"\n📈 Mejoras estimadas:")
            for aspecto, mejora in resultado['estimated_improvement'].items():
                print(f"  - {aspecto.replace('_', ' ').title()}: {mejora}")
                
        except Exception as e:
            print(f"❌ Error en optimización de políticas: {e}")

    def _monitorear_con_ia(self, interfaz):
        """Monitoreo de red con IA"""
        print(f"👁️  Monitoreando {interfaz} con IA...")
        try:
            resultado = guardian_ai.monitor_with_ai(interfaz)
            
            print(f"📊 Métricas de rendimiento:")
            metricas = resultado['performance_metrics']
            print(f"  - Latencia: {metricas['latency_ms']} ms")
            print(f"  - Throughput: {metricas['throughput_mbps']} Mbps")
            print(f"  - Pérdida de paquetes: {metricas['packet_loss_percent']}%")
            print(f"  - Jitter: {metricas['jitter_ms']} ms")
            
            print(f"\n🧠 Análisis de comportamiento:")
            comportamiento = resultado['behavioral_analysis']
            for aspecto, cantidad in comportamiento.items():
                if cantidad > 0:
                    print(f"  - {aspecto.replace('_', ' ').title()}: {cantidad}")
            
            if resultado['threat_correlation']:
                print(f"\n🔗 Correlaciones de amenazas:")
                for corr in resultado['threat_correlation']:
                    print(f"    • ID: {corr['correlation_id']}")
                    print(f"      Tipo: {corr['threat_type']} (Confianza: {corr['confidence']:.1%})")
                    print(f"      Eventos relacionados: {corr['related_events']}")
            
            if resultado['ai_insights']:
                print(f"\n🧠 Insights de IA:")
                for insight in resultado['ai_insights']:
                    print(f"    • {insight}")
                    
        except Exception as e:
            print(f"❌ Error en monitoreo con IA: {e}")

    def _alertar_con_contexto_inteligente(self, tipo_amenaza):
        """Alerta con contexto inteligente"""
        print(f"🚨 Generando alerta inteligente para: {tipo_amenaza}")
        try:
            resultado = guardian_ai.alert_with_intelligent_context(tipo_amenaza)
            
            print(f"🆔 ID de Alerta: {resultado['alert_id']}")
            print(f"⚠️  Severidad: {resultado['severity'].upper()}")
            print(f"🕒 Timestamp: {resultado['timestamp']}")
            
            contexto = resultado['context']
            print(f"\n📋 Contexto de la amenaza:")
            print(f"  - Descripción: {contexto['description']}")
            if 'common_vectors' in contexto:
                print(f"  - Vectores comunes: {', '.join(contexto['common_vectors'])}")
            if 'typical_targets' in contexto:
                print(f"  - Objetivos típicos: {', '.join(contexto['typical_targets'])}")
            
            print(f"\n💡 Acciones recomendadas:")
            for accion in resultado['recommended_actions']:
                print(f"    • {accion}")
            
            print(f"\n📊 Impacto en el negocio:")
            impacto = resultado['business_impact']
            print(f"  - Disponibilidad: {impacto['availability']}")
            print(f"  - Confidencialidad: {impacto['confidentiality']}")
            print(f"  - Integridad: {impacto['integrity']}")
                    
        except Exception as e:
            print(f"❌ Error en alerta inteligente: {e}")

    def _generar_informe_riesgo_ia(self):
        """Generación de informe de riesgo con IA"""
        print(f"📊 Generando informe de riesgo con IA...")
        try:
            resultado = guardian_ai.generate_risk_report_with_ai()
            
            print(f"📋 ID del Informe: {resultado['report_id']}")
            print(f"📅 Fecha de generación: {resultado['generation_timestamp']}")
            
            print(f"\n📈 Evaluación de riesgo:")
            evaluacion = resultado['risk_assessment']
            print(f"  - Puntuación general: {evaluacion['overall_risk_score']}/10")
            print(f"  - Tendencia: {evaluacion['trend']}")
            
            print(f"\n🎯 Riesgo por categorías:")
            for categoria, puntuacion in evaluacion['risk_categories'].items():
                print(f"  - {categoria.replace('_', ' ').title()}: {puntuacion}/10")
            
            print(f"\n🌍 Panorama de amenazas:")
            amenazas = resultado['threat_landscape']
            print(f"  - Amenazas activas: {amenazas['active_threats']}")
            print(f"  - Amenazas emergentes: {', '.join(amenazas['trending_threats'])}")
            
            print(f"\n🛡️  Resumen de vulnerabilidades:")
            vulns = resultado['vulnerability_summary']
            print(f"  - Total: {vulns['total_vulnerabilities']}")
            print(f"  - Críticas: {vulns['by_severity']['critical']}")
            print(f"  - Altas: {vulns['by_severity']['high']}")
            
            print(f"\n💡 Recomendaciones estratégicas:")
            for rec in resultado['recommendations'][:3]:
                print(f"    • {rec['recommendation']} (Prioridad: {rec['priority']})")
                print(f"      Timeline: {rec['timeline']}")
                    
        except Exception as e:
            print(f"❌ Error en generación de informe: {e}")

    def _recomendar_acciones_mitigacion(self):
        """Recomendación de acciones de mitigación"""
        print(f"💡 Generando recomendaciones de mitigación...")
        try:
            resultado = guardian_ai.recommend_mitigation_actions()
            
            print(f"🚨 Acciones inmediatas:")
            for accion in resultado['immediate_actions']:
                print(f"    • {accion['action']} (Prioridad: {accion['priority']})")
                print(f"      Timeline: {accion['timeline']}")
                print(f"      Recursos: {', '.join(accion['resources_required'])}")
                print()
            
            print(f"📅 Acciones a corto plazo:")
            for accion in resultado['short_term_actions']:
                print(f"    • {accion['action']} (Prioridad: {accion['priority']})")
                print(f"      Timeline: {accion['timeline']}")
                print()
            
            print(f"🎯 Acciones a largo plazo:")
            for accion in resultado['long_term_actions']:
                print(f"    • {accion['action']} (Prioridad: {accion['priority']})")
                print(f"      Timeline: {accion['timeline']}")
                print()
            
            print(f"📊 Estimaciones:")
            print(f"  - Reducción de riesgo: {resultado['estimated_risk_reduction']}")
            print(f"  - Costo total estimado: {resultado['total_estimated_cost']}")
            print(f"  - Timeline de ROI: {resultado['roi_timeline']}")
                    
        except Exception as e:
            print(f"❌ Error en recomendaciones de mitigación: {e}")
            
            print(f"📈 Anomalías estándar detectadas: {len(resultado['standard_anomalies'])}")
            print(f"🤖 Anomalías detectadas por IA: {len(resultado['ai_detected_anomalies'])}")
            print(f"🎯 Evaluación de riesgo: {resultado['risk_assessment']}")
            
            if resultado['ai_detected_anomalies']:
                print(f"\n🚨 Anomalías detectadas por IA:")
                for anomalia in resultado['ai_detected_anomalies']:
                    print(f"  • {anomalia['type']}: {anomalia['description']}")
                    print(f"    Severidad: {anomalia['severity']}, Confianza: {anomalia['ai_confidence']:.2%}")
                    
        except Exception as e:
            print(f"❌ Error en detección de anomalías: {e}")

    def _evaluar_vulnerabilidades(self, rango_ip):
        """Evaluación de vulnerabilidades con IA"""
        print(f"🛡️  Evaluando vulnerabilidades en {rango_ip} con IA...")
        try:
            resultado = guardian_ai.evaluate_vulnerabilities(rango_ip)
            
            if 'error' in resultado:
                print(f"❌ {resultado['error']}")
                return
            
            print(f"📊 Resumen del escaneo:")
            print(f"  - Hosts escaneados: {resultado['hosts_scanned']}")
            print(f"  - Vulnerabilidades encontradas: {resultado['risk_summary']['total_vulnerabilities']}")
            print(f"  - Puntaje de riesgo general: {resultado['risk_summary']['overall_risk_score']}/100")
            
            print(f"\n📈 Distribución de riesgos:")
            for nivel, cantidad in resultado['risk_summary']['risk_distribution'].items():
                if cantidad > 0:
                    print(f"  - {nivel}: {cantidad}")
            
            if 'ai_analysis' in resultado and resultado['ai_analysis']['priority_vulnerabilities']:
                print(f"\n🎯 Vulnerabilidades prioritarias (IA):")
                for vuln in resultado['ai_analysis']['priority_vulnerabilities'][:3]:  # Top 3
                    print(f"  • Host {vuln['host']}:{vuln['port']} - {vuln['vulnerability_id']} (Riesgo: {vuln['risk_score']}/100)")
            
            if 'ai_analysis' in resultado and resultado['ai_analysis']['attack_vectors']:
                print(f"\n⚔️  Vectores de ataque identificados:")
                for vector in resultado['ai_analysis']['attack_vectors']:
                    print(f"  • {vector}")
            
            if 'ai_analysis' in resultado and resultado['ai_analysis']['mitigation_strategy']:
                print(f"\n🛠️  Estrategia de mitigación recomendada:")
                for estrategia in resultado['ai_analysis']['mitigation_strategy']:
                    print(f"  • {estrategia}")
                    
        except Exception as e:
            print(f"❌ Error en evaluación de vulnerabilidades: {e}")

    def _predecir_ataques(self):
        """Predicción de ataques con IA"""
        print("🔮 Prediciendo posibles ataques con IA...")
        try:
            resultado = guardian_ai.predict_attacks()
            
            print(f"⏰ Horizonte de predicción: {resultado['time_horizon'].replace('_', ' ')}")
            print(f"🎯 Nivel de confianza: {resultado['confidence_level']:.2%}")
            
            if resultado['predicted_attacks']:
                print(f"\n⚠️  Ataques predichos:")
                for ataque in resultado['predicted_attacks']:
                    print(f"  • {ataque['attack_type'].replace('_', ' ').title()}")
                    print(f"    Probabilidad: {ataque['probability']:.2%}")
                    print(f"    Tiempo estimado: {ataque['expected_time']}")
                    print(f"    Vectores objetivo: {', '.join(ataque['target_vectors'])}")
                    print()
            
            if resultado['recommendations']:
                print(f"💡 Recomendaciones preventivas:")
                for recomendacion in resultado['recommendations']:
                    print(f"  • {recomendacion}")
                    
        except Exception as e:
            print(f"❌ Error en predicción de ataques: {e}")

    def _generar_reglas_firewall_inteligentes(self, contexto):
        """Generación inteligente de reglas de firewall"""
        print(f"🧠 Generando reglas de firewall inteligentes para contexto: {contexto}")
        try:
            resultado = guardian_ai.generate_intelligent_firewall_rules(contexto)
            
            print(f"📊 Reglas generadas: {resultado['rule_count']}")
            print(f"🎯 Confianza de IA: {resultado['ai_confidence']:.2%}")
            print(f"📈 Efectividad estimada: {resultado['estimated_effectiveness']:.2%}")
            
            print(f"\n🛡️  Reglas generadas:")
            for i, regla in enumerate(resultado['generated_rules'][:5], 1):  # Mostrar primeras 5
                print(f"  {i}. {regla['description']}")
                print(f"     {regla['source_ip']} → {regla['destination_ip']}:{regla['port']} ({regla['protocol']}) - {regla['action']}")
                if 'ai_confidence' in regla:
                    print(f"     Confianza: {regla['ai_confidence']:.2%}")
                print()
            
            if resultado['rule_count'] > 5:
                print(f"  ... y {resultado['rule_count'] - 5} reglas más")
                
        except Exception as e:
            print(f"❌ Error en generación de reglas: {e}")

    def _optimizar_politicas_seguridad(self):
        """Optimización de políticas de seguridad con IA"""
        print("⚙️  Optimizando políticas de seguridad con IA...")
        try:
            resultado = guardian_ai.optimize_security_policies()
            
            print(f"📊 Políticas actuales analizadas: {resultado['current_policy_count']}")
            print(f"📈 Mejora estimada: {resultado['estimated_improvement']:.2%}")
            
            optimizacion = resultado['optimization_analysis']
            print(f"\n🔧 Análisis de optimización:")
            print(f"  - Reglas originales: {optimizacion['original_rule_count']}")
            
            if optimizacion['optimizations']:
                print(f"  - Optimizaciones encontradas:")
                for opt in optimizacion['optimizations']:
                    print(f"    • {opt['type']}: {opt['description']}")
            
            if optimizacion['recommendations']:
                print(f"  - Recomendaciones:")
                for rec in optimizacion['recommendations']:
                    print(f"    • {rec['type']}: {rec['description']}")
            
            ai_rec = resultado['ai_recommendations']
            if ai_rec['policy_gaps']:
                print(f"\n🚨 Brechas en políticas identificadas:")
                for brecha in ai_rec['policy_gaps']:
                    print(f"  • {brecha['description']} (Prioridad: {brecha['priority']})")
            
            if ai_rec['security_improvements']:
                print(f"\n🛡️  Mejoras de seguridad recomendadas:")
                for mejora in ai_rec['security_improvements']:
                    print(f"  • {mejora}")
            
            if ai_rec['performance_optimizations']:
                print(f"\n⚡ Optimizaciones de rendimiento:")
                for opt in ai_rec['performance_optimizations']:
                    print(f"  • {opt}")
                    
        except Exception as e:
            print(f"❌ Error en optimización de políticas: {e}")

    def _monitorear_con_ia(self, interfaz):
        """Monitoreo avanzado con IA"""
        print(f"👁️  Iniciando monitoreo avanzado con IA en {interfaz}...")
        try:
            # Combinar análisis de amenazas y detección de anomalías
            amenazas = guardian_ai.analyze_threats_realtime(interfaz)
            anomalias = guardian_ai.detect_network_anomalies(interfaz)
            
            print(f"🔍 Estado del monitoreo:")
            print(f"  - Interfaz: {interfaz}")
            print(f"  - Nivel de amenaza: {amenazas['ai_insights']['threat_level']}")
            print(f"  - Anomalías detectadas: {anomalias['total_anomalies']}")
            print(f"  - Evaluación de riesgo: {anomalias['risk_assessment']}")
            
            print(f"\n📊 Métricas de tráfico:")
            traffic = amenazas['traffic_analysis']
            print(f"  - Paquetes analizados: {traffic['total_packets']}")
            print(f"  - Tasa de sospecha: {(traffic['suspicious_packets']/traffic['total_packets'])*100:.2f}%")
            
            # Recomendaciones combinadas
            recomendaciones = set(amenazas['ai_insights']['recommended_actions'])
            print(f"\n💡 Recomendaciones de IA:")
            for rec in list(recomendaciones)[:3]:
                print(f"  • {rec}")
                
        except Exception as e:
            print(f"❌ Error en monitoreo con IA: {e}")

