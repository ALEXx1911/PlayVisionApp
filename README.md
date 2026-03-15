# PlayVisionApp⚽​

A full-stack web application for querying and visualizing football data and statistics. PlayVision allows users to access information about teams, players, matches, and tournaments, displaying relevant data in a clear and detailed manner.

Built with Angular (frontend), Django (backend), Postgres (database), and Nginx as web server/proxy. Includes Docker Compose deployment and local development environment.

## Architecture
- Frontend: Angular 20, built in [PlayVisionV1/frontend](PlayVisionV1/frontend).
- Backend: Django in [PlayVisionV1/backend](PlayVisionV1/backend), main app in [PlayVisionV1/backend/apps/playvisionapi](PlayVisionV1/backend/apps/playvisionapi).
- Database: Postgres 15.
- Nginx: serves `dist/frontend` and proxies to backend; config in [PlayVisionV1/nginx/nginx.conf](PlayVisionV1/nginx/nginx.conf).
- Orchestration: [PlayVisionV1/docker-compose.yml](PlayVisionV1/docker-compose.yml).

## Requirements
- Docker and Docker Compose.
- Node.js 18+ and npm (for frontend build).
- Python 3.11+ (for local backend development outside Docker).

## Environment Variables

This project uses environment files to configure Django, Postgres, CORS and app behavior.

- Template: [PlayVisionV1/.env.example](PlayVisionV1/.env.example)
- Active file used by Docker Compose: [PlayVisionV1/.env](PlayVisionV1/.env)

### Variables used
- `SECRET_KEY`: Django secret key (must be unique per environment).
- `DEBUG`: `True` for development, `False` for production.
- `ALLOWED_HOSTS`: comma-separated hostnames/IPs.
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: database connection settings.
- `SEED_DB`: set to `true` only for initial data seed, then return to `false`.
- `CORS_ALLOWED_ORIGINS`: comma-separated frontend origins.

## Quick Start (Docker)
1) Build the frontend (required for Nginx to serve `dist`):
```bash
cd PlayVisionV1/frontend
npm install
npm run build
```
2) **First time setup - Seed the database:**  
The app doesn't display data initially. To populate the database with test data, edit [PlayVisionV1/docker-compose.yml](PlayVisionV1/docker-compose.yml) and change:
```yaml
SEED_DB: "true"
```
3) Start services:
```bash
docker compose up -d --build
```

### First-time database seed
- Edit [PlayVisionV1/.env](PlayVisionV1/.env) and set `SEED_DB=true`.
- Run deployment.
- Set `SEED_DB=false` and redeploy to avoid reseeding.

### Access
- Web: http://localhost
- Swagger UI: http://localhost/playVision/api/docs/
- OpenAPI Schema: http://localhost/playVision/api/schema/
- Logs:
```bash
docker compose logs -f nginx
docker compose logs -f backend
docker compose logs -f db
```

## Local Development

### Backend (Django)
```bash
cd PlayVisionV1/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
- API available at http://localhost:8000
- **API Documentation (local):**
  - Swagger UI: http://localhost:8000/playVision/api/docs/
  - OpenAPI Schema: http://localhost:8000/playVision/api/schema/
- Migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
- Tests:
```bash
python pytest
```

### Frontend (Angular)
```bash
cd PlayVisionV1/frontend
npm install
npm start
```
- Development at http://localhost:4200
- Production build:
```bash
npm run build
```

## Key Structure
- Compose: [PlayVisionV1/docker-compose.yml](PlayVisionV1/docker-compose.yml)
- Nginx: [PlayVisionV1/nginx/nginx.conf](PlayVisionV1/nginx/nginx.conf)
- Frontend: [PlayVisionV1/frontend](PlayVisionV1/frontend)
- Backend: [PlayVisionV1/backend](PlayVisionV1/backend)
- Django API: [PlayVisionV1/backend/apps/playvisionapi/api](PlayVisionV1/backend/apps/playvisionapi/api)

## Deployment
- Production with Docker: build frontend and start with `docker compose up -d --build`.
- Nginx serves frontend from `./frontend/dist/frontend` and proxies to internal backend.
- Volumes:
  - `media_data` (images), mounted at `/var/www/images` in Nginx and `/app/media` in backend.
  - `postgres_data` (Postgres data).

## Troubleshooting
- 404 on Nginx: make sure you ran `npm run build` in [PlayVisionV1/frontend](PlayVisionV1/frontend).
- DB connection: verify credentials in compose and that the `db` service is healthy.
- Migrations: if backend doesn't start, apply `migrate` manually inside the container or locally.

## License
See the [LICENSE](LICENSE) file.
