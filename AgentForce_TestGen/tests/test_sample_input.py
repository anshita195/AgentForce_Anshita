import pytest
import sample_input

def test_empty_cart():
    """unit: 
"""
    result = sample_input.calculate_discount([])
    assert result == 0.0

def test_no_discount():
    """unit: 
"""
    result = sample_input.calculate_discount([(10, 2), (5, 3)])
    assert result == 0.0

def test_discount_applied():
    """unit: 
"""
    result = sample_input.calculate_discount([(20, 3), (10, 5)])
    assert result == 11.0

def test_single_item_no_discount():
    """unit: 
"""
    result = sample_input.calculate_discount([(50, 1)])
    assert result == 0.0

def test_single_item_with_discount():
    """unit: 
"""
    result = sample_input.calculate_discount([(110, 1)])
    assert result == 11.0

def test_large_quantity_no_discount():
    """unit: 
"""
    result = sample_input.calculate_discount([(1, 99)])
    assert result == 0.0

def test_large_quantity_with_discount():
    """unit: 
"""
    result = sample_input.calculate_discount([(1, 101)])
    assert result == 10.1

def test_zero_price_item():
    """unit: 
"""
    result = sample_input.calculate_discount([(0, 1000)])
    assert result == 0.0

def test_zero_quantity_item():
    """unit: 
"""
    result = sample_input.calculate_discount([(1000, 0)])
    assert result == 0.0

def test_mixed_prices_and_quantities():
    """unit: 
"""
    result = sample_input.calculate_discount([(10, 5), (20, 2), (5, 10)])
    assert result == 14.0
