from fastapi.testclient import TestClient

import main


client = TestClient(main.application)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_loan_endpoint():
    r = client.post(
        "/finance/loan",
        json={
            "principal": 1000,
            "annual_rate": 5,
            "years": 1,
            "payments_per_year": 12,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "payment" in data
    assert "total" in data


def test_compound_interest_endpoint():
    r = client.post(
        "/finance/compound-interest",
        json={
            "principal": 1000,
            "annual_rate": 5,
            "periods_per_year": 4,
            "years": 3,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "future_value" in data


def test_npv_endpoint():
    r = client.post(
        "/finance/npv",
        json={
            "rate": 0.05,
            "cash_flows": [-1000, 200, 300, 400, 500],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "npv" in data


def test_irr_endpoint():
    r = client.post(
        "/finance/irr",
        json={
            "cash_flows": [-1000, 200, 300, 400, 500],
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "irr" in data
