# AI Study Project

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=111111)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

AI Study Project is a full-stack productivity and personal management application for organizing tasks, goals, notes, reminders, budgets, and expenses. It combines a FastAPI backend, a React + TypeScript frontend, JWT-secured user workflows, and AI-powered productivity tools built with the NVIDIA Nemotron AI API.

The project is designed as a portfolio-ready full-stack application with protected routes, RESTful resource management, a responsive dashboard, automated backend tests, and practical AI features such as chat, summarization, email generation, task breakdowns, and budget insights.

## Features

### Authentication

- User registration
- User login
- JWT-based authentication
- Protected frontend routes
- Authenticated API access with bearer tokens

### Productivity Management

| Domain | Capabilities |
| --- | --- |
| Tasks | Create, update, delete, and view tasks |
| Goals | Create, update, delete, and track goals |
| Notes | Create, update, delete, and view notes |
| Reminders | Create, update, delete, and view reminders |
| Budgets | Create, update, delete, and view budgets |
| Expenses | Create, update, delete, and view expenses |

### AI Tools

- AI Assistant Chat powered by NVIDIA Nemotron
- AI Note Summarizer
- AI Email Generator
- AI Task Breakdown tool
- AI Budget Insights tool
- Copy AI response support
- Clear conversation support
- Message timestamps

### Frontend

- React + TypeScript application
- Responsive dashboard
- Protected pages
- Typed API modules with Axios
- Authentication context
- Reusable layout and state components

### Backend

- REST API built with FastAPI
- Pydantic request and response schemas
- SQLAlchemy ORM models and services
- Dependency injection for database sessions and auth
- JWT security
- Alembic migration structure
- Automated backend test suite

## Architecture Overview

```text
React + TypeScript Frontend
        |
        | Axios HTTP client
        v
FastAPI REST API
        |
        | Pydantic schemas, routers, services
        v
SQLAlchemy ORM
        |
        v
SQLite Database

AI routes and services
        |
        v
NVIDIA Nemotron AI API
```

The application follows a layered structure:

- The frontend handles routing, protected pages, forms, dashboard views, and user interactions.
- Axios attaches JWT tokens to authenticated requests.
- FastAPI routers expose REST endpoints for each feature area.
- Service modules contain business logic.
- SQLAlchemy models represent persisted data.
- Pydantic schemas validate API payloads.
- AI service modules wrap calls to NVIDIA Nemotron.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Alembic |
| Database | SQLite |
| Authentication | JWT, OAuth2 password flow, Passlib |
| Frontend | React, TypeScript, Vite, React Router |
| API Client | Axios |
| AI | NVIDIA Nemotron AI API |
| Testing | Pytest, FastAPI TestClient |

## Folder Structure

```text
AI-Study-Project/
|-- backend/
|   |-- alembic/
|   |   `-- versions/
|   |-- app/
|   |   |-- ai/
|   |   |   |-- routers/
|   |   |   |-- schemas/
|   |   |   `-- services/
|   |   |-- core/
|   |   |-- database/
|   |   |-- models/
|   |   |-- routers/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- main.py
|   |   `-- settings.py
|   |-- tests/
|   `-- alembic.ini
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- api/
|   |   |-- assets/
|   |   |-- components/
|   |   |-- context/
|   |   |-- pages/
|   |   |-- routes/
|   |   |-- types/
|   |   |-- App.tsx
|   |   `-- main.tsx
|   |-- package.json
|   `-- vite.config.ts
|-- .gitignore
`-- README.md
```

## Installation Guide

### Prerequisites

- Python 3.11 or later
- Node.js 20 or later
- npm
- NVIDIA API key for Nemotron-powered AI features

Clone the repository:

```bash
git clone https://github.com/your-username/AI-Study-Project.git
cd AI-Study-Project
```

## Backend Setup

From the project root:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install fastapi uvicorn sqlalchemy alembic pydantic python-dotenv python-jose passlib[bcrypt] python-multipart openai pytest httpx
```

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=sqlite:///./ai_study.db
TEST_DATABASE_URL=sqlite:///./test_ai_study.db
SECRET_KEY=replace-with-a-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
NVIDIA_API_KEY=replace-with-your-nvidia-api-key
```

Run database migrations if needed:

```bash
alembic upgrade head
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Frontend Setup

From the project root:

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## Environment Variables

### Backend

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | Main database connection URL | `sqlite:///./ai_study.db` |
| `TEST_DATABASE_URL` | Test database connection URL | `sqlite:///./test_ai_study.db` |
| `SECRET_KEY` | Secret used to sign JWT tokens | `replace-with-a-secure-secret-key` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `30` |
| `NVIDIA_API_KEY` | API key for NVIDIA Nemotron | `nvapi-...` |

### Frontend

| Variable | Description | Example |
| --- | --- | --- |
| `VITE_API_BASE_URL` | Backend API base URL used by Axios | `http://localhost:8000` |

## Running the Application

Run the backend:

```bash
cd backend
uvicorn app.main:app --reload
```

Run the frontend in a separate terminal:

```bash
cd frontend
npm run dev
```

Open the app:

```text
http://localhost:5173
```

## Running Tests

Run the backend test suite:

```bash
cd backend
pytest
```

Run frontend linting:

```bash
cd frontend
npm run lint
```

Build the frontend:

```bash
cd frontend
npm run build
```

## API Overview

Base URL:

```text
http://localhost:8000
```

| Area | Method | Endpoint | Description |
| --- | --- | --- | --- |
| Health | `GET` | `/` | Backend health message |
| Auth | `POST` | `/register` | Register a user |
| Auth | `POST` | `/login` | Log in and receive an access token |
| Auth | `GET` | `/me` | Get the authenticated user |
| Tasks | `GET` | `/tasks` | List tasks |
| Tasks | `POST` | `/tasks` | Create a task |
| Tasks | `GET` | `/tasks/{task_id}` | Get a task |
| Tasks | `PUT` | `/tasks/{task_id}` | Update a task |
| Tasks | `DELETE` | `/tasks/{task_id}` | Delete a task |
| Goals | `GET` | `/goals` | List goals |
| Goals | `POST` | `/goals` | Create a goal |
| Goals | `GET` | `/goals/{goal_id}` | Get a goal |
| Goals | `PUT` | `/goals/{goal_id}` | Update a goal |
| Goals | `DELETE` | `/goals/{goal_id}` | Delete a goal |
| Notes | `GET` | `/notes` | List notes |
| Notes | `POST` | `/notes` | Create a note |
| Notes | `GET` | `/notes/{note_id}` | Get a note |
| Notes | `PUT` | `/notes/{note_id}` | Update a note |
| Notes | `DELETE` | `/notes/{note_id}` | Delete a note |
| Reminders | `GET` | `/reminders` | List reminders |
| Reminders | `POST` | `/reminders` | Create a reminder |
| Reminders | `GET` | `/reminders/{reminder_id}` | Get a reminder |
| Reminders | `PUT` | `/reminders/{reminder_id}` | Update a reminder |
| Reminders | `DELETE` | `/reminders/{reminder_id}` | Delete a reminder |
| Budgets | `GET` | `/budgets` | List budgets |
| Budgets | `POST` | `/budgets` | Create a budget |
| Budgets | `GET` | `/budgets/{budget_id}` | Get a budget |
| Budgets | `PUT` | `/budgets/{budget_id}` | Update a budget |
| Budgets | `DELETE` | `/budgets/{budget_id}` | Delete a budget |
| Expenses | `GET` | `/expenses` | List expenses |
| Expenses | `POST` | `/expenses` | Create an expense |
| Expenses | `GET` | `/expenses/{expense_id}` | Get an expense |
| Expenses | `PUT` | `/expenses/{expense_id}` | Update an expense |
| Expenses | `DELETE` | `/expenses/{expense_id}` | Delete an expense |
| Dashboard | `GET` | `/dashboard` | Get dashboard summary data |
| AI | `POST` | `/assistant/chat` | Chat with the AI assistant |
| AI | `POST` | `/ai/summarize-note` | Summarize note content |
| AI | `POST` | `/ai/generate-mail` | Generate email content |
| AI | `POST` | `/ai/task-breakdown` | Break a goal into actionable tasks |
| AI | `POST` | `/ai/budget-insights` | Generate budget insights |

Protected endpoints require an authorization header:

```http
Authorization: Bearer <access_token>
```

## AI Features

AI Study Project integrates NVIDIA Nemotron through backend AI services. The AI functionality is exposed through authenticated API endpoints and frontend tools.

| Feature | Endpoint | Purpose |
| --- | --- | --- |
| Assistant Chat | `/assistant/chat` | General productivity assistant conversation |
| Note Summarizer | `/ai/summarize-note` | Condense long notes into concise summaries |
| Email Generator | `/ai/generate-mail` | Draft emails from a stated purpose |
| Task Breakdown | `/ai/task-breakdown` | Convert a goal into smaller actionable tasks |
| Budget Insights | `/ai/budget-insights` | Analyze budget information and return practical insights |




## Future Improvements

- Add refresh token support
- Add password reset flow
- Add email or push notifications for reminders
- Add recurring tasks and reminders
- Add richer analytics for goals, spending, and productivity trends
- Add file attachments for notes
- Add Docker support for easier local setup
- Add CI workflows for linting, testing, and builds
- Add deployment documentation for frontend and backend hosting



## License

This project is intended for educational and portfolio use. 
