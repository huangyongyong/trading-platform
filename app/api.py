from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
import sqlite3
import os
from pathlib import Path

# 获取当前文件所在目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent  # 项目根目录

from app.database import init_database, get_connection, create_listing, get_all_listings

app = FastAPI()

# ✅ 恢复CORS支持（前端调用API必需）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 服务静态文件（app.js等）
# 将整个public目录挂载到根路径
app.mount("/", StaticFiles(directory=str(PROJECT_ROOT / "public")), name="public")

# ✅ 添加启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    try:
        init_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        # 不抛出异常，应用继续运行

# ✅ 根路径返回简单信息
# ✅ 根路径指向index.html
@app.get("/")
def read_root():
    """服务前端主页"""
    file_path = PROJECT_ROOT / "public" / "index.html"
    
    if not file_path.exists():
        return JSONResponse(
            status_code=404,
            content={"message": "Frontend not found", "detail": f"Expected file at {file_path}"}
        )
    
    return FileResponse(file_path)

# ✅ 显式提供app.js路由（可选，但更安全）
@app.get("/app.js")
def serve_app_js():
    """直接提供app.js文件"""
    file_path = PROJECT_ROOT / "public" / "app.js"
    if file_path.exists():
        return FileResponse(file_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js not found")

# ✅ 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "ok"}

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