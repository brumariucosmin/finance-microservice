from functools import lru_cache
from typing import List, Tuple


def calculate_loan(
    principal: float,
    annual_rate: float,
    years: int,
    payments_per_year: int,
) -> Tuple[float, float]:
    """
    Returnează (payment_per_period, total_payment).
    """
    n = years * payments_per_year

    if annual_rate == 0:
        # zero interest → principal evenly over n payments
        payment = principal / n
        total = principal
        return payment, total

    rate_per_period = annual_rate / 100 / payments_per_year
    payment = principal * rate_per_period / (
        1 - (1 + rate_per_period) ** -n
    )
    total = payment * n

    return payment, total


@lru_cache(maxsize=128)
def compound_interest(
    principal: float,
    annual_rate: float,
    periods_per_year: int,
    years: float,
) -> float:
    """
    Calculează dobânda compusă:
    A = P * (1 + r/n)^(n*t)
    """
    r = annual_rate / 100
    return principal * (1 + r / periods_per_year) ** (
        periods_per_year * years
    )


def npv(
    rate: float,
    cash_flows: List[float],
) -> float:
    """
    Calculează Net Present Value:
    sum(cf / (1 + rate)^i)
    """
    return sum(
        cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows)
    )


def irr(
    cash_flows: List[float],
    iterations: int = 50,
) -> float:
    """
    Newton–Raphson pentru IRR.
    """
    guess = 0.1

    for _ in range(iterations):
        f = sum(
            cf / ((1 + guess) ** i)
            for i, cf in enumerate(cash_flows)
        )
        df = sum(
            -i * cf / ((1 + guess) ** (i + 1))
            for i, cf in enumerate(cash_flows)
        )
        guess -= f / df

    return guess
