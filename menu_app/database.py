import os
from sqlmodel import Session, create_engine


# Create engine for DB
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)


def get_session():

    # Return generator for database connection
    with Session(engine) as session:
        yield session
