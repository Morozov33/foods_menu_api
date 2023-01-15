start: #start uvicorn server for FastAPI
	poetry run uvicorn menu_app.main:app --reload

lint: #linter for code
	poetry run flake8 menu_app

migrate: #make and add migrations by Alembic
	poetry run alembic revision --autogenerate -m "migrate"
	poetry run alembic upgrade head

test: #start pytest
	poetry run python3

coverage-xml: #start tests code coverage and write report is xml-file for CodeClimate
	poetry run coverage run --source='.'
	poetry run coverage xml

export: #make export dependens from poetry on Heroku
	poetry export -f requirements.txt --output requirements.txt
