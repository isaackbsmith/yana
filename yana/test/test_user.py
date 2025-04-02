import pytest


@pytest.fixture()
def user_payload():
    """Generate a user payload"""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@doe.com",
        "phone_number": "0558234782",
        "user_type": "primary",
        "gender": "male",
        "password": "abcdefgh"
    }


@pytest.fixture()
def user_payload_updated():
    """Generate an updated user payload"""
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@doe.com",
        "phone_number": "0558234782",
        "user_type": "primary",
        "gender": "female",
    }


def test_create_get_user(test_client, user_payload):
    response = test_client.post("/users/new", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    user_id = response_json["id"]

    # Get the created user
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["first_name"] == user_payload["first_name"]
    assert response_json["last_name"] == user_payload["last_name"]
    assert response_json["gender"] == user_payload["gender"]
    assert response_json["email"] == user_payload["email"]
    assert response_json["phone_number"] == user_payload["phone_number"]
    assert response_json["user_type"] == user_payload["user_type"]


def test_create_update_user(test_client, user_payload, user_payload_updated):
    response = test_client.post("/users/new", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    user_id = response_json["id"]

    # Update the current user
    response = test_client.put(f"/users/{user_id}", json=user_payload_updated)
    response_json = response.json()
    print("RESPONSE ==> ", response_json)
    assert response.status_code == 201
    assert response_json["first_name"] == user_payload_updated["first_name"]
    assert response_json["last_name"] == user_payload_updated["last_name"]
    assert response_json["gender"] == user_payload_updated["gender"]
    assert response_json["email"] == user_payload_updated["email"]
    assert response_json["phone_number"] == user_payload_updated["phone_number"]
    assert response_json["user_type"] == user_payload_updated["user_type"]


def test_create_delete_user(test_client, user_payload):
    response = test_client.post("/users/new", json=user_payload)
    response_json = response.json()
    assert response.status_code == 201

    user_id = response_json["id"]

    # Delete the created user
    response = test_client.delete(f"/users/{user_id}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["message"] == "User deleted successfully"

    # Get the deleted user
    response = test_client.get(f"/users/{user_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "User does not exist"


def test_user_not_found(test_client, new_id):
    response = test_client.get(f"/users/{new_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "User does not exist"


def test_create_user_with_wrong_payload(test_client):
    response = test_client.post("/users/new", json={})
    assert response.status_code == 422

