import os
from sqlmodel import SQLModel, create_engine


def get_engine():
    POSTGRES_DB_URL = os.getenv('POSTGRES_DB_URL')
    DEBUG = os.getenv('DEBUG')
    engine = create_engine(POSTGRES_DB_URL, echo=bool(DEBUG))
    return engine


def connect_db_and_create_tables():
    SQLModel.metadata.create_all(get_engine())
