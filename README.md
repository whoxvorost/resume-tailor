# Resume Tailor API

AI-powered resume tailoring platform backend built with FastAPI.

## Tech Stack

- Python + FastAPI
- PostgreSQL + SQLAlchemy + Alembic
- Ollama (local AI)
- JWT Authentication
- Docker + Docker Compose

## Features

- Resume upload (PDF, DOCX)
- ATS scoring against job description
- AI-powered resume generation via Ollama
- PDF export
- JWT authentication

## Getting Started

### With Docker

```bash
docker compose up --build
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
python main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login user |
| POST | /resume/upload | Upload resume |
| POST | /resume/analyze | ATS scoring |
| POST | /resume/generate | Generate resume |
| POST | /resume/export | Export PDF |
| GET | /health | Health check |

## Environment Variables

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/resume_tailor
```