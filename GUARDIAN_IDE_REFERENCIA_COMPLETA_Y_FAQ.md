# 📚 Guía de Referencia Completa y FAQ - Guardián IDE

Esta guía proporciona una referencia completa de todos los comandos y funcionalidades del Guardián IDE, así como respuestas a las preguntas más frecuentes.

## Referencia de Comandos

### Comandos Básicos

| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `analizar puertos de <IP>` | Escanea los puertos de una dirección IP. | `analizar puertos de 192.168.1.1` |
| `crear regla firewall puerto: <PUERTO> protocolo: <TCP/UDP> accion: <bloquear/permitir>` | Crea una regla de firewall. | `crear regla firewall puerto: 22 protocolo: TCP accion: bloquear` |
| `leer logs de <RUTA>` | Lee un archivo de log. | `leer logs de /var/log/syslog` |
| `monitorear trafico en <INTERFAZ>` | Monitorea el tráfico de red. | `monitorear trafico en eth0` |
| `alertar "<MENSAJE>"` | Envía una alerta de seguridad. | `alertar "Intrusión detectada"` |
| `ver procesos activos` | Muestra los procesos activos. | `ver procesos activos` |

### Comandos de IA

| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `analizar amenazas en tiempo real en <INTERFAZ>` | Analiza amenazas en tiempo real con IA. | `analizar amenazas en tiempo real en eth0` |
| `detectar anomalias en trafico de <INTERFAZ>` | Detecta anomalías en el tráfico de red. | `detectar anomalias en trafico de eth0` |
| `evaluar vulnerabilidades de <RANGO_IP>` | Evalúa vulnerabilidades en un rango de IPs. | `evaluar vulnerabilidades de 192.168.1.0/24` |
| `predecir ataques [basado en patrones historicos]` | Predice posibles ataques. | `predecir ataques basado en patrones historicos` |
| `generar reglas firewall inteligentes para <CONTEXTO>` | Genera reglas de firewall con IA. | `generar reglas firewall inteligentes para web_server` |
| `optimizar politicas de seguridad [automaticamente]` | Optimiza las políticas de seguridad. | `optimizar politicas de seguridad automaticamente` |
| `monitorear con ia la red <INTERFAZ>` | Monitorea la red con IA. | `monitorear con ia la red eth0` |
| `alertar con contexto inteligente sobre <TIPO_AMENAZA>` | Genera alertas con contexto de IA. | `alertar con contexto inteligente sobre malware` |
| `generar informe de riesgo con ia` | Genera un informe de riesgo con IA. | `generar informe de riesgo con ia` |
| `recomendar acciones de mitigacion` | Recomienda acciones de mitigación. | `recomendar acciones de mitigacion` |

## Preguntas Frecuentes (FAQ)

**P: ¿Necesito instalar algo para usar Guardián IDE?**

R: No, el IDE es completamente basado en web. Solo necesitas un navegador moderno.

**P: ¿Es seguro usar Guardián IDE?**

R: Sí, todas las conexiones son seguras (HTTPS) y el análisis se realiza en un entorno aislado. No se almacenan tus datos personales.

**P: ¿Puedo usar Guardián IDE en mi smartphone?**

R: Sí, la interfaz es completamente responsive y funciona en cualquier dispositivo.

**P: ¿Qué es el Dashboard de IA?**

R: Es un panel de monitoreo en tiempo real que usa inteligencia artificial para analizar la seguridad de tu red, detectar amenazas y ofrecerte recomendaciones.

**P: ¿Cómo funcionan los bots?**

R: Los bots son programas automatizados que realizan tareas de seguridad por ti. Puedes crearlos usando plantillas o de forma personalizada con la ayuda de un asistente de IA.

**P: ¿El lenguaje Guardián es difícil de aprender?**

R: No, Guardián está diseñado para ser un lenguaje pseudonatural, con una sintaxis muy intuitiva y fácil de entender. Además, el IDE te ayuda con autocompletado y validación en tiempo real.

**P: ¿Puedo conectar Guardián IDE a mis propias herramientas?**

R: Sí, el IDE expone una API REST que puedes usar para integrar con otros sistemas. Próximamente se agregará documentación completa de la API.

**P: ¿Dónde se guardan mis proyectos y bots?**

R: Actualmente, los proyectos y bots se guardan en una base de datos local en el servidor del IDE. Próximamente se agregará la funcionalidad para exportarlos y guardarlos localmente.

**P: ¿Cómo puedo reportar un error o sugerir una mejora?**

R: Puedes contactar al equipo de desarrollo a través de la plataforma Manus o, si tienes acceso, crear un "Issue" en el repositorio de GitHub.
