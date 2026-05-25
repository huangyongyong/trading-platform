import os
import tempfile

import sqlite3
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

if os.environ.get("VERCEL"):
    # Vercel环境：使用 /tmp 目录
    DB_PATH = os.path.join("/tmp", "listings.db")
else:
    # 本地开发环境：使用当前目录
    DB_PATH = os.path.join(os.path.dirname(__file__), "listings.db")

# 数据库文件路径
#DB_PATH = "listings.db"


def init_database():
    """初始化数据库表"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY,
                product_model TEXT NOT NULL,
                price INTEGER NOT NULL,
                contact TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        """)
        conn.commit()


@contextmanager
def get_connection():
    """获取数据库连接（上下文管理器）"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_listing(conn, listing_data: Dict[str, Any]) -> Dict[str, Any]:
    """创建报价单"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO listings (id, product_model, price, contact, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        listing_data["id"],
        listing_data["product_model"],
        listing_data["price"],
        listing_data["contact"],
        listing_data["created_at"],
    ))
    conn.commit()
    return dict(listing_data)


def get_all_listings(
    conn,
    product_model_filter: Optional[str] = None,
    min_price: Optional[int] = None,   # ✅ 必须有这个参数
    max_price: Optional[int] = None,   # ✅ 必须有这个参数
) -> List[Dict]:
    """查询报价单，支持多重过滤"""
    cursor = conn.cursor()

    # 基础 SQL
    sql = "SELECT * FROM listings WHERE 1=1"
    params = []

    # 产品型号过滤
    if product_model_filter:
        sql += " AND LOWER(product_model) LIKE ?"
        params.append(f"%{product_model_filter.lower()}%")

    # 最低价过滤
    if min_price is not None:    # ✅ 必须是 is not None
        sql += " AND price >= ?"
        params.append(min_price)

    # 最高价过滤
    if max_price is not None:    # ✅ 必须是 is not None
        sql += " AND price <= ?"
        params.append(max_price)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]