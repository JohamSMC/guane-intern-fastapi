from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_USER = os.getenv("POSTGRES_USER")
PG_DB = os.getenv("POSTGRES_DB")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode=prefer'.format(
    PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()