import pytest
from fastapi.testclient import TestClient # This is a requests object

from app.main import app


# Creating out test database (test_db)
from app.config import settings
from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.oauth2 import create_access_token
from app import models
from alembic import command


# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:password123@localhost:5432/fastapi_db_test"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:"
    f"{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/"
    f"{settings.postgres_db}_test"
)      # The _test at the end is what makes t=this a different database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# Dependency
# def get_test_db():
#    """This functions creates a db sesssion each time we make a request, 
#    then closes the db session after we are done"""
    # db = TestingSessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()

# models.Base.metadata.create_all(bind=engine)

# app.dependency_overrides[get_db] = get_test_db #overriding get_db with get_test_db

# client = TestClient(app)

@pytest.fixture() #scope="module"
def session(): #session changs to db here, i.e db as output
    """fixtures will run before our tests starts"""
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture() #defaulr scope is function, changing it to module, gives it more advantages
def client(session): #our test 'client' ficture, now depends on our 'session' db fixture
    # run some code before we run our test
    def get_test_db():
        """This functions creates a db sesssion each time we make a request, 
        then closes the db session after we are done"""
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
    # run some code after our test finishes
    # command.upgrade("head")  #using alembic instead of sqlalchemy
    # command.downgrade("base")


@pytest.fixture
def test_user(client):
    """creating a fixture for our test user"""
    # create a user
    user_data = {"email":"ataime6@gmail.com", "password": "12345"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data.get('password') #since the response doesnt come back with the password, but we need the password
    return new_user


@pytest.fixture
def test_user2(client):
    """creating a fixture for our test user"""
    # create a user
    user_data = {"email":"ataime7@gmail.com", "password": "12345"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data.get('password') #since the response doesnt come back with the password, but we need the password
    return new_user

@pytest.fixture
def token(test_user):
    """create the token"""
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_conf_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    # print(posts)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts


