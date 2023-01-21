import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import Session, create_engine


def get_database_url():

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load envroinments variable
    env_path = os.path.join(BASE_DIR, '.env')
    load_dotenv(dotenv_path=env_path)

    # Get database url
    database_url = os.getenv("POSTGRES_DB_URL")
    return database_url


# Create engine for DB
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)


def get_session():

    # Return generator for database connection
    with Session(engine) as session:
        yield session
