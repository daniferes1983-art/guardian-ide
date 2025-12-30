# 🚀 Guía de Despliegue Permanente - Guardián IDE

Esta guía proporciona instrucciones detalladas para desplegar el Guardián IDE de forma permanente en diferentes entornos.

---

## 📋 Opciones de Despliegue

### 1. **Despliegue Local Permanente** (Recomendado para desarrollo)
### 2. **Despliegue en Servidor Linux** (Recomendado para producción)
### 3. **Despliegue en Cloud** (Render, Heroku, Railway, etc.)
### 4. **Despliegue con Docker**

---

## 1️⃣ Despliegue Local Permanente

### Opción A: Usar el Script de Inicio

```bash
cd /home/ubuntu/guardian_web_ide
./start_server.sh
```

El servidor se iniciará en `http://localhost:5000` y permanecerá ejecutándose.

### Opción B: Usar Gunicorn Directamente

```bash
cd /home/ubuntu/guardian_web_ide
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
```

### Opción C: Usar nohup para Desconexión

```bash
cd /home/ubuntu/guardian_web_ide
nohup ./start_server.sh > logs/server.log 2>&1 &
```

El servidor continuará ejecutándose incluso si cierras la terminal.

---

## 2️⃣ Despliegue en Servidor Linux (Producción)

### Requisitos Previos

- Servidor Linux (Ubuntu 20.04+)
- Python 3.11+
- Acceso SSH
- Dominio (opcional)

### Paso 1: Preparar el Servidor

```bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependencias
sudo apt-get install -y python3.11 python3.11-venv python3-pip nginx supervisor

# Crear usuario para la aplicación
sudo useradd -m -s /bin/bash guardian
```

### Paso 2: Clonar el Repositorio

```bash
sudo -u guardian git clone <tu-repositorio> /opt/guardian-ide
cd /opt/guardian-ide
```

### Paso 3: Crear Entorno Virtual

```bash
sudo -u guardian python3.11 -m venv venv
sudo -u guardian source venv/bin/activate
sudo -u guardian pip install -r requirements.txt
```

### Paso 4: Configurar Supervisor

Crear archivo `/etc/supervisor/conf.d/guardian-ide.conf`:

```ini
[program:guardian-ide]
directory=/opt/guardian-ide
command=/opt/guardian-ide/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 --timeout 120 wsgi:app
user=guardian
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/guardian-ide/gunicorn.log
environment=FLASK_ENV=production
```

Crear directorio de logs:

```bash
sudo mkdir -p /var/log/guardian-ide
sudo chown guardian:guardian /var/log/guardian-ide
```

Iniciar Supervisor:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start guardian-ide
```

### Paso 5: Configurar Nginx como Reverse Proxy

Crear archivo `/etc/nginx/sites-available/guardian-ide`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Redirigir HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Configuración SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Tamaño máximo de carga
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Caché de archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Habilitar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/guardian-ide /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 6: Configurar SSL con Let's Encrypt

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### Paso 7: Verificar Despliegue

```bash
# Verificar estado de Supervisor
sudo supervisorctl status guardian-ide

# Ver logs
sudo tail -f /var/log/guardian-ide/gunicorn.log

# Probar aplicación
curl https://tu-dominio.com/api/health
```

---

## 3️⃣ Despliegue en Plataformas Cloud

### Render.com

1. Ir a [render.com](https://render.com)
2. Crear cuenta y conectar GitHub
3. Crear nuevo "Web Service"
4. Configurar:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:app`
5. Agregar variables de entorno:
   - `FLASK_ENV=production`
   - `SECRET_KEY=tu-clave-secreta`
6. Desplegar

**URL:** `https://guardian-ide.onrender.com`

### Heroku

```bash
# Instalar Heroku CLI
brew tap heroku/brew && brew install heroku

# Autenticarse
heroku login

# Crear aplicación
heroku create guardian-ide

# Configurar variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=tu-clave-secreta

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

**URL:** `https://guardian-ide.herokuapp.com`

### Railway

1. Ir a [railway.app](https://railway.app)
2. Conectar GitHub
3. Seleccionar repositorio
4. Railway detectará automáticamente Python
5. Agregar variables de entorno
6. Desplegar automáticamente

**URL:** `https://guardian-ide-production.up.railway.app`

---

## 4️⃣ Despliegue con Docker

### Construir Imagen

```bash
cd /home/ubuntu/guardian_web_ide
docker build -t guardian-ide:latest .
```

### Ejecutar Contenedor

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=tu-clave-secreta \
  -v guardian-data:/app/data \
  --name guardian-ide \
  --restart unless-stopped \
  guardian-ide:latest
```

### Con Docker Compose

```bash
cp .env.example .env
# Editar .env con valores de producción

docker-compose up -d
```

---

## 🔐 Consideraciones de Seguridad

### 1. Cambiar SECRET_KEY

Generar clave segura:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Configurar en variables de entorno:

```bash
export SECRET_KEY="tu-clave-generada"
```

### 2. Configurar CORS

En `config.py`, ajustar `CORS_ORIGINS`:

```python
CORS_ORIGINS = ["https://tu-dominio.com", "https://www.tu-dominio.com"]
```

### 3. Usar HTTPS

- Usar Let's Encrypt para certificados gratuitos
- Configurar redirección HTTP → HTTPS
- Habilitar HSTS

### 4. Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 5. Backups

```bash
# Backup de base de datos
cp guardian_ide.db guardian_ide.db.backup

# Backup completo
tar -czf guardian-ide-backup.tar.gz /opt/guardian-ide
```

---

## 📊 Monitoreo

### Ver Logs

```bash
# Supervisor
sudo supervisorctl tail -f guardian-ide

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Systemd
sudo journalctl -u guardian-ide -f
```

### Monitorear Recursos

```bash
# CPU y memoria
htop

# Espacio en disco
df -h

# Procesos
ps aux | grep gunicorn
```

### Health Check

```bash
curl https://tu-dominio.com/api/health
```

---

## 🔄 Actualizar Despliegue

### Con Git

```bash
cd /opt/guardian-ide
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart guardian-ide
```

### Con Docker

```bash
docker pull guardian-ide:latest
docker stop guardian-ide
docker rm guardian-ide
docker run -d ... guardian-ide:latest
```

---

## 🆘 Solución de Problemas

### Aplicación no inicia

```bash
# Ver logs
sudo supervisorctl tail -f guardian-ide

# Verificar sintaxis Python
python3 -m py_compile wsgi.py

# Verificar dependencias
source venv/bin/activate
pip install -r requirements.txt
```

### Error 502 Bad Gateway

- Verificar que Gunicorn está ejecutándose
- Verificar logs de Nginx
- Reiniciar aplicación: `sudo supervisorctl restart guardian-ide`

### Errores de base de datos

- Verificar permisos de archivo
- Verificar espacio en disco
- Hacer backup y recrear base de datos

### Problemas de SSL

```bash
# Renovar certificado
sudo certbot renew

# Verificar certificado
sudo certbot certificates
```

---

## ✅ Checklist de Despliegue

- [ ] Código actualizado en repositorio
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generada y configurada
- [ ] Base de datos inicializada
- [ ] CORS configurado correctamente
- [ ] SSL/HTTPS habilitado
- [ ] Firewall configurado
- [ ] Backups configurados
- [ ] Monitoreo habilitado
- [ ] Health check funcionando
- [ ] Logs accesibles
- [ ] Dominio apuntando a servidor

---

## 📈 Recomendaciones de Producción

### Rendimiento

- Usar CDN para archivos estáticos
- Habilitar compresión gzip
- Implementar caching
- Usar base de datos PostgreSQL en lugar de SQLite

### Seguridad

- Mantener dependencias actualizadas
- Usar firewall WAF
- Implementar rate limiting
- Monitorear accesos sospechosos

### Mantenimiento

- Realizar backups diarios
- Revisar logs regularmente
- Actualizar sistema operativo
- Monitorear uso de recursos

---

## 🎯 Próximos Pasos

1. Elegir método de despliegue (recomendado: Servidor Linux + Nginx)
2. Seguir instrucciones paso a paso
3. Verificar que todo funciona
4. Configurar monitoreo y backups
5. Compartir URL con usuarios

---

**Guardián IDE v1.0.0** - Listo para Producción
