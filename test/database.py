# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import test_setting
# from app.database import Base, get_db
# from app.main import app
# from alembic import command


# SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{test_setting.database_username}:{test_setting.database_password}@{test_setting.database_hostname}/{test_setting.database_name}'

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocalTest = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# ##get the DB connection
# # def override_get_db():
# #      db = SessionLocalTest()
# #      try:
# #           yield db
# #      finally:
# #           db.close() 

# ##override the db connection 
# # app.dependency_overrides[get_db] = override_get_db

# ##fixture creat db connection session 
# ##create & Drop tables in DB 
# @pytest.fixture()
# def session():
#      Base.metadata.drop_all(bind = engine)
#      Base.metadata.create_all(bind = engine)
#      db = SessionLocalTest()
#      try:
#           yield db
#      finally:
#           db.close() 

# ##use session fixture to override db connection with test_db
# ##create a new Test client
# @pytest.fixture()
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close() 

#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
#      ##uncomment this if want to create and update table via alembic
#     #  command.upgrade("head")
#     #  yield TestClient(app)
#     #  command.upgrade("base")