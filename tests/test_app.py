import pytest
from app import app, expenses


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        expenses.clear()
        yield client

    expenses.clear()


def test_health_route(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_add_expense(client):
    response = client.post(
        "/add",
        data={
            "description": "Lunch",
            "category": "Food",
            "amount": "150"
        }
    )

    assert response.status_code == 302
    assert len(expenses) == 1
    assert expenses[0]["description"] == "Lunch"
    assert expenses[0]["amount"] == 150.0


def test_invalid_expense_rejected(client):
    response = client.post(
        "/add",
        data={
            "description": "Test",
            "category": "Food",
            "amount": "-100"
        }
    )

    assert response.status_code == 400
    assert len(expenses) == 0


def test_api_expenses(client):
    expenses.append({
        "description": "Lunch",
        "category": "Food",
        "amount": 150.0
    })

    response = client.get("/api/expenses")

    assert response.status_code == 200
    assert response.json[0]["description"] == "Lunch"
    assert response.json[0]["amount"] == 150.0


def test_missing_description_rejected(client):
    response = client.post(
        "/add",
        data={
            "description": "",
            "category": "Food",
            "amount": "100"
        }
    )

    assert response.status_code == 400
    assert len(expenses) == 0


def test_non_numeric_amount_rejected(client):
    response = client.post(
        "/add",
        data={
            "description": "Lunch",
            "category": "Food",
            "amount": "abc"
        }
    )

    assert response.status_code == 400
    assert len(expenses) == 0
