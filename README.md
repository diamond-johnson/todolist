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