import pytest
from pydantic import ValidationError
from main import StockChange, ProductIn

def test_stock_quantity_must_be_positive():
    with pytest.raises(ValidationError):
        StockChange(product_id=1, quantity=0, transaction_type="ISSUE")

def test_negative_price_is_rejected():
    with pytest.raises(ValidationError):
        ProductIn(sku="A1", name="Sample product", unit_price=-1)
