start: #use last migration and start uvicorn server for app
	poetry run alembic upgrade head
	poetry run uvicorn menu_app.main:app --reload

lint: #linter for code
	poetry run flake8 menu_app tests

migrate: #make migrations by Alembic
	poetry run alembic revision --autogenerate -m "migrate"

test: #start pytest
	poetry run pytest

coverage: #start code coverage and write report is xml-file for CodeClimate
	poetry run pytest --cov-report xml --cov=menu_app tests/
