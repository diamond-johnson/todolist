# To-Do List Project (Phase 1 - In-Memory)

A simple in-memory To-Do List application built with Python OOP, following SOLID principles, dependency injection, and clean code conventions.

## Setup

1. Install Poetry if not already: `pip install poetry`.
2. Run `poetry install` to create the virtual environment and install dependencies.
3. Copy `.env.example` to `.env` and configure limits.
4. Run the app: `poetry run todolist`.

## Usage

The CLI menu allows creating/editing/deleting projects and tasks, with validation and limits enforced.

## Running in PyCharm

- Use the Poetry virtual environment (PyCharm should detect it).
- Mark `src` as Sources Root for proper imports.
- Run `cli.py` or use the script `todolist`.

## Testing

Run `poetry run pytest` (add tests in a `tests/` folder as needed).

## Future Extensions

Designed for persistence (e.g., JSON/SQLite) and web API (FastAPI) in future phases.



## To-Do List Project (Phase 2 - SQLAlchemy Persistence)
A full-featured CLI To-Do List application with persistent storage using PostgreSQL and SQLAlchemy.
This phase builds directly on Phase 1, replacing the in-memory implementation with a robust, production-ready persistence layer while keeping the clean architecture, SOLID principles, dependency injection, and business rules intact.

## Summary of Phase 2 Achievements
In this phase, we successfully upgraded the application from in-memory storage to persistent database storage using:

- PostgreSQL as the database
- SQLAlchemy 2.0
- Alembic for database migrations and versioning
- Repository pattern with abstract interfaces and concrete SQLAlchemy implementations
- Full CRUD operations for Projects and Tasks with proper relationships (one-to-many + cascade delete)
- Business rules enforcement in Services (project/task limits, unique project names, status/deadline validation)
- Custom exception hierarchy for better error handling
- Auto-closing of overdue tasks via a scheduled background job (APScheduler with persistent job store)
- Configuration via .env files

The CLI remains the main interface, now working seamlessly with real persisted data across restarts.

## Setup

- Install Poetry if not already: pip install poetry
- Run poetry install to create the virtual environment and install dependencies (including psycopg2-binary, alembic, apscheduler)
- Copy .env.example to .env and fill in your PostgreSQL credentials:
```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todolist
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100
```
Make sure PostgreSQL is running and the database exists (or create it).
Apply database migrations:
```
poetry run alembic upgrade head
```
This will create the projects and tasks tables.

## Usage
Run the Main CLI Application
```
poetry run python -m app.main
# or
poetry run todolist   # (if you added a script in pyproject.toml)
```
The interactive menu allows you to:

- Create, edit, delete, and list projects
- Create, edit, change status, delete, and list tasks within projects
- All data is saved permanently in the database

## Run the Overdue Task Auto-Closer (Optional, in separate terminal)
```
poetry run python -m app.commands.scheduler
```
This starts a persistent background scheduler that:

- Checks for overdue tasks (deadline passed and not DONE) every 15 minutes
- Automatically marks them as DONE and sets closed_at
- Jobs are stored in the database, so it survives restarts
```
todolist/
├── app/
│   ├── cli/              → Console interface
│   ├── commands/         → autoclose_overdue.py + scheduler.py
│   ├── core/             → Config loading
│   ├── db/               → SQLAlchemy engine, session, Base
│   ├── exceptions/       → Custom exception hierarchy
│   ├── models/           → Project, Task, TaskStatus (SQLAlchemy models)
│   ├── repositories/     → Abstract interfaces + SQLAlchemy implementations
│   ├── services/         → Business logic (ProjectService, TaskService, BaseService)
│   └── main.py           → Entry point
├── alembic/                  → Migration scripts
├── alembic.ini
├── pyproject.toml
├── .env / .env.example
└── README.md
```
### Future Extensions
This foundation is now ready for:

- Web API with FastAPI (expose the same services)
- User authentication and multi-tenancy
- Task reminders/notifications
- Rich CLI with tables (using rich or tabulate)


## Phase 3 (WEB API)
This version transitions the application from a simple command-line tool to a full-featured web API and deprecating the old CLI.
## Features
- RESTful API: A complete API for CRUD (Create, Read, Update, Delete) operations on Projects and Tasks.

- Layered Architecture: Follows a clean architecture with distinct layers for API (Controllers), Business Logic (Services), and Data Access (Repositories).

- Asynchronous Support: Built with async and await for high-performance, non-blocking I/O.

- Automatic Interactive Documentation: API documentation is automatically generated by FastAPI and available at the /docs endpoint (Swagger UI).

- Database Persistence: Data is stored in a PostgreSQL database, managed via Docker.

- Database Migrations: Uses Alembic to manage database schema changes.

- Background Jobs: Includes a scheduler to run background tasks, such as automatically closing overdue tasks.

- Deprecated CLI: The original CLI is preserved but marked as deprecated, guiding users to the new API.

## 🛠️ Tech Stack
- Backend: Python 3, FastAPI

- Database: PostgreSQL

- ORM: SQLAlchemy 2.0 (with async support)

- Containerization: Docker

- Dependency Management: Poetry
 
- Database Migrations: Alembic

- API Testing: Postman

## 📂 Project Setup
Prerequisites
- Python 3.10+

- Poetry

- Docker Desktop

1. Clone the Repository
```
git clone <your-repository-url>
cd <repository-folder>
```

2. Install Dependencies
Use Poetry to install all the required Python packages from the pyproject.toml file.
```
poetry install
```

3. Configure Environment Variables
Create a .env file in the root of the project. You can copy the example below. Ensure the credentials match what you use in your Docker command.
.env file:
```
# Database Credentials
DB_USER=rose
DB_PASSWORD=secret123
DB_HOST=localhost
DB_PORT=5433
DB_NAME=todolistdb

# Application Configuration
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=100
```

## 🚀 Running the Application
Follow these steps in order to launch the database and the API server.

Step 1: Start the PostgreSQL Database
Run the PostgreSQL database as a Docker container.

For the first time:
```
docker run --name todolist-db -e POSTGRES_USER=rose -e POSTGRES_PASSWORD=secret123 -e POSTGRES_DB=todolistdb -p 5433:5432 -d postgres
```

To restart an existing, stopped container:
```
docker start todolist-db
```

Step 2: Apply Database Migrations
This command creates the projects and tasks tables in your database based on the SQLAlchemy models. You only need to run this the very first time you set up the database.
```
poetry run alembic upgrade head
```

Step 3: Start the API Server
Run the Uvicorn server to start your FastAPI application.
```
poetry run uvicorn app.main:app --reload
```
Your API is now live and accessible at http://127.0.0.1:8000.

Step 4: (Optional) Start the Background Scheduler
To enable the automatic closing of overdue tasks, open a new, separate terminal and run:
```
poetry run python -m app.commands.scheduler
```

## ⚡ Using the API
- Interactive Docs (Swagger UI): Open your browser and navigate to http://127.0.0.1:8000/docs to see all available endpoints and test them directly.

- Postman: Use Postman to create a collection for this API. The base URL for all API v1 endpoints is http://127.0.0.1:8000/api/v1.
Example POST request to create a project: http://127.0.0.1:8000/api/v1/projects/

## ⚠️ Deprecated CLI
The original command-line interface still functions but is deprecated. It will show a warning upon use. To run it:
```
poetry run python -m app.main
```
