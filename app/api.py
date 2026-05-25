from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
import sqlite3

from app.database import init_database, get_connection, create_listing, get_all_listings

app = FastAPI()

# ✅ 关键：添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（生产环境应该限制）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 服务静态文件
#app.mount("/static", StaticFiles(directory="static"), name="static")

# 将根路径指向 index.html
@app.get("/")
def read_root():
    return FileResponse("public/index.html")


# ✅ 新增：显式提供静态文件路由（CSS/JS）
@app.get("/static/{filename}")
def read_static(filename: str):
    return FileResponse(f"public/{filename}")

# ✅ 初始化数据库
init_database()

class Listing(BaseModel):
    id: int
    product_model: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)
    contact: str = Field(..., min_length=1)
    created_at: datetime


@app.post("/listings", status_code=201)
def create_listing_api(listing: Listing):
    with get_connection() as conn:
        try:
            result = create_listing(conn, listing.model_dump())
            return result
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="ID already exists"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )


@app.get("/listings")
def get_listings_api(
    product_model: Optional[str] = Query(default=None),
    min_price: Optional[int] = Query(default=None, ge=0, description="最低价格"),
    max_price: Optional[int] = Query(default=None, ge=0, description="最高价格"),
):
    with get_connection() as conn:
        listings = get_all_listings(
            conn,
            product_model_filter=product_model,
            min_price=min_price,
            max_price=max_price,
        )
        return listings
# 在文件最末尾添加以下内容：
# 这一行是 Vercel 的 Serverless Function 入口
#app = app