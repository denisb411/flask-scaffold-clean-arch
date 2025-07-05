# =======================
# Dockerfile (multi-stage)
# =======================
FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.3

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry via pip (specific version)
RUN pip install --no-cache-dir poetry==2.1.3

WORKDIR /app
ENV PYTHONPATH=/app

# Copy and install only base dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false

COPY app app
COPY Makefile Makefile

# =========================
# 🧪 Test Stage
# =========================
FROM base AS test

COPY tests tests
COPY pytest.ini pytest.ini

RUN poetry install --with test --no-root --no-ansi --no-interaction
CMD ["make", "test"]

# =========================
# 🛠 Dev Stage
# =========================
FROM base AS dev

COPY mypy.ini mypy.ini

RUN poetry install --with dev --no-root --no-ansi --no-interaction
CMD ["make", "run-dev"]

# =========================
# 🚀 Prod Stage
# =========================
FROM base AS prod
RUN poetry install --only main --no-root --no-ansi --no-interaction
CMD ["poetry", "run-prod"]
