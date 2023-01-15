import os
from sqlmodel import Session, create_engine


# database_url = os.getenv('POSTGRES_DB_URL')
DEBUG = os.getenv('DEBUG')
database_url = "postgresql+psycopg2://postgres@localhost/food_menu"
engine = create_engine(database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
