## What this project does

This project demonstrates how to build and test RESTful APIs using FastAPI. It provides example endpoints, dependency management, and automated testing with pytest. The repository is intended for learning and experimenting with FastAPI features and best practices.

## Description
This project is a learning exercise using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## Run with Docker

Use this if you want to run API + PostgreSQL with one command.

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd fastapi
   ```

2. Build and start services:
   ```sh
   docker compose up --build
   ```

3. Open the API docs:
   ```
   http://localhost:8000/docs
   ```

4. Stop services:
   ```sh
   docker compose down
   ```

## Run Locally (System)

Use this if you want to run without Docker.

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd fastapi
   ```

2. Create and activate virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows:
   ```sh
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in project root:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=fastapi123
   DATABASE_NAME=fastapi
   DATABASE_USERNAME=postgres
   SECRET_KEY=FastApi
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

5. Run database migrations:
   ```sh
   alembic upgrade head
   ```

6. Start FastAPI app:
   ```sh
   uvicorn app.main:app --reload
   ```

7. Open the API docs:
   ```
   http://localhost:8000/docs
   ```

## Testing

Run tests using pytest:
```sh
pytest
```

## CI/CD

This project uses GitHub Actions for continuous integration. On every push or pull request, the workflow will:
- Set up Python
- Install dependencies
- Run tests with pytest
