import re

class GuardianLexer:
    def __init__(self):
        self.tokens = []
        self.current_pos = 0
        self.token_specs = [
            ("IP", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            ("NUMERO", r"\b\d+\b"),
            ("CADENA_CON_ESPACIOS", r"\"[^\"]*\"|\"[^\"]*\""), # Strings in double quotes
            ("RUTA_ARCHIVO", r"(?:/[a-zA-Z0-9_./-]+|[a-zA-Z]:\\(?:[a-zA-Z0-9_.-]+\\)*[a-zA-Z0-9_.-]+)"), # Linux/Windows paths
            ("PALABRA_CLAVE", r"\b(?:analizar|puertos|de|crear|regla|firewall|puerto|protocolo|accion|bloquear|permitir|leer|logs|monitorear|trafico|en|alertar|mensaje|ver|procesos|activos|TCP|UDP|amenazas|tiempo|real|detectar|anomalias|evaluar|vulnerabilidades|predecir|ataques|basado|patrones|historicos|generar|reglas|inteligentes|para|optimizar|politicas|seguridad|automaticamente|con|ia|la|red|contexto|inteligente|sobre|informe|riesgo|recomendar|acciones|mitigacion|listar|mostrar|responder|cancelar|plantillas|creacion)\b"),
            ("BOT", r"\bbot\b"),
            ("ASIGNACION", r":"),
            ("ESPACIO", r"\s+"),
            ("CADENA_SIMPLE", r"[a-zA-Z0-9_áéíóúÁÉÍÓÚüÜñÑ\s!]+"), # Single word or phrase without quotes, including accented characters, spaces, and exclamation mark
            ("UNKNOWN", r".") # Catch-all for anything not matched
        ]
        self.regex = "|".join("(?P<%s>%s)" % pair for pair in self.token_specs)

    def tokenize(self, text):
        self.tokens = []
        self.current_pos = 0
        for mo in re.finditer(self.regex, text):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == "ESPACIO":
                continue
            elif kind == "UNKNOWN":
                raise ValueError(f"Caracter inesperado: {value} en la posición {mo.start()}")
            
            # Handle quoted strings, remove quotes
            if kind == "CADENA_CON_ESPACIOS":
                value = value.strip("\"\'")
            self.tokens.append({"type": kind, "value": value})
        return self.tokens

    def peek(self):
        if self.current_pos < len(self.tokens):
            return self.tokens[self.current_pos]
        return None

    def consume(self):
        if self.current_pos < len(self.tokens):
            token = self.tokens[self.current_pos]
            self.current_pos += 1
            return token
        return None

    def reset_position(self):
        self.current_pos = 0

# Example Usage (for testing)
if __name__ == "__main__":
    lexer = GuardianLexer()
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
            tokens = lexer.tokenize(cmd)
            for token in tokens:
                print(token)
        except ValueError as e:
            print(f"Error de lexer: {e}")

    # Test with an invalid command
    print("\nComando inválido: analizar puertos de 192.168.1.1.256")
    try:
        tokens = lexer.tokenize("analizar puertos de 192.168.1.1.256")
        for token in tokens:
            print(token)
    except ValueError as e:
        print(f"Error de lexer: {e}")

    print("\nComando inválido: crear regla firewall puerto: abc")
    try:
        tokens = lexer.tokenize("crear regla firewall puerto: abc")
        for token in tokens:
            print(token)
    except ValueError as e:
        print(f"Error de lexer: {e}")




