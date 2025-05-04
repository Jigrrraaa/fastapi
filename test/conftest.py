### conftest file function and fixtures are easy to accessiblt in pytest library so use this file add reuseable code here
### have created database connection so it will be fetched from all file
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import test_setting
from app.database import Base, get_db
from app.main import app
from app import models
from alembic import command
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{test_setting.database_username}:{test_setting.database_password}@{test_setting.database_hostname}/{test_setting.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocalTest = sessionmaker(autocommit = False, autoflush=False, bind=engine)

##get the DB connection
# def override_get_db():
#      db = SessionLocalTest()
#      try:
#           yield db
#      finally:
#           db.close() 

##override the db connection 
# app.dependency_overrides[get_db] = override_get_db

##fixture creat db connection session 
##create & Drop tables in DB 
@pytest.fixture()
def session():
     Base.metadata.drop_all(bind = engine)
     Base.metadata.create_all(bind = engine)
     db = SessionLocalTest()
     try:
          yield db
     finally:
          db.close() 

##use session fixture to override db connection with test_db
##create a new Test client
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close() 

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
     ##uncomment this if want to create and update table via alembic
    #  command.upgrade("head")
    #  yield TestClient(app)
    #  command.upgrade("base")


@pytest.fixture
def test_user(client):
    user_data = {"email" : "jigar@gmail.com",
                "phone_number" : "1234567890",
                "password" : "password123"}
    res = client.post("/User", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert new_user.get('email') == "jigar@gmail.com"
    assert res.status_code == 201
    return new_user

@pytest.fixture
def test_user1(client):
    user_data = {"email" : "jigar1@gmail.com",
                "phone_number" : "1234567890",
                "password" : "password123"}
    res = client.post("/User", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert new_user.get('email') == "jigar1@gmail.com"
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" :test_user.get('id')})

@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user1,session):
    post_data = [{
        "title" : "First Title",
        "content" : "first contenet",
        "who_created_user" : test_user['id']
    },
    {
        "title" : "Second Title",
        "content" : "Second contenet",
        "who_created_user" : test_user['id']
    },
    {
        "title" : "Third Title",
        "content" : "Third contenet",
        "who_created_user" : test_user['id']
    },
    {
        "title" : "fourth Title",
        "content" : "fourth contenet",
        "who_created_user" : test_user1['id']
    },
    {
        "title" : "Fifth Title",
        "content" : "Fifth contenet",
        "who_created_user" : test_user1['id']
    }]
    

    def create_post_model(post):
        return models.Posts(**post)
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Posts).all()
    return posts


