## What this project does

This project demonstrates how to build and test RESTful APIs using FastAPI. It provides example endpoints, dependency management, and automated testing with pytest. The repository is intended for learning and experimenting with FastAPI features and best practices.

## Description
This project is a learning exercise using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## Setup

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd FastApi
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Docker Compose

You can run this project using Docker Compose for easy setup and deployment. Make sure you have `docker` and `docker-compose` installed.

To start the application with Docker Compose:
```sh
docker-compose up --build
```

This will build the Docker image and start all defined services. You can access the FastAPI app at the URL specified in your `docker-compose.yml` file (commonly `http://localhost:8000`).

To stop the services:
```sh
docker-compose down
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
