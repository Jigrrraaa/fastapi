from app import schemas
from  jose import jwt
from app.config import test_setting
import pytest
from fastapi import status



# def test_root(client):
#     res = client.get("/get")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Welcome to my api" 
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/User", json={"email" : "hello@gmail.com", "phone_number" : "1234567890", "password" : "password123"})
    new_user = schemas.Users(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED

def test_login_user(client, test_user):
    res = client.post("/login", data={"username" : test_user.get('email'),"password" : test_user.get('password')})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, test_setting.secret_key,algorithms= test_setting.algorithm)
    id = payload.get("user_id")
    assert id == test_user.get('id')
    assert login_res.token_type == "Bearer"
    assert res.status_code == status.HTTP_200_OK

@pytest.mark.parametrize("email,password , status_code, error_message",[
    ('wrongemail@gmail.com', 'password123', status.HTTP_403_FORBIDDEN, "Invalid Creditails"),
    ('jigar@gmail.com', 'wrongPassword', status.HTTP_403_FORBIDDEN, "Invalid Creditails"),
    (None,'password123', status.HTTP_422_UNPROCESSABLE_ENTITY , "Username and password are required"),
    ('jigar@gmail.com', None, status.HTTP_422_UNPROCESSABLE_ENTITY, "Username and password are required")
])    
def test_incorrect_login(client, email, password, status_code,error_message):
    res = client.post("/login", data={"username" : email,"password" : password})
    assert res.status_code == status_code
    assert res.json().get('detail') == error_message


