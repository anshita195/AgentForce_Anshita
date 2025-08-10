import pytest
from examples import sample_input

def test_sample_input_1():
    # Test with input: []
    result = sample_input.calculate_discount([])
    assert result == pytest.approx(0.0)

def test_sample_input_2():
    # Test with input: [(10, 1)]
    result = sample_input.calculate_discount([(10, 1)])
    assert result == pytest.approx(0.0)

def test_sample_input_3():
    # Test with input: [(10, 1), (20, 1)]
    result = sample_input.calculate_discount([(10, 1), (20, 1)])
    assert result == pytest.approx(0.0)

def test_sample_input_4():
    # Test with input: [(50, 1), (60, 1)]
    result = sample_input.calculate_discount([(50, 1), (60, 1)])
    assert result == pytest.approx(11.0)

def test_sample_input_5():
    # Test with input: [(10, 5), (20, 3)]
    result = sample_input.calculate_discount([(10, 5), (20, 3)])
    assert result == pytest.approx(11.0)

def test_sample_input_6():
    # Test with input: [(10, 10), (5, 20)]
    result = sample_input.calculate_discount([(10, 10), (5, 20)])
    assert result == pytest.approx(20.0)

def test_sample_input_7():
    # Test with input: [(100, 1), (1, 1)]
    result = sample_input.calculate_discount([(100, 1), (1, 1)])
    assert result == pytest.approx(10.1)

def test_sample_input_8():
    # Test with input: [(1000, 1)]
    result = sample_input.calculate_discount([(1000, 1)])
    assert result == pytest.approx(100.0)

def test_sample_input_9():
    # Test with input: [(1, 1000)]
    result = sample_input.calculate_discount([(1, 1000)])
    assert result == pytest.approx(100.0)

def test_sample_input_10():
    # Test with input: [(0, 0)]
    result = sample_input.calculate_discount([(0, 0)])
    assert result == pytest.approx(0.0)

def test_sample_input_11():
    # Test with input: [(100.5, 1)]
    result = sample_input.calculate_discount([(100.5, 1)])
    assert result == pytest.approx(10.05)
