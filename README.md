### Status: [![linter](https://github.com/Morozov33/foods_menu_api/actions/workflows/linter.yml/badge.svg)](https://github.com/Morozov33/foods_menu_api/actions/workflows/linter.yml)  [![tests](https://github.com/Morozov33/foods_menu_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Morozov33/foods_menu_api/actions/workflows/tests.yml)  [![Maintainability](https://api.codeclimate.com/v1/badges/a01595bc13c6dadfd0ad/maintainability)](https://codeclimate.com/github/Morozov33/foods_menu_api/maintainability)  [![Test Coverage](https://api.codeclimate.com/v1/badges/a01595bc13c6dadfd0ad/test_coverage)](https://codeclimate.com/github/Morozov33/foods_menu_api/test_coverage)
### It's usinig: ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)  ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)  ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
----
Для запуска на локальной машине:
1. `git clone git@github.com:Morozov33/foods_menu_api.git`
2. `cd foods_menu_api`
3. `make build` собирает образы и запускает контейнеры приложения в фоновом режиме. При сборке используются образы `python:3.10-slim` и `postgres:15.1-alpine`
4. При сборке запускаются тесты, посмотреть результаты: `make result`
5. Приложение доступно по адресу: `127.0.0.1:8000`
6. Остановка контейнеров `make stop`
7. Запуск контейнеров `make start` 
