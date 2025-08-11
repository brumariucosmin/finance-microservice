import pytest

from app.services.finance import calculate_loan
from app.services.finance import compound_interest
from app.services.finance import npv
from app.services.finance import irr


def test_calculate_loan_zero_rate():
    payment, total = calculate_loan(1200, 0, 1, 12)
    assert pytest.approx(payment, rel=1e-2) == 100
    assert pytest.approx(total, rel=1e-2) == 1200


def test_compound_interest():
    fv = compound_interest(100, 10, 1, 2)
    assert pytest.approx(fv, rel=1e-6) == 121


def test_npv_simple():
    cash_flows = [-100, 60, 60, 60]
    result = npv(0.1, cash_flows)
    expected = sum(
        cf / ((1 + 0.1) ** i)
        for i, cf in enumerate(cash_flows)
    )
    assert pytest.approx(result, rel=1e-6) == expected


def test_irr_simple():
    rate = irr([-100, 35, 50, 40])
    # IRR aproximat ~11.76%
    assert pytest.approx(rate, rel=1e-2) == pytest.approx(0.1176, rel=1e-2)
