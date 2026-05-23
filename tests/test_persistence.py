import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sqlite3
import os
import time

from app.main import app
from app.database import get_connection, init_database  # ✅ 只导入可用的

client = TestClient(app)


def test_listing_persists_across_requests():
    """验证数据在多次请求间持久化"""
    # ✅ 不依赖 DB_PATH
    init_database()  # 确保表存在

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listings")
        conn.commit()

    # 创建第一条
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

    # 验证数据库
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM listings")
        count = cursor.fetchone()[0]

    assert count == 1


def test_id_uniqueness_enforced_by_database():
    """验证数据库层面的 ID 唯一约束"""
    init_database()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM listings")
        conn.commit()

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

    # 第二条 ID 重复，应该失败
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
    # 可能是 400（应用层）或 500（数据库异常）
    assert response2.status_code in (400, 500)
    assert "ID already exists" in response2.text