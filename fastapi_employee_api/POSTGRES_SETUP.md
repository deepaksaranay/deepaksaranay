# PostgreSQL Setup

Set `DATABASE_URL` to a PostgreSQL connection string before starting the API.

Example:

`postgresql+psycopg://postgres:postgres@localhost:5432/employees`

Run Alembic migrations with:

`alembic upgrade head`
