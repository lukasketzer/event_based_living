
from sqlalchemy import (
    create_engine,
    Column,
    String,
    DateTime,
    Integer,
    text,
    Date,
    Time,
)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

import uuid
import uuid

POSTGRES_USER = "app"
POSTGRES_PASSWORD = "password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB_NAME = "postgres"
from .models import EventOptional

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()


# Main events table
class EventsDB(Base):
    __tablename__ = "events"
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    name = Column(String)
    description = Column(String)
    event_type = Column(String)
    start_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
    end_date = Column(Date, nullable=True)
    end_time = Column(Time, nullable=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    postal_code = Column(String)
    venue = Column(String, nullable=True)
    url = Column(String)
    price = Column(String)


CONNECTION_STRING = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    session = SessionLocal()
    print(session.execute(text("SELECT 1")).scalar())
    session.close()
