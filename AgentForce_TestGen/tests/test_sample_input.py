import pytest
from examples import sample_input


@pytest.mark.parametrize('input_value,expected', [
    ([], 0.0)  # empty list returns zero,
    ([(50, 1)], 0.0)  # below threshold,
    ([(60, 2)], pytest.approx(12.0))  # above threshold
])
def test_basic_scenarios(input_value, expected):
    '''Test various input scenarios'''
    result = sample_input.calculate_discount(input_value)
    assert result == expected


def test_exact_threshold():
    '''total exactly 100 should give no discount'''
    result = sample_input.calculate_discount([(50, 2)])
    assert result == 0.0


@pytest.mark.slow
def test_performance():
    '''Test with large cart'''
    large_input = [(1.0, 1)] * 100000
    result = sample_input.calculate_discount(large_input)
    assert result == pytest.approx(100000 * 0.1)

