import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, Column, VARCHAR

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id = Column(Integer, primary_key=True)
    birth_year = Column(VARCHAR(60))
    eye_color = Column(VARCHAR(60))
    films = Column(VARCHAR(2000))
    gender = Column(VARCHAR(60))
    hair_color = Column(VARCHAR(60))
    height = Column(VARCHAR(60))
    homeworld = Column(VARCHAR(60))
    mass = Column(VARCHAR(60))
    name = Column(VARCHAR(60))
    skin_color = Column(VARCHAR(60))
    species = Column(VARCHAR(2000))
    starships = Column(VARCHAR(2000))
    vehicles = Column(VARCHAR(2000))