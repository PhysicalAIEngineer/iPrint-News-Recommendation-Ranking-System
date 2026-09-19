import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://iprint:iprint@localhost:5432/iprint",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def db_healthcheck():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
