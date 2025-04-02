import pytest
import pendulum


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
        "brand_name": "Tetra",
        "generic_name": "Tetrahydrate",
        "description": "For pain",
        "strength": "10mg",
        "dosage": 1,
        "dosage_form_id": 4,
        "medication_route_id": 5
    }


@pytest.fixture()
def schedule_payload():
    return {
        "begin_date": pendulum.now(tz="UTC").strftime("%Y-%m-%d"),
        "end_date": None,
        "begin_time": pendulum.now(tz="UTC").strftime("%H:%M:%S"),
        "end_time": None,
        "schedule_type": "medication",
        "repeated": "hourly",
        "repetition_step": 1,
        "repeated_monthly_on": None,
        "repeated_until": "forever",
        "repeated_until_date": None,
        "repeated_reps": None,
        "medicaiton_id": "",
        "appointment_id": None,
    }

@pytest.fixture()
def schedule_payload_updated():
    return {
        "begin_date": pendulum.now().to_iso8601_string(),
        "end_date": None,
        "begin_time": pendulum.now().to_iso8601_string(),
        "end_time": None,
        "schedule_type": "medication",
        "repeated": "daily",
        "repetition_step": 2,
        "repeated_monthly_on": None,
        "repeated_until": "forever",
        "repeated_until_date": None,
        "repeated_reps": None,
        "medicaiton_id": "",
        "appointment_id": None,
    }


def test_create_get_schedules(test_client, user_payload, medication_payload, schedule_payload):

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

    # Inject ids into schedule
    # schedule_payload["user_id"] = user_id
    schedule_payload["medication_id"] = medication_id


    # Create a schedule
    response = test_client.post("/schedules/new", json=schedule_payload)
    response_json = response.json()
    print("SCHEDULE ==>", response_json)
    assert response.status_code == 201
    schedule_id = response_json["id"]


    # Get the created schedule
    response = test_client.get(f"/schedules/{schedule_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["begin_date"] == schedule_payload["begin_date"]
    assert response_json["end_date"] == schedule_payload["end_date"]
    assert response_json["begin_time"] == schedule_payload["begin_time"]
    assert response_json["end_time"] == schedule_payload["end_time"]
    assert response_json["schedule_type"] == schedule_payload["schedule_type"]
    assert response_json["repeated"] == schedule_payload["repeated"]
    assert response_json["repetition_step"] == schedule_payload["repetition_step"]
    assert response_json["repeated_monthly_on"] == schedule_payload["repeated_monthly_on"]
    assert response_json["repeated_until"] == schedule_payload["repeated_until"]
    assert response_json["repeated_until_date"] == schedule_payload["repeated_until_date"]
    assert response_json["repeated_reps"] == schedule_payload["repeated_reps"]
    # assert response_json["user_id"] == schedule_payload["user_id"]
    assert response_json["medication_id"] == schedule_payload["medication_id"]
    assert response_json["appointment_id"] == schedule_payload["appointment_id"]

    # Get the created slot
    response = test_client.get(f"/adherence/next")
    assert response.status_code == 200
    response_json = response.json()
    print("SCHEDULE ==>", response_json)
    assert response_json["schedule_id"] == schedule_id
    assert response_json["repeated"] == schedule_payload["repeated"]
    assert response_json["repetition_step"] == schedule_payload["repetition_step"]
    assert response_json["repeated_monthly_on"] == schedule_payload["repeated_monthly_on"]


# def test_next_adherence_slot(test_client, schedule_payload):
#     # Get the created slot
#     response = test_client.get(f"/adherence/next")
#     assert response.status_code == 200
#     response_json = response.json()
#     print("SCHEDULE ==>", response_json)
#     assert response_json["date"] == schedule_payload["begin_date"]
#     assert response_json["time"] == schedule_payload["begin_time"]
#     assert response_json["repeated"] == schedule_payload["repeated"]
#     assert response_json["repetition_step"] == schedule_payload["repetition_step"]
#     assert response_json["repeated_monthly_on"] == schedule_payload["repeated_monthly_on"]



# def test_create_update_medication(test_client, user_payload, medication_payload, medication_payload_updated):
#     # create a user
#     response = test_client.post("/users/new", json=user_payload)
#     response_json = response.json()
#     assert response.status_code == 201
#     user_id = response_json["id"]
#
#     # Inject user id into medication payload
#     medication_payload["user_id"] = user_id
#
#     # Create a medication
#     response = test_client.post("/medications/new", json=medication_payload)
#     response_json = response.json()
#     assert response.status_code == 201
#     medication_id = response_json["id"]
#
#     # Update the medication
#     response = test_client.put(f"/medications/{medication_id}", json=medication_payload_updated)
#     assert response.status_code == 201
#     response_json = response.json()
#     print("RESPONSE ==> ", response_json)
#     assert response_json["brand_name"] == medication_payload_updated["brand_name"]
#     assert response_json["generic_name"] == medication_payload_updated["generic_name"]
#     assert response_json["description"] == medication_payload_updated["description"]
#     assert response_json["strength"] == medication_payload_updated["strength"]
#     assert response_json["dosage"] == medication_payload_updated["dosage"]
#     assert response_json["dosage_form_id"] == medication_payload_updated["dosage_form_id"]
#     assert response_json["medication_route_id"] == medication_payload_updated["medication_route_id"]
#
#
# def test_create_delete_medication(test_client, user_payload, medication_payload):
#     response = test_client.post("/users/new", json=user_payload)
#     response_json = response.json()
#     assert response.status_code == 201
#
#     user_id = response_json["id"]
#     medication_payload["user_id"] = user_id
#
#     # Create a medication
#     response = test_client.post("/medications/new", json=medication_payload)
#     response_json = response.json()
#     assert response.status_code == 201
#     medication_id = response_json["id"]
#
#     # Delete the created medication
#     response = test_client.delete(f"/medications/{medication_id}")
#     response_json = response.json()
#     assert response.status_code == 202
#     assert response_json["message"] == "Medication deleted successfully"
#
#     # Get the deleted medication
#     response = test_client.get(f"/medications/{medication_id}")
#     assert response.status_code == 404
#     response_json = response.json()
#     assert response_json["detail"] == "Medication does not exist"
#
#
# def test_medication_not_found(test_client, new_id):
#     response = test_client.get(f"/medications/{new_id}")
#     assert response.status_code == 404
#     response_json = response.json()
#     assert response_json["detail"] == "Medication does not exist"
#
#
# def test_create_medication_with_wrong_payload(test_client):
#     response = test_client.post("/medications/new", json={})
#     assert response.status_code == 422
#
