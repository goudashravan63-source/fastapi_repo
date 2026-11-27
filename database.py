# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# sql_database_url = "postgresql+psycopg://postgres:db%40123@localhost/fastapi"
# engine = create_engine(sql_database_url)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
# You can override everything with one DATABASE_URL environment variable.
# Otherwise the values below are used. URL.create() takes care of special
# characters in the password (like @), so no manual encoding is needed.
DATABASE_URL = os.getenv("DATABASE_URL")
from dotenv import load_dotenv
load_dotenv()




if DATABASE_URL is None:
    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg",
        username=settings.database_username,
        password=settings.database_password,
        host=settings.database_hostname,
        port=int(settings.database_port),
        database=settings.database_name,
    )

    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



connect_args = {}
if str(DATABASE_URL).startswith("sqlite"):
    connect_args = {"check_same_thread": False}  # only needed for the SQLite tests

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

