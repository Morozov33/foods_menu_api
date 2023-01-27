build: # Building Docker images and start: test, app and db
	docker compose -f docker-compose.yml up -d --build

start: # Start Docker containers: app, db and cache
	docker compose start menu_app

stop: # Stop Docker containers
	docker compose stop menu_app db cashe

test: # Start Docker containers: test_app, test_db and test_cache
	docker compose -f docker-compose.tests.yml up -d --build

result: # Show tests result
	docker logs test_app

localstart: # Use last migration and local start uvicorn server for app
	export DATABASE_URL=postgresql+asyncpg://postgres@localhost:5433/food_menu_db && poetry run alembic upgrade head && poetry run uvicorn menu_app.main:app --reload

lint: #linter for code
	poetry run flake8 menu_app tests

migrate: #make migrations by Alembic
	export DATABASE_URL=postgresql+asyncpg://postgres@localhost/food_menu_db &&
	poetry run alembic revision --autogenerate -m "migrate"

localtest: #start pytest
	poetry run pytest

coverage: #start code coverage and write report is xml-file for CodeClimate
	poetry run pytest --cov-report xml --cov=menu_app tests/
