import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app
from app.database import get_connection, init_database

client = TestClient(app)


def test_price_filter():
    """验证价格区间过滤"""
    # 清空数据库
    init_database()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listings")
        conn.commit()

    # 准备测试数据
    test_data = [
        {
            "id": 1,
            "product_model": "iPhone 15",
            "price": 4500,
            "contact": "wx123",
            "created_at": "2026-05-21T00:00:00",
        },
        {
            "id": 2,
            "product_model": "MacBook Pro",
            "price": 12000,
            "contact": "qq456",
            "created_at": "2026-05-22T00:00:00",
        },
        {
            "id": 3,
            "product_model": "iPad Air",
            "price": 6000,
            "contact": "tel789",
            "created_at": "2026-05-23T00:00:00",
        },
    ]

    for item in test_data:
        client.post("/listings", json=item)

    # 测试 1：min_price
    response = client.get("/listings", params={"min_price": 5000})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # MacBook Pro(12000) + iPad Air(6000)
    assert all(item["price"] >= 5000 for item in data)

    # 测试 2：max_price
    response = client.get("/listings", params={"max_price": 10000})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # iPhone 15(4500) + iPad Air(6000)
    assert all(item["price"] <= 10000 for item in data)

    # 测试 3：区间
    response = client.get("/listings", params={"min_price": 5000, "max_price": 10000})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_model"] == "iPad Air"
    assert 5000 <= data[0]["price"] <= 10000

    # 测试 4：组合搜索
    response = client.get(
        "/listings",
        params={"product_model": "Pro", "min_price": 10000},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_model"] == "MacBook Pro"
    assert data[0]["price"] == 12000