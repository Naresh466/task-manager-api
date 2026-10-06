# Task Manager API

A REST API for managing tasks, built with **Python, FastAPI, SQLAlchemy and SQLite**.

## Features
- Create, list, view, update and delete tasks
- Filter tasks by status
- Automatic interactive API docs
- Automated tests with pytest

## Tech stack
Python 3 | FastAPI | SQLAlchemy | SQLite | pytest

## Run it locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then open http://127.0.0.1:8000/docs

## Run the tests
```bash
python -m pytest
```

## API endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /tasks | Create a task |
| GET | /tasks | List tasks (optional `?status=`) |
| GET | /tasks/{id} | Get one task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |