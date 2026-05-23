import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app, listings

client = TestClient(app)


def test_id_must_be_unique():
    listings.clear()

    # 第一条成功
    response1 = client.post(
        "/listings",
        json={
            "id": 1,
            "product_model": "iPhone 15",
            "price": 4500,
            "contact": "wx123",
            "created_at": "2026-05-21T00:00:00",
        },
    )
    assert response1.status_code == 201

    # 第二条 ID 重复
    response2 = client.post(
        "/listings",
        json={
            "id": 1,
            "product_model": "MacBook Pro",
            "price": 12000,
            "contact": "qq456",
            "created_at": "2026-05-22T00:00:00",
        },
    )

    assert response2.status_code == 400
    assert "ID already exists" in response2.text