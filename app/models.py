from datetime import datetime
from pydantic import BaseModel, Field


class Listing(BaseModel):
    id: int
    product_model: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)  # ✅ 自动拒绝 <= 0
    contact: str = Field(..., min_length=1)
    created_at: datetime