# test_calculator_pytest.py
import pytest
from calculator import apply_discount

def test_standard_discount():
    # No self.assertEqual! Just plain Python math comparison.
    assert apply_discount(100, 20) == 80

def test_zero_discount():
    assert apply_discount(50, 0) == 50

def test_invalid_discount_raises_error():
    # PyTest uses a simpler context manager syntax
    with pytest.raises(ValueError):
        apply_discount(100, -5)