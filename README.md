# 🧱 Flask API scaffold

A clean, testable, and production-ready **Flask API scaffold** that demonstrates how to build modern Python backend services using **Clean Architecture**, **SOLID principles**, and **type safety**.

This project provides a complete CRUD for `clients`, with robust validation, full E2E test coverage, and Dockerized environments for dev, test, and prod.

---

## ✅ Features

- ✅ Clean Architecture (controllers, services, repositories)
- ✅ Full type annotations (with `mypy` and `pydantic`)
- ✅ Dependency Injection (via `dependency-injector`)
- ✅ PostgreSQL support with SQLAlchemy
- ✅ Full E2E test suite using `pytest` and `pytest-cov`
- ✅ API docs via Swagger (`flasgger`)
- ✅ Docker multi-stage builds (including **Distroless** production)
- ✅ Poetry for Python packaging and dependency management

---

## 🔧 Tech Stack

| Layer                | Tool / Library                                                                       |
| -------------------- | ------------------------------------------------------------------------------------ |
| API Framework        | [Flask](https://flask.palletsprojects.com/) with Blueprints                          |
| ORM                  | [SQLAlchemy](https://www.sqlalchemy.org/)                                            |
| Validation & Typing  | [Pydantic v2](https://docs.pydantic.dev), [mypy](https://mypy-lang.org/)             |
| Dependency Injection | [dependency-injector](https://python-dependency-injector.ets-labs.org/)              |
| API Docs             | [Flasgger](https://github.com/flasgger/flasgger) (Swagger UI)                        |
| Testing              | [pytest](https://docs.pytest.org/), [pytest-cov](https://pytest-cov.readthedocs.io/) |
| Package Manager      | [Poetry](https://python-poetry.org/)                                                 |
| Runtime Environment  | Docker (multi-stage builds + distroless prod)                                        |
| Coverage Threshold   | 90% minimum enforced via `pytest.ini`                                                |

---

## 📁 Folder Structure

```txt
app/
├── application/
│   ├── dtos/              # Request validation models (Pydantic)
│   ├── exceptions.py      # App-level errors
│   └── services/          # Use cases and interfaces
├── config.py              # Configuration loader
├── containers.py          # DI container setup
├── infrastructure/
│   ├── models/            # SQLAlchemy ORM models
│   └── repositories/      # Database access logic
├── interfaces/
│   └── controllers/       # Flask routes (HTTP interface)
├── utils/                 # Logging, helpers, request validation
├── main.py                # App entrypoint and registration
```

---

## 📦 Environment Configuration

| File           | Description                                       |
| -------------- | ------------------------------------------------- |
| `.env.dev`     | Development environment                           |
| `.env.test`    | Testing configuration                             |
| `.env`         | Production configuration (used with prod compose) |
| `.env.example` | Template for creating your own `.env`             |

---

## 🚀 Running the Project

### 📦 Development

```bash
./docker-run-dev.sh
```

- Runs `make run` inside the container
- API: [http://localhost:5000](http://localhost:5000)
- Swagger: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

---

### 🧪 Testing

```bash
./docker-run-tests-and-lint.sh
```

- Runs full **E2E tests** using `pytest`
- Enforces minimum 90% coverage
- Generates HTML report: `htmlcov/index.html`

---

### 🏗️ Production

1. Copy the template:

```bash
cp .env.example .env
```

2. Set real database credentials in `.env`
3. Start:

```bash
docker compose --env-file .env -f docker-compose.prod.yml up -d
```

---

## 🧪 Type Safety and Code Quality

- Full static typing (`.pyi`-like safety via Pydantic & mypy)
- Code formatting with [black](https://black.readthedocs.io/)
- Import sorting with [isort](https://pycqa.github.io/isort/)
- Type checks with `mypy`
- Lint task available via `make lint`

---

## 📦 Poetry Usage

### Add a new dependency

```bash
docker compose -f docker-compose.dev.yml run --rm app poetry add <package>@<version>
docker compose -f docker-compose.dev.yml build app
```

### Upgrade dependencies

```bash
docker compose -f docker-compose.dev.yml run --rm app poetry update
docker compose -f docker-compose.dev.yml build app
```

---

## 🛀 Clean Architecture Principles

- **Interfaces** (HTTP): `interfaces/controllers`
- **Use Cases** (Services): `application/services`
- **Entities / Models**: `infrastructure/models`
- **DTOs** for payload safety
- **Protocols** for interface-driven development
- **Exception abstraction** via custom `AppError`

---

## 🛠️ Make Commands

```bash
make run         # Run the app
make test        # Run tests
make test-cov    # Run tests with coverage
make lint        # Format + sort + type check
```

---

## 📆 Coverage & Testing Summary

- Tests simulate real API calls via Flask test client
- Tables are recreated before each test via fixtures
- Fail early if coverage drops below 90%

---

## 📩 License

MIT © Denis Candido
