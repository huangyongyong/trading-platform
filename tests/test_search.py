import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app, listings

client = TestClient(app)


def test_search_listings_by_product_model():
    # ✅ 清空内存，保证测试独立
    listings.clear()

    # 准备测试数据
    client.post(
        "/listings",
        json={
            "id": 1,
            "product_model": "iPhone 15",
            "price": 4500,
            "contact": "wx123",
            "created_at": "2026-05-21T00:00:00",
        },
    )

    client.post(
        "/listings",
        json={
            "id": 2,
            "product_model": "MacBook Pro",
            "price": 12000,
            "contact": "qq456",
            "created_at": "2026-05-22T00:00:00",
        },
    )

    # 搜索
    #response = client.get("/listings?product_model=iPhone")
    response = client.get(
        "/listings",
        params={"product_model": "iPhone"}
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["product_model"] == "iPhone 15"