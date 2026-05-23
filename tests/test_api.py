import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app, listings  # ✅ 同时导入 listings

client = TestClient(app)


def test_create_listing():
    payload = {
        "id": 1,
        "product_model": "iPhone 15",
        "price": 4500,
        "contact": "wx123",
        "created_at": "2026-05-21T00:00:00"
    }

    response = client.post("/listings", json=payload)

    assert response.status_code == 201


def test_get_listings():
    # ✅ 关键：清空内存数据，保证测试独立
    listings.clear()

    payload = {
        "id": 1,
        "product_model": "iPhone 15",
        "price": 4500,
        "contact": "wx123",
        "created_at": "2026-05-21T00:00:00"
    }

    client.post("/listings", json=payload)

    response = client.get("/listings")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["product_model"] == "iPhone 15"