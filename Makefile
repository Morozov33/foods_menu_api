build: # Building Docker images and start: test, app and db
	docker compose -f docker-compose.yml -f docker-compose.tests.yml up -d --build

start: # Start Docker containers: app and db
	docker compose start menu_app

stop: # Stop Docker containers
	docker compose stop menu_app db_food_menu

result: # Show tests result
	docker logs tests_menu_app

localstart: # Use last migration and local start uvicorn server for app
	export DATABASE_URL=postgresql+psycopg2://postgres@localhost/<database_name>
	poetry run alembic upgrade head
	poetry run uvicorn menu_app.main:app --reload

lint: #linter for code
	poetry run flake8 menu_app tests

migrate: #make migrations by Alembic
	export DATABASE_URL=postgresql+psycopg2://postgres@localhost/<database_name> &&
	poetry run alembic revision --autogenerate -m "migrate"

test: #start pytest
	export DATABASE_URL=sqlite:// && poetry run pytest

coverage: #start code coverage and write report is xml-file for CodeClimate
	poetry run pytest --cov-report xml --cov=menu_app tests/
