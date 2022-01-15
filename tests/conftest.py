import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import Base, get_db
from app import models
from app.oauth2 import create_access_token

engine = create_engine(
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
    "_test"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hugo@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "hugo2@gmail.com", "password": "password2"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user.get("id")})


@pytest.fixture
def authorized_client(client, token):
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "user_id": test_user.get("id"),
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "user_id": test_user.get("id"),
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_user.get("id"),
        },
        {
            "title": "4th title",
            "content": "4th content",
            "user_id": test_user2.get("id"),
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_list = list(map(create_post_model, posts_data))
    session.add_all(post_list)
    session.commit()
    return session.query(models.Post).all()


@pytest.fixture
def updated_post_data(test_posts):
    return {
        "title": "updated_title",
        "content": "updated_content",
        "id": test_posts[0].id,
    }


@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user.get("id"))
    session.add(new_vote)
    session.commit()
