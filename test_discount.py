import pytest
from discount_calculator import apply_discount

@pytest.mark.parametrize("input_amount, expected", [
    (999, 999),
    (1000, 950),
    (1001, 950.95),
    (4999, 4749.05),
    (5000, 4750),
    (5001, 5001)
])
def test_apply_discount(input_amount, expected):
    """
    Тестируем функцию apply_discount с различными значениями.
    """
    result = apply_discount(input_amount)
    assert result == expected, f"Ожидалось {expected}, но получено {result} для входа {input_amount}"