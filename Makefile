start: #use last migration and start uvicorn server for app
	poetry run alembic upgrade head
	poetry run uvicorn menu_app.main:app --reload

lint: #linter for code
	poetry run flake8 menu_app

migrate: #make migrations by Alembic
	poetry run alembic revision --autogenerate -m "migrate"
