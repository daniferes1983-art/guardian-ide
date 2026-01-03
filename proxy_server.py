#!/usr/bin/env python3
"""
Servidor Proxy que sirve archivos estáticos y redirige las llamadas a la API
al servidor Flask en el puerto 5000
"""

import os
import sys
import json
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, urljoin
import threading

# Puerto para el servidor proxy
PROXY_PORT = 8080

# URL del servidor Flask
FLASK_API_URL = 'http://localhost:5000'

# Directorio de archivos estáticos
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

class ProxyHandler(SimpleHTTPRequestHandler):
    """Manejador HTTP que sirve archivos estáticos y redirige API calls"""
    
    def do_GET(self):
        """Maneja solicitudes GET"""
        # Si es una llamada a API, redirigir al servidor Flask
        if self.path.startswith('/api/'):
            self.proxy_request('GET')
        else:
            # Servir archivos estáticos
            super().do_GET()
    
    def do_POST(self):
        """Maneja solicitudes POST"""
        if self.path.startswith('/api/'):
            self.proxy_request('POST')
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Maneja solicitudes OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def proxy_request(self, method):
        """Redirige la solicitud al servidor Flask"""
        try:
            # Construir URL completa del servidor Flask
            api_url = urljoin(FLASK_API_URL, self.path)
            
            # Leer el cuerpo de la solicitud si existe
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Hacer la solicitud al servidor Flask
            if method == 'GET':
                response = requests.get(api_url, timeout=30)
            else:  # POST
                headers = dict(self.headers)
                response = requests.post(api_url, data=body, headers=headers, timeout=30)
            
            # Enviar la respuesta al cliente
            self.send_response(response.status_code)
            
            # Copiar headers de la respuesta
            for header, value in response.headers.items():
                if header.lower() not in ['content-encoding', 'transfer-encoding']:
                    self.send_header(header, value)
            
            # Agregar headers CORS
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            
            self.end_headers()
            
            # Enviar el cuerpo de la respuesta
            self.wfile.write(response.content)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con el servidor Flask: {e}")
            self.send_error(502, f"Bad Gateway: {str(e)}")
        except Exception as e:
            print(f"Error en proxy_request: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def translate_path(self, path):
        """Traduce el path a la ruta del archivo estático"""
        # Remover query string
        if '?' in path:
            path = path.split('?')[0]
        
        # Si es raíz, servir index.html
        if path == '/':
            path = '/index.html'
        
        # Construir la ruta del archivo
        file_path = os.path.join(STATIC_DIR, path.lstrip('/'))
        
        return file_path
    
    def end_headers(self):
        """Agregar headers CORS por defecto"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def run_proxy_server():
    """Inicia el servidor proxy"""
    os.chdir(STATIC_DIR)
    
    server_address = ('', PROXY_PORT)
    httpd = HTTPServer(server_address, ProxyHandler)
    
    print(f"🌐 Servidor Proxy iniciado en puerto {PROXY_PORT}")
    print(f"📁 Sirviendo archivos estáticos desde: {STATIC_DIR}")
    print(f"🔗 Redirigiendo API calls a: {FLASK_API_URL}")
    print(f"📍 Accede a: http://localhost:{PROXY_PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔ Servidor detenido")
        httpd.server_close()

if __name__ == '__main__':
    run_proxy_server()
