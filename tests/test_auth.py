from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():

    response = client.post(
        "/auth/register",
        json={
            "nome": "Teste",
            "email": "teste@email.com",
            "senha": "123456",
            "role": "user"
        }
    )

    assert response.status_code in [200, 400]


def test_login():

    response = client.post(
        "/auth/login",
        data={
            "username": "teste@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body

def test_login_usuario_invalido():

    response = client.post(
        "/auth/login",
        data={
            "username": "naoexiste@email.com",
            "password": "12345"
        }
    )

    assert response.status_code == 401


def test_login_senha_invalida():

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@erp.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401