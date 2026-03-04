# Docker Setup Guide

This project is fully Docker-ready and can be run using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- At least 2GB of free disk space

## Getting Started

### 1. Build and Start Services

From the project root directory:

```bash
docker compose up --build
```

This command will:
- Build the backend (Django) image
- Build the frontend (Vite/React) image
- Pull the Nginx image
- Start all services (web, client, nginx)
- Run Django migrations automatically
- Collect static files automatically

### 2. Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Backend via Nginx proxy**: http://localhost (port 80)

### 3. View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web      # Django app
docker compose logs -f client   # Frontend
docker compose logs -f nginx    # Reverse proxy
```

### 4. Stop Services

```bash
docker compose down
```

To also remove volumes (data):
```bash
docker compose down -v
```

## Architecture

### Services

1. **web**: Django application running on port 8000
   - Handles API requests
   - Runs migrations on startup
   - Collects static files on startup
   - Healthcheck: Every 5 seconds, checks if port 8000 responds

2. **client**: React/Vite frontend built and served via Nginx
   - Compiled frontend assets
   - Runs on port 3000

3. **nginx**: Reverse proxy server
   - Serves frontend from port 3000
   - Proxies backend requests to Django app on port 8000
   - Serves static files from Django
   - Runs on port 80
   - Waits for Django healthcheck before starting

### Volumes

- `./Application/_server:/app` - Live code mounting (for development)
- `./Application/_server/static:/static` - Shared static files volume

## Configuration

### Django Settings (`Application/_server/_server/settings.py`)

- `DEBUG = True` - Development mode (change for production)
- `ALLOWED_HOSTS = ["*"]` - Allow all hosts (restrict for production)
- `STATIC_ROOT = BASE_DIR / 'static'` - Static files location
- `DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'` - SQLite database

### Environment Variables (`.env`)

Located at `Application/_server/.env`:

```
ASSET_URL=http://localhost:5173
```

See `.env.example` for all available options.

## Troubleshooting

### Services fail to start

1. Check logs: `docker compose logs`
2. Ensure ports 80, 3000, 8000 are not in use
3. Try rebuilding: `docker compose up --build`

### Database migration errors

If you see migration errors:
1. The migrations should run automatically
2. If they fail, check the backend logs
3. Ensure no database lock issues exist

### Static files not served

1. Verify the static volume is mounted: `docker compose ps`
2. Check static files were collected: `docker exec fullstack_web ls -la /app/static/`
3. Verify nginx config: `docker exec fullstack_nginx cat /etc/nginx/nginx.conf`

### Frontend not loading

1. Ensure the client service built successfully: `docker compose logs client`
2. Check the asset proxy URL in `.env` matches your setup
3. Verify port 3000 is accessible

## Development Workflow

### Modifying Backend Code

Changes to `/Application/_server` are live-mounted:
1. Edit Python files
2. Django will auto-reload for development
3. Changes appear in running container

### Modifying Frontend Code

Frontend changes require rebuild:
1. Edit React/Vite files in `/Application/client`
2. Rebuild the client service: `docker compose up --build client`
3. Access new version at http://localhost:3000

### Running Django Commands

```bash
docker compose exec web python manage.py [command]

# Examples
docker compose exec web python manage.py shell
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Production Considerations

Before deploying to production:

1. ✅ Set `DEBUG = False` in settings.py
2. ✅ Change `ALLOWED_HOSTS` to your domain
3. ✅ Use a strong `SECRET_KEY`
4. ✅ Set up proper static file serving (CloudFront, S3, etc.)
5. ✅ Use environment variables for sensitive data
6. ✅ Configure database with proper backups
7. ✅ Set up logging and monitoring
8. ✅ Use a production-grade WSGI server (gunicorn is configured)

## File Structure

```
.
├── docker-compose.yml
├── .dockerignore
├── README_DOCKER.md (this file)
│
├── Application/
│   ├── _server/
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   ├── nginx.conf
│   │   ├── requirements.txt
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── .dockerignore
│   │   ├── manage.py
│   │   ├── db.sqlite3
│   │   ├── static/
│   │   └── ... (Django app files)
│   │
│   └── client/
│       ├── Dockerfile
│       ├── .dockerignore
│       ├── package.json
│       ├── package-lock.json
│       ├── vite.config.js
│       └── ... (React app files)
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
