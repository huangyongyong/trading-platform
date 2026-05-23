import pytest
from datetime import datetime
# 关键：从 app.models 导入 Listing
from pydantic import ValidationError
from app.models import Listing 

def test_listing_rejects_invalid_price():
    with pytest.raises(ValidationError):
        Listing(
            id=2,
            product_model="Xiaomi 14",
            price=-100,   # ❌ 非法
            contact="qq456",
            created_at=datetime(2026, 5, 21)
        )

def test_listing_accepts_valid_data():
    from datetime import datetime

    listing = Listing(
        id=1,
        product_model="iPhone 15",
        price=4500,
        contact="wx123",
        created_at=datetime(2026, 5, 21)
    )

    assert listing.price == 4500
    assert listing.product_model == "iPhone 15"