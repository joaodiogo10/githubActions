from src.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.database import get_db
from src.models import Base
import pytest
import src.schemas as schemas

SQLALCHEMY_DATABASE_URL = f'mariadb+mariadbconnector://{settings.MARIADB_USER}:{settings.MARIADB_PASSWORD}' \
    f'@{settings.MARIADB_HOST}:{settings.MARIADB_PORT}/{settings.MARIADB_DATABASE}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client: TestClient) -> schemas.User:
    user_data = {"name": "Ricardo",
                 "email": "ricardocas@gmail.com",
                 "address": "Rua do francisco perdido"}
    res = client.post("/users/", json=user_data)

    new_user = schemas.User(**res.json())
    return new_user


@pytest.fixture()
def test_users(client: TestClient) -> list[schemas.User]:
    users = []
    user_data = {"name": "Ricardo",
                 "email": "ricardocas@gmail.com",
                 "address": "Rua do francisco perdido"}
    res = client.post("/users/", json=user_data)
    users.append(schemas.User(**res.json()))

    user_data = {"name": "Rui Aguiar",
                 "email": "ruiAguiar@ua.pt",
                 "address": "Praceira dos cansados"}
    res = client.post("/users/", json=user_data)
    users.append(schemas.User(**res.json()))

    user_data = {"name": "Sergio Calado",
                 "email": "sergioCaladoPJ@gmail.com",
                 "address": "Terreiro do chaço"}
    res = client.post("/users/", json=user_data)
    users.append(schemas.User(**res.json()))

    return users