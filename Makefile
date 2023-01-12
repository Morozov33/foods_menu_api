start: #start uvicorn server for FastAPI
	poetry run python3 uvicorn main:app --reload

lint: #linter for code
	poetry run flake8  <dir_names>

migrate: #make and add migrations
	poetry run python3
	poetry run python3

test: #start pytest
	poetry run python3

coverage-xml: #start tests code coverage and write report is xml-file for CodeClimate
	poetry run coverage run --source='.'
	poetry run coverage xml

export: #make export dependens from poetry on Heroku
	poetry export -f requirements.txt --output requirements.txt
