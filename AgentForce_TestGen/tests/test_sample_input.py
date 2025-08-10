import pytest
from examples import sample_input

def test_sample_input_1():
    # Test with input: []
    result = sample_input.calculate_discount([])
    assert result == pytest.approx(0.0)

def test_sample_input_2():
    # Test with input: [(10, 1), (20, 1), (30, 1)]
    result = sample_input.calculate_discount([(10, 1), (20, 1), (30, 1)])
    assert result == pytest.approx(0.0)

def test_sample_input_3():
    # Test with input: [(10, 2), (20, 3), (30, 4)]
    result = sample_input.calculate_discount([(10, 2), (20, 3), (30, 4)])
    assert result == pytest.approx(20.0)

def test_sample_input_4():
    # Test with input: [(100, 1), (1, 1)]
    result = sample_input.calculate_discount([(100, 1), (1, 1)])
    assert result == pytest.approx(10.1)

def test_sample_input_5():
    # Test with input: [(10, 0), (20, 0), (30, 0)]
    result = sample_input.calculate_discount([(10, 0), (20, 0), (30, 0)])
    assert result == pytest.approx(0.0)

def test_sample_input_6():
    # Test with input: [(1000, 1)]
    result = sample_input.calculate_discount([(1000, 1)])
    assert result == pytest.approx(100.0)

def test_sample_input_7():
    # Test with input: [(100, 0.5)]
    result = sample_input.calculate_discount([(100, 0.5)])
    assert result == pytest.approx(0.0)

def test_sample_input_8():
    # Test with input: [(100, 1.5)]
    result = sample_input.calculate_discount([(100, 1.5)])
    assert result == pytest.approx(15.0)
