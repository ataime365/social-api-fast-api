import pytest
from jose import jwt

from app import schemas
from app.config import settings
# from .database import client, session #fixtures  #database here is our test database file


def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == 'Hello world'
    assert response.status_code == 200

def test_create_user(client): #fixtures are available as a parameter
    res = client.post('/users/', json={"email":"ataime6@gmail.com", "password": "12345"})
    new_user = schemas.UserOut(**res.json()) #Does its own pydantic validation
    assert new_user.email == "ataime6@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user): #fixtures are available as a parameter
    # create a user, using est_user, before trying to login
    res = client.post('/login', data={"username":test_user['email'], "password": test_user['password']})
    token = schemas.Token(**res.json()) #Does its own pydantic validation
    # decoding the token
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id") # Extracting the id from the decoded token
    # assert new_user.email == "ataime6@gmail.com"
    assert id == test_user['id']
    assert token.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
            ("wrongemail@gmail.com", 'password123', 403),
            ("ataime@gmail.com", 'wrongpassword', 403),
            ("wrongemail@gmail.com", 'wrongpassword', 403),
            (None, 'password123', 422),
            ("ataime@gmail.com", None, 422)]
            )
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={"username":email , "password": password })
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

