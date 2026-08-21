# FastAPI Employee Management API

A production-style learning project built with FastAPI, SQLAlchemy, SQLite, Pydantic, and pytest.

## Features

- Employee CRUD operations
- SQLite database
- SQLAlchemy ORM
- Pydantic request/response validation
- Automatic Swagger/OpenAPI documentation
- Pytest test suite
- Clean layered project structure

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for Swagger UI.

## API

- `GET /` health check
- `GET /employees` list employees
- `GET /employees/{id}` get employee
- `POST /employees` create employee
- `PUT /employees/{id}` update employee
- `DELETE /employees/{id}` delete employee
