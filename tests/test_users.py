from src import schemas
from fastapi.testclient import TestClient
from fastapi import status
import pytest


def test_createUserValid(client: TestClient):
    # Arrange
    post_body = {"name": "joao",
                 "email": "joao@gmail.com",
                 "address": "myaddress"}
    # Act
    res = client.post("/users/", json=post_body)

    # Assert
    new_user = schemas.User(**res.json())
    assert new_user.email == "joao@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED

def test_create_user_alreadyRegisteredEmail(test_user: schemas.User, client: TestClient):
    # Arrange
    post_body = {"name": "joao",
                 "email": test_user.email,
                 "address": "myaddress"}

    # Act
    res = client.post("/users/", json=post_body)

    # Assert
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.json().get("detail") == "Email already registered"

@pytest.mark.parametrize(
    "skip, limit, total", [
        (1, 2, 2),
        (0, 3, 3),
    ])
def test_read_users_shouldGetUsers(test_users: list[schemas.User], client: TestClient,
                                   skip: int, limit: int, total: int):
    # Act
    res = client.get(
        "/users/", params={"skip": str(skip), "limit": str(limit)})

    # Assert
    schemas.User(**res.json()[0])
    assert len(res.json()) == total
    assert res.status_code == status.HTTP_200_OK

def test_read_user_shouldGetUser(test_users: list[schemas.User], client: TestClient):
    # Arrange
    test_user = test_users[-1]
    id = test_user.id

    # Act
    res = client.get(f"/users/{id}")

    # Assert
    resp_user = schemas.User(**res.json())
    assert resp_user.id == test_user.id
    assert res.status_code == status.HTTP_200_OK

def test_read_user_userNotFound(test_user: schemas.User, client: TestClient):
    # Arrange
    id = test_user.id + 100

    # Act
    res = client.get(f"/users/{id}")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_update_user_shouldUpdate(test_user: schemas.User, client: TestClient):
    # Arrange
    id = test_user.id
    put_body = {"name": "newName",
                 "email": "newEmail@gmail.com",
                 "address": "newAddress"}
    # Act
    res = client.put(f"/users/{id}", json=put_body)

    #Assert
    updated_user = schemas.User(**res.json())
    assert updated_user.name == put_body["name"]
    assert updated_user.email == put_body["email"]
    assert updated_user.address == put_body["address"]
    assert res.status_code == status.HTTP_200_OK

def test_update_user_notFound(test_user: schemas.User, client: TestClient):
    # Arrange
    id = test_user.id + 100

    # Act
    res = client.get(f"/users/{id}")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_shouldDelete(test_user: schemas.User, client: TestClient):
    # Arrange
    id = test_user.id

    # Act
    res = client.delete(f"/users/{id}")

    #Assert
    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_delete_user_notFound(test_user: schemas.User, client: TestClient):
    # Arrange
    id = test_user.id + 100

    # Act
    res = client.delete(f"/users/{id}")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND