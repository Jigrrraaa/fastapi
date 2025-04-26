from time import time
import psycopg
from psycopg.rows import dict_row
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}/{setting.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close() 

# while True:
#      try:
#           conn = psycopg.connect(
#                host='localhost',
#                dbname='fastapi',
#                user='postgres',
#                password='fastapi123',
#                row_factory=dict_row  # Corrected parameter name
#           )
#           cursor = conn.cursor()
#           print("Database connection was successful!")
#           break
#      except Exception as error:
#           print("Connecting to database failed")
#           print("Error:", error)
#           time.sleep(2)
