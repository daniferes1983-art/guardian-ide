
class GuardianParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parse(self, text):
        self.lexer.tokenize(text)
        self.current_token = self.lexer.consume()
        return self.parse_command()

    def eat(self, token_type, expected_value=None):
        if self.current_token and self.current_token["type"] == token_type:
            if expected_value and self.current_token["value"] != expected_value:
                raise ValueError(f"Error de sintaxis: Se esperaba \'{expected_value}\' pero se encontró \'{self.current_token['value']}\'")
            token = self.current_token
            self.current_token = self.lexer.consume()
            return token
        else:
            raise ValueError(f"Error de sintaxis: Se esperaba {token_type} pero se encontró {self.current_token['type'] if self.current_token else 'EOF'}")

    def parse_command(self):
        if self.current_token is None:
            return None

        if self.current_token["type"] == "PALABRA_CLAVE":
            if self.current_token["value"] == "analizar":
                next_token = self.lexer.peek()
                if next_token and next_token["value"] == "amenazas":
                    return self.parse_analizar_amenazas_tiempo_real()
                else:
                    return self.parse_analizar_puertos()
            elif self.current_token["value"] == "crear":
                next_token = self.lexer.peek()
                if next_token and next_token["value"] == "bot":
                    return self.parse_crear_bot()
                else:
                    return self.parse_crear_regla_firewall()
            elif self.current_token["value"] == "listar":
                return self.parse_listar_plantillas()
            elif self.current_token["value"] == "mostrar":
                return self.parse_mostrar_plantilla()
            elif self.current_token["value"] == "responder":
                return self.parse_responder()
            elif self.current_token["value"] == "cancelar":
                return self.parse_cancelar_creacion_bot()
            elif self.current_token["value"] == "leer":
                return self.parse_leer_logs()
            elif self.current_token["value"] == "monitorear":
                next_token = self.lexer.peek()
                if next_token and next_token["value"] == "con":
                    return self.parse_monitorear_con_ia()
                else:
                    return self.parse_monitorear_trafico()
            elif self.current_token["value"] == "alertar":
                next_token = self.lexer.peek()
                if next_token and next_token["value"] == "con":
                    return self.parse_alertar_con_contexto_inteligente()
                else:
                    return self.parse_alertar()
            elif self.current_token["value"] == "ver":
                return self.parse_ver_procesos()
            elif self.current_token["value"] == "detectar":
                return self.parse_detectar_anomalias()
            elif self.current_token["value"] == "evaluar":
                return self.parse_evaluar_vulnerabilidades()
            elif self.current_token["value"] == "predecir":
                return self.parse_predecir_ataques()
            elif self.current_token["value"] == "generar":
                next_token = self.lexer.peek()
                if next_token and next_token["value"] == "reglas":
                    return self.parse_generar_reglas_firewall_inteligentes()
                elif next_token and next_token["value"] == "informe":
                    return self.parse_generar_informe_riesgo_ia()
                else:
                    raise ValueError(f"Comando 'generar' incompleto")
            elif self.current_token["value"] == "optimizar":
                return self.parse_optimizar_politicas_seguridad()
            elif self.current_token["value"] == "recomendar":
                return self.parse_recomendar_acciones_mitigacion()
            else:
                raise ValueError(f"Comando desconocido: {self.current_token['value']}")
        else:
            raise ValueError(f"Error de sintaxis: Se esperaba una palabra clave de comando pero se encontró {self.current_token['type']}")

    def parse_analizar_puertos(self):
        self.eat("PALABRA_CLAVE", "analizar")
        self.eat("PALABRA_CLAVE", "puertos")
        self.eat("PALABRA_CLAVE", "de")
        ip_token = self.eat("IP")
        return {"command": "analizar_puertos", "ip": ip_token["value"]}

    def parse_crear_regla_firewall(self):
        self.eat("PALABRA_CLAVE", "crear")
        self.eat("PALABRA_CLAVE", "regla")
        self.eat("PALABRA_CLAVE", "firewall")
        self.eat("PALABRA_CLAVE", "puerto")
        self.eat("ASIGNACION", ":")
        puerto_token = self.eat("NUMERO")
        self.eat("PALABRA_CLAVE", "protocolo")
        self.eat("ASIGNACION", ":")
        protocolo_token = self.eat("PALABRA_CLAVE")
        if protocolo_token["value"] not in ["TCP", "UDP"]:
            raise ValueError(f"Protocolo inválido: {protocolo_token['value']}. Se esperaba TCP o UDP.")
        self.eat("PALABRA_CLAVE", "accion")
        self.eat("ASIGNACION", ":")
        accion_token = self.eat("PALABRA_CLAVE")
        if accion_token["value"] not in ["bloquear", "permitir"]:
            raise ValueError(f"Acción inválida: {accion_token['value']}. Se esperaba bloquear o permitir.")
        return {"command": "crear_regla_firewall", 
                "puerto": int(puerto_token["value"]), 
                "protocolo": protocolo_token["value"], 
                "accion": accion_token["value"]}

    def parse_leer_logs(self):
        self.eat("PALABRA_CLAVE", "leer")
        self.eat("PALABRA_CLAVE", "logs")
        self.eat("PALABRA_CLAVE", "de")
        ruta_token = self.eat("RUTA_ARCHIVO")
        return {"command": "leer_logs", "ruta_archivo": ruta_token["value"]}

    def parse_monitorear_trafico(self):
        self.eat("PALABRA_CLAVE", "monitorear")
        self.eat("PALABRA_CLAVE", "trafico")
        self.eat("PALABRA_CLAVE", "en")
        interfaz_token = self.eat("CADENA_SIMPLE")
        return {"command": "monitorear_trafico", "interfaz": interfaz_token["value"]}

    def parse_alertar(self):
        self.eat("PALABRA_CLAVE", "alertar")
        mensaje_token = self.eat("CADENA_CON_ESPACIOS") if self.current_token and self.current_token["type"] == "CADENA_CON_ESPACIOS" else self.eat("CADENA_SIMPLE")
        return {"command": "alertar", "mensaje": mensaje_token["value"]}

    def parse_ver_procesos(self):
        self.eat("PALABRA_CLAVE", "ver")
        self.eat("PALABRA_CLAVE", "procesos")
        self.eat("PALABRA_CLAVE", "activos")
        return {"command": "ver_procesos"}

    def parse_analizar_amenazas_tiempo_real(self):
        self.eat("PALABRA_CLAVE", "analizar")
        self.eat("PALABRA_CLAVE", "amenazas")
        self.eat("PALABRA_CLAVE", "en")
        self.eat("PALABRA_CLAVE", "tiempo")
        self.eat("PALABRA_CLAVE", "real")
        
        # Interfaz opcional
        interfaz = "eth0"  # valor por defecto
        if self.current_token and self.current_token["value"] == "en":
            self.eat("PALABRA_CLAVE", "en")
            interfaz_token = self.eat("CADENA_SIMPLE")
            interfaz = interfaz_token["value"]
        
        return {"command": "analizar_amenazas_tiempo_real", "interfaz": interfaz}

    def parse_detectar_anomalias(self):
        self.eat("PALABRA_CLAVE", "detectar")
        self.eat("PALABRA_CLAVE", "anomalias")
        self.eat("PALABRA_CLAVE", "en")
        self.eat("PALABRA_CLAVE", "trafico")
        self.eat("PALABRA_CLAVE", "de")
        interfaz_token = self.eat("CADENA_SIMPLE")
        return {"command": "detectar_anomalias", "interfaz": interfaz_token["value"]}

    def parse_evaluar_vulnerabilidades(self):
        self.eat("PALABRA_CLAVE", "evaluar")
        self.eat("PALABRA_CLAVE", "vulnerabilidades")
        self.eat("PALABRA_CLAVE", "de")
        # Aceptar tanto IP como CADENA_SIMPLE para rangos de IP
        if self.current_token and self.current_token["type"] == "IP":
            rango_token = self.eat("IP")
        else:
            rango_token = self.eat("CADENA_SIMPLE")
        return {"command": "evaluar_vulnerabilidades", "rango_ip": rango_token["value"]}

    def parse_predecir_ataques(self):
        self.eat("PALABRA_CLAVE", "predecir")
        self.eat("PALABRA_CLAVE", "ataques")
        # Opcional: "basado en patrones historicos"
        if self.current_token and self.current_token["value"] == "basado":
            self.eat("PALABRA_CLAVE", "basado")
            self.eat("PALABRA_CLAVE", "en")
            self.eat("PALABRA_CLAVE", "patrones")
            self.eat("PALABRA_CLAVE", "historicos")
        return {"command": "predecir_ataques"}

    def parse_generar_reglas_firewall_inteligentes(self):
        self.eat("PALABRA_CLAVE", "generar")
        self.eat("PALABRA_CLAVE", "reglas")
        self.eat("PALABRA_CLAVE", "firewall")
        self.eat("PALABRA_CLAVE", "inteligentes")
        self.eat("PALABRA_CLAVE", "para")
        contexto_token = self.eat("CADENA_SIMPLE")
        return {"command": "generar_reglas_firewall_inteligentes", "contexto": contexto_token["value"]}

    def parse_optimizar_politicas_seguridad(self):
        self.eat("PALABRA_CLAVE", "optimizar")
        self.eat("PALABRA_CLAVE", "politicas")
        self.eat("PALABRA_CLAVE", "de")
        self.eat("PALABRA_CLAVE", "seguridad")
        # Opcional: "automaticamente"
        if self.current_token and self.current_token["value"] == "automaticamente":
            self.eat("PALABRA_CLAVE", "automaticamente")
        return {"command": "optimizar_politicas_seguridad"}

    def parse_monitorear_con_ia(self):
        self.eat("PALABRA_CLAVE", "monitorear")
        self.eat("PALABRA_CLAVE", "con")
        self.eat("PALABRA_CLAVE", "ia")
        self.eat("PALABRA_CLAVE", "la")
        self.eat("PALABRA_CLAVE", "red")
        interfaz_token = self.eat("CADENA_SIMPLE")
        return {"command": "monitorear_con_ia", "interfaz": interfaz_token["value"]}

    def parse_alertar_con_contexto_inteligente(self):
        self.eat("PALABRA_CLAVE", "alertar")
        self.eat("PALABRA_CLAVE", "con")
        self.eat("PALABRA_CLAVE", "contexto")
        self.eat("PALABRA_CLAVE", "inteligente")
        self.eat("PALABRA_CLAVE", "sobre")
        tipo_token = self.eat("CADENA_SIMPLE")
        return {"command": "alertar_con_contexto_inteligente", "tipo_amenaza": tipo_token["value"]}

    def parse_generar_informe_riesgo_ia(self):
        self.eat("PALABRA_CLAVE", "generar")
        self.eat("PALABRA_CLAVE", "informe")
        self.eat("PALABRA_CLAVE", "de")
        self.eat("PALABRA_CLAVE", "riesgo")
        self.eat("PALABRA_CLAVE", "con")
        self.eat("PALABRA_CLAVE", "ia")
        return {"command": "generar_informe_riesgo_ia"}

    def parse_recomendar_acciones_mitigacion(self):
        self.eat("PALABRA_CLAVE", "recomendar")
        self.eat("PALABRA_CLAVE", "acciones")
        self.eat("PALABRA_CLAVE", "de")
        self.eat("PALABRA_CLAVE", "mitigacion")
        return {"command": "recomendar_acciones_mitigacion"}

# Example Usage (for testing)
if __name__ == "__main__":
    from guardian_lexer import GuardianLexer

    lexer = GuardianLexer()
    parser = GuardianParser(lexer)

    test_commands = [
        "analizar puertos de 192.168.1.1",
        "crear regla firewall puerto: 22 protocolo: TCP accion: bloquear",
        "leer logs de /var/log/syslog",
        "monitorear trafico en eth0",
        "alertar Intrusión detectada!",
        "ver procesos activos",
        "alertar \"Mensaje con espacios\"",
        "crear regla firewall puerto: 80 protocolo: UDP accion: permitir"
    ]

    for cmd in test_commands:
        print(f"\nComando: {cmd}")
        try:
            ast = parser.parse(cmd)
            print(f"AST: {ast}")
        except ValueError as e:
            print(f"Error de parser: {e}")

    print("\n--- Pruebas de errores ---")
    error_commands = [
        "analizar puertos 192.168.1.1", # Missing 'de'
        "crear regla firewall puerto: abc protocolo: TCP accion: bloquear", # Invalid port
        "crear regla firewall puerto: 22 protocolo: FTP accion: bloquear", # Invalid protocol
        "alertar", # Missing message
        "comando_inexistente"
    ]

    for cmd in error_commands:
        print(f"\nComando (error): {cmd}")
        try:
            ast = parser.parse(cmd)
            print(f"AST: {ast}")
        except ValueError as e:
            print(f"Error de parser: {e}")



    def parse_crear_bot(self):
        self.eat("PALABRA_CLAVE", "crear")
        self.eat("BOT", "bot")
        template_name = None
        if self.current_token and (self.current_token["type"] == "CADENA_SIMPLE" or self.current_token["type"] == "CADENA_CON_ESPACIOS"):
            template_name = self.eat(self.current_token["type"])["value"]
        return {"command": "crear_bot", "template_name": template_name}

    def parse_listar_plantillas(self):
        self.eat("PALABRA_CLAVE", "listar")
        self.eat("PALABRA_CLAVE", "plantillas")
        return {"command": "listar_plantillas"}

    def parse_mostrar_plantilla(self):
        self.eat("PALABRA_CLAVE", "mostrar")
        self.eat("PALABRA_CLAVE", "plantilla")
        template_name = self.eat("CADENA_SIMPLE")["value"]
        return {"command": "mostrar_plantilla", "template_name": template_name}

    def parse_responder(self):
        self.eat("PALABRA_CLAVE", "responder")
        response_value = self.current_token["value"]
        self.eat(self.current_token["type"])
        return {"command": "responder", "response": response_value}

    def parse_cancelar_creacion_bot(self):
        self.eat("PALABRA_CLAVE", "cancelar")
        self.eat("PALABRA_CLAVE", "creacion")
        self.eat("BOT", "bot")
        return {"command": "cancelar_creacion_bot"}


