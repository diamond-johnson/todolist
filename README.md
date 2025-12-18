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