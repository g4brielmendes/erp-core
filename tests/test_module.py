from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@erp.com",
            "password": "12345"
        }
    )

    return response.json()["access_token"]


def test_create_module():

    token = get_token()

    response = client.post(
        "/modules/",
        json={
            "nome": "financeiro",
            "url": "http://localhost",
            "porta": 8001
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_list_modules():

    token = get_token()

    response = client.get(
        "/modules/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200