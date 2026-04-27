"""Tests for the binomial option pricer."""

from src.binomial import (
    price_american_option_binomial,
    price_european_option_binomial,
    price_option_binomial,
)


def test_european_call_price_is_positive():
    """Test European call price is positive."""

    # Price option
    price = price_european_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=100,
        option_type="call",
    )

    # Check price
    assert price > 0


def test_european_put_price_is_positive():
    """Test European put price is positive."""

    # Price option
    price = price_european_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=100,
        option_type="put",
    )

    # Check price
    assert price > 0


def test_american_put_is_at_least_european_put():
    """Test American put is at least European put."""

    # European put
    european_price = price_european_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=100,
        option_type="put",
    )

    # American put
    american_price = price_american_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=100,
        option_type="put",
    )

    # Compare prices
    assert american_price >= european_price


def test_general_function_returns_float():
    """Test general pricing function returns a float."""

    # Price option
    price = price_option_binomial(
        stock_price=100,
        strike_price=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.20,
        steps=10,
        option_type="call",
        exercise_style="european",
    )

    # Check type
    assert isinstance(price, float)


def test_invalid_option_type_raises_error():
    """Test invalid option type raises error."""

    # Check error
    try:
        price_option_binomial(
            stock_price=100,
            strike_price=100,
            time_to_maturity=1,
            risk_free_rate=0.05,
            volatility=0.20,
            steps=10,
            option_type="bad",
            exercise_style="european",
        )
    except ValueError as error:
        assert "Option type" in str(error)