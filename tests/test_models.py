import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models import Listing


def test_listing_accepts_valid_data():
    data = {
        "id": 1,
        "product_model": "iPhone 15",
        "price": 4500,
        "contact": "wx123",
        "created_at": datetime(2026, 5, 21),
    }

    listing = Listing(**data)

    assert listing.product_model == "iPhone 15"
    assert listing.price == 4500


def test_listing_requires_all_fields():
    with pytest.raises(ValidationError):
        Listing(
            id=3,
            product_model="华为 P70"
            # ❌ 缺 price / contact / created_at
        )