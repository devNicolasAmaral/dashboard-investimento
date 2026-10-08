from sqlmodel import create_engine, Session
from sqlalchemy.engine import URL

from app.core.config import settings


database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_db,
)

engine = create_engine(database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session