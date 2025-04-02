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
def medication_payload():
    return {
        "brand_name": "Xanax",
        "generic_name": "Alprazolam",
        "description": "For anxiety",
        "strength": "50mg",
        "dosage": 2,
        "dosage_form_id": 1,
        "medication_route_id": 1
    }


@pytest.fixture()
def medication_payload_updated():
    return {
        "brand_name": "Tetra",
        "generic_name": "Tetrahydrate",
        "description": "For pain",
        "strength": "10mg",
        "dosage": 1,
        "dosage_form_id": 4,
        "medication_route_id": 5
    }


def test_create_get_medication(test_client, user_payload, medication_payload):

    # # Create a user
    # response = test_client.post("/users/new", json=user_payload)
    # response_json = response.json()
    # assert response.status_code == 201
    # user_id = response_json["id"]
    #
    # # Inject user id into medication payload
    # medication_payload["user_id"] = user_id

    # Create a medication
    response = test_client.post("/medications/new", json=medication_payload)
    response_json = response.json()
    assert response.status_code == 201
    medication_id = response_json["id"]

    # Get the created medication
    response = test_client.get(f"/medications/{medication_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["brand_name"] == medication_payload["brand_name"]
    assert response_json["generic_name"] == medication_payload["generic_name"]
    assert response_json["description"] == medication_payload["description"]
    assert response_json["strength"] == medication_payload["strength"]
    assert response_json["dosage"] == medication_payload["dosage"]


def test_create_update_medication(test_client, user_payload, medication_payload, medication_payload_updated):
    # # Create a user
    # response = test_client.post("/users/new", json=user_payload)
    # response_json = response.json()
    # assert response.status_code == 201
    # user_id = response_json["id"]
    #
    # # Inject user id into medication payload
    # medication_payload["user_id"] = user_id

    # Create a medication
    response = test_client.post("/medications/new", json=medication_payload)
    response_json = response.json()
    assert response.status_code == 201
    medication_id = response_json["id"]

    # Update the medication
    response = test_client.put(f"/medications/{medication_id}", json=medication_payload_updated)
    response_json = response.json()
    print("RESPONSE ==> ", response_json)
    assert response.status_code == 201
    assert response_json["brand_name"] == medication_payload_updated["brand_name"]
    assert response_json["generic_name"] == medication_payload_updated["generic_name"]
    assert response_json["description"] == medication_payload_updated["description"]
    assert response_json["strength"] == medication_payload_updated["strength"]
    assert response_json["dosage"] == medication_payload_updated["dosage"]


def test_create_delete_medication(test_client, user_payload, medication_payload):
    # response = test_client.post("/users/new", json=user_payload)
    # response_json = response.json()
    # assert response.status_code == 201
    #
    # user_id = response_json["id"]
    # medication_payload["user_id"] = user_id

    # Create a medication
    response = test_client.post("/medications/new", json=medication_payload)
    response_json = response.json()
    assert response.status_code == 201
    medication_id = response_json["id"]

    # Delete the created medication
    response = test_client.delete(f"/medications/{medication_id}")
    response_json = response.json()
    assert response.status_code == 202
    assert response_json["message"] == "Medication deleted successfully"

    # Get the deleted medication
    response = test_client.get(f"/medications/{medication_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Medication does not exist"


def test_medication_not_found(test_client, new_id):
    response = test_client.get(f"/medications/{new_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Medication does not exist"


def test_create_medication_with_wrong_payload(test_client):
    response = test_client.post("/medications/new", json={})
    assert response.status_code == 422

