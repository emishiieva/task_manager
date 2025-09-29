# Task Management System

A simple task management application with a Vue 3 + Vite frontend and a FastAPI + SQLAlchemy backend.
The project is containerized with Docker and uses PostgreSQL as the database.

---

## Tech Stack

- **Frontend**: Vue 3, Vite, TailwindCSS
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose

---

## Setup and Run

### 1. Clone the repository

```bash
git clone <repo_url>
cd task_manager
```

### 2. Create `.env` files

#### frontend/.env

### For Docker (frontend container connecting to backend via host port)
```env
VITE_API_BASE_URL=http://localhost:8000
```

### For local development (frontend running locally, backend in its container)
```env
VITE_API_BASE_URL=http://backend:8000
```

#### backend/.env

```env
DATABASE_URL=postgresql+psycopg2://myuser:mypassword@db:5432/task_db
```

---

### 3. Run the application

```bash
docker-compose up --build
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- PostgreSQL: `localhost:5432` (user: `myuser`, password: `mypassword`, db: `task_db`)

---

### 4. Create tables

```bash
docker-compose exec backend python create_tables.py
```

---

## Useful Commands

### Rebuild the project

```bash
docker-compose up --build
```

### Stop containers

```bash
docker-compose down
```

---

## API Docs

Once running, API documentation is available at:
 [http://localhost:8000/docs](http://localhost:8000/docs)

---
