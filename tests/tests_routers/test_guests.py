import pytest


def test_current_user(client):
    response = client.get("/guests/current_user?guest_uuid=nonexistent_uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Guest not found"}

    response = client.get("/guests/current_user")
    assert response.status_code == 404
    assert response.json() == {"detail": "Guest not found"}


def test_create_user(client):
    response = client.post("/guests/create", json={"name": 'test_name'})
    assert response.status_code == 200
    assert response.json()['name'] == 'test_name'
    assert 'id' in response.json().keys()


@pytest.mark.parametrize('user_id, expected', [
    (5, 'test_name'),
    (6, 'test_name'),
    (7, 'test_name'),
    (1, 'string'),
])
def test_get_user(client, user_id, expected):
    response = client.get(f"/guests/{user_id}")
    assert response.status_code == 200
    assert response.json()['name'] == expected


@pytest.mark.parametrize('user_id, expected, code', [
    (5000000, "Guest with id 5000000 not found", 404),
    (0, "Guest with id 0 not found", 404),
    (-1, "Guest with id -1 not found", 404),

])
def test_bad_get_user(client, user_id, expected, code):
    response = client.get(f"/guests/{user_id}")
    assert response.status_code == code
    assert response.json() == {"detail": expected}


def test_bad_422_get_user(client):
    response = client.get("/guests/test")
    assert response.status_code == 422
