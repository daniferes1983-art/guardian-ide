# 🚀 Guía de Despliegue - Guardián IDE

Esta guía proporciona instrucciones paso a paso para desplegar Guardián IDE en diferentes plataformas de hosting.

## 📋 Tabla de Contenidos

1. [Despliegue en Render.com](#despliegue-en-rendercom)
2. [Despliegue en Heroku](#despliegue-en-heroku)
3. [Despliegue en Railway](#despliegue-en-railway)
4. [Despliegue en DigitalOcean](#despliegue-en-digitalocean)
5. [Despliegue con Docker](#despliegue-con-docker)

---

## Despliegue en Render.com

Render.com es una plataforma moderna que ofrece despliegue gratuito para aplicaciones Python.

### Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Repositorio Git (GitHub, GitLab o Bitbucket)

### Pasos

1. **Conectar repositorio**
   - Ir a [dashboard.render.com](https://dashboard.render.com)
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio Git
   - Seleccionar el repositorio de Guardián IDE

2. **Configurar servicio**
   - **Name:** `guardian-ide`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 wsgi:app`

3. **Variables de entorno**
   - Click en "Environment"
   - Agregar variables:
     ```
     FLASK_ENV=production
     SECRET_KEY=your-secret-key-here
     ```

4. **Desplegar**
   - Click en "Create Web Service"
   - Esperar a que se complete el despliegue
   - Tu aplicación estará disponible en `https://guardian-ide.onrender.com`

### Actualizar Despliegue

Render.com se actualiza automáticamente cuando haces push a tu rama principal:

```bash
git add .
git commit -m "Cambios para despliegue"
git push origin main
```

---

## Despliegue en Heroku

Heroku es una plataforma clásica para desplegar aplicaciones Python.

### Requisitos Previos

- Cuenta en [Heroku](https://www.heroku.com)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Git configurado

### Pasos

1. **Instalar Heroku CLI**
   ```bash
   # En macOS
   brew tap heroku/brew && brew install heroku
   
   # En Ubuntu/Debian
   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
   
   # En Windows
   # Descargar desde https://cli-assets.heroku.com/heroku-x64.exe
   ```

2. **Autenticarse en Heroku**
   ```bash
   heroku login
   ```

3. **Crear aplicación Heroku**
   ```bash
   cd /path/to/guardian_web_ide
   heroku create guardian-ide
   ```

4. **Configurar variables de entorno**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

5. **Desplegar**
   ```bash
   git push heroku main
   ```

6. **Verificar despliegue**
   ```bash
   heroku open
   heroku logs --tail
   ```

### Actualizar Despliegue

```bash
git add .
git commit -m "Cambios para despliegue"
git push heroku main
```

---

## Despliegue en Railway

Railway es una plataforma moderna y simple para desplegar aplicaciones.

### Requisitos Previos

- Cuenta en [Railway.app](https://railway.app)
- GitHub conectado

### Pasos

1. **Conectar repositorio**
   - Ir a [railway.app](https://railway.app)
   - Click en "New Project"
   - Seleccionar "Deploy from GitHub"
   - Autorizar y seleccionar repositorio

2. **Configurar variables de entorno**
   - En el dashboard, ir a "Variables"
   - Agregar:
     ```
     FLASK_ENV=production
     SECRET_KEY=your-secret-key-here
     PORT=8000
     ```

3. **Desplegar**
   - Railway detectará automáticamente que es una aplicación Python
   - Usará `requirements.txt` para instalar dependencias
   - Ejecutará con Procfile

4. **Obtener URL**
   - La URL estará disponible en el dashboard
   - Algo como: `https://guardian-ide-production.up.railway.app`

---

## Despliegue en DigitalOcean

DigitalOcean ofrece máquinas virtuales (Droplets) y App Platform.

### Opción 1: DigitalOcean App Platform (Recomendado)

1. **Conectar repositorio**
   - Ir a [cloud.digitalocean.com](https://cloud.digitalocean.com)
   - Click en "Apps" → "Create App"
   - Conectar GitHub

2. **Configurar**
   - Seleccionar repositorio
   - Configurar build y start commands
   - Agregar variables de entorno

3. **Desplegar**
   - Click en "Deploy"

### Opción 2: DigitalOcean Droplet + Docker

1. **Crear Droplet**
   ```bash
   # Crear droplet con Docker
   # Usar imagen "Docker on Ubuntu 22.04"
   ```

2. **SSH en el Droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Clonar repositorio**
   ```bash
   git clone <your-repo-url>
   cd guardian_web_ide
   ```

4. **Crear archivo .env**
   ```bash
   cp .env.example .env
   # Editar .env con valores de producción
   ```

5. **Ejecutar con Docker Compose**
   ```bash
   docker-compose up -d
   ```

6. **Configurar Nginx como reverse proxy**
   ```bash
   sudo apt-get update
   sudo apt-get install nginx
   ```

   Crear `/etc/nginx/sites-available/guardian-ide`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Habilitar sitio:
   ```bash
   sudo ln -s /etc/nginx/sites-available/guardian-ide /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. **SSL con Let's Encrypt**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## Despliegue con Docker

### Despliegue Local con Docker

```bash
# Construir imagen
docker build -t guardian-ide:latest .

# Ejecutar contenedor
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -v guardian-data:/app/data \
  --name guardian-ide \
  guardian-ide:latest

# Verificar
curl http://localhost:5000/api/health
```

### Despliegue con Docker Compose

```bash
# Crear archivo .env
cp .env.example .env

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

---

## Verificación Post-Despliegue

Después de desplegar, verifica que todo funciona correctamente:

```bash
# Health check
curl https://your-deployed-url/api/health

# Obtener comandos disponibles
curl https://your-deployed-url/api/commands

# Obtener plantillas de bots
curl https://your-deployed-url/api/bots/templates

# Probar ejecución de comando
curl -X POST https://your-deployed-url/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "analizar puertos de 192.168.1.1"}'
```

---

## Solución de Problemas

### Aplicación no inicia

1. Verificar logs:
   ```bash
   # Render
   # Ver en dashboard
   
   # Heroku
   heroku logs --tail
   
   # Docker
   docker logs guardian-ide
   ```

2. Verificar variables de entorno
3. Verificar que `requirements.txt` está actualizado
4. Verificar que `wsgi.py` existe y es correcto

### Error 502 Bad Gateway

- Aplicación no está respondiendo
- Verificar que el puerto es correcto
- Verificar que la aplicación inicia sin errores

### Base de datos no persiste

- Usar volúmenes de Docker
- O usar base de datos en la nube (PostgreSQL, MongoDB)

### Errores de importación

- Verificar que todas las dependencias están en `requirements.txt`
- Reinstalar dependencias: `pip install -r requirements.txt`

---

## Monitoreo y Mantenimiento

### Logs

```bash
# Heroku
heroku logs --tail

# Render
# Ver en dashboard

# Docker
docker logs -f guardian-ide
```

### Actualizaciones

```bash
# Hacer cambios localmente
git add .
git commit -m "Descripción de cambios"

# Push a repositorio
git push origin main

# Plataforma se actualiza automáticamente
```

### Backups

Para aplicaciones con datos persistentes:

```bash
# Backup de base de datos
cp guardian_ide.db guardian_ide.db.backup

# Restaurar
cp guardian_ide.db.backup guardian_ide.db
```

---

## Recomendaciones de Producción

1. **Seguridad**
   - Cambiar `SECRET_KEY` a un valor fuerte
   - Usar HTTPS (certificado SSL)
   - Configurar CORS apropiadamente
   - Usar variables de entorno para datos sensibles

2. **Rendimiento**
   - Aumentar número de workers de Gunicorn
   - Usar CDN para archivos estáticos
   - Implementar caching

3. **Monitoreo**
   - Configurar alertas
   - Monitorear uso de recursos
   - Revisar logs regularmente

4. **Base de Datos**
   - Considerar migrar a PostgreSQL para producción
   - Implementar backups automáticos
   - Monitorear tamaño de base de datos

---

## Soporte

Para problemas de despliegue, consultar:

- [Documentación de Render](https://render.com/docs)
- [Documentación de Heroku](https://devcenter.heroku.com)
- [Documentación de Railway](https://docs.railway.app)
- [Documentación de DigitalOcean](https://docs.digitalocean.com)
- [Documentación de Docker](https://docs.docker.com)

---

**Guardián IDE v1.0.0** - Despliegue simplificado
