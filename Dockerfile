FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy lock-file
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# install python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# add app
COPY ./menu_app /app/menu_app
COPY ./tests /app/tests
COPY ./migrations /app/migrations
COPY ./alembic.ini /app/alembic.ini
