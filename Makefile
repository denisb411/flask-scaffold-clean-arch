.PHONY: test test-cov lint run run-dev run-tests install run-prod run-dev

# Install dependencies using Poetry
install:
	poetry install

# Run tests
test:
	python -m pytest tests

# Run the Flask app (production mode: no reload)
run:
	python app/main.py

# Run the Flask app with auto-reload (development mode)
run-dev:
	python -m flask run --host=0.0.0.0 --port=5000

# Run the Flask app using Gunicorn (production mode)
run-prod:
	gunicorn -w 4 -b 0.0.0.0:5000 "app.main:create_app()"

# Lint and static analysis
lint:
	python -m black app tests
	python -m isort app tests
	python -m mypy app
