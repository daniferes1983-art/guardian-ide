#!/usr/bin/env python3
"""
Punto de entrada principal para el IDE Guardián
"""

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)

