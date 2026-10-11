
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page_opens(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_page_opens(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_admin_redirects_to_login(client):
    response = client.get("/admin")
    assert response.status_code == 302
    assert "/login" in response.location


def test_order_rejects_empty_fields(client):
    response = client.post(
        "/order",
        data={
            "name": "",
            "phone": "",
            "message": ""
        }
    )
    assert response.status_code == 400

def test_order_rejects_invalid_phone(client):
    response = client.post(
        "/order",
        data={
            "name": "Тест",
            "phone": "123",
            "message": "Тестовый заказ"
        }
    )
    assert response.status_code == 400




def test_login_rejects_wrong_password(client):
    response = client.get("/login")
    assert response.status_code == 200

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.data, "html.parser")
    token_input = soup.find("input", {"name": "csrf_token"})

    assert token_input is not None

    response = client.post(
        "/login",
        data={
            "password": "definitely-wrong-password",
            "csrf_token": token_input["value"]
        }
    )

    assert response.status_code == 401



def test_order_requires_csrf_token(client):
    response = client.post(
        "/order",
        data={
            "name": "Тест",
            "phone": "77012345678",
            "message": "Тестовый заказ"
        }
    )
    assert response.status_code == 400
    assert b"CSRF" in response.data or b"csrf" in response.data

