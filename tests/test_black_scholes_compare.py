"""Tests comparing binomial prices to Black-Scholes prices."""

from src.binomial import price_european_option_binomial
from src.black_scholes import call_price, put_price
from src.plots import build_convergence_data


def test_black_scholes_call_price_is_positive():
    """Test Black-Scholes call price is positive."""

    # Price option
    price = call_price(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    # Check price
    assert price > 0


def test_black_scholes_put_price_is_positive():
    """Test Black-Scholes put price is positive."""

    # Price option
    price = put_price(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    # Check price
    assert price > 0


def test_binomial_call_gets_close_to_black_scholes():
    """Test binomial call approaches Black-Scholes call."""

    # Binomial price
    binomial_price = price_european_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=500,
        option_type="call",
    )

    # Black-Scholes price
    black_scholes_price = call_price(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    # Check closeness
    assert abs(binomial_price - black_scholes_price) < 0.05


def test_binomial_put_gets_close_to_black_scholes():
    """Test binomial put approaches Black-Scholes put."""

    # Binomial price
    binomial_price = price_european_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=500,
        option_type="put",
    )

    # Black-Scholes price
    black_scholes_price = put_price(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
    )

    # Check closeness
    assert abs(binomial_price - black_scholes_price) < 0.05


def test_convergence_data_has_expected_rows():
    """Test convergence data returns expected rows."""

    # Build data
    rows = build_convergence_data(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        option_type="call",
    )

    # Check rows
    assert len(rows) == 7
    assert rows[0]["steps"] == 5
    assert rows[-1]["steps"] == 500