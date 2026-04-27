"""Black-Scholes pricing formulas for European options."""

import math


def _normal_cdf(value):
    """Calculate standard normal CDF."""

    # Normal CDF
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _calculate_d1(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
):
    """Calculate the Black-Scholes d1 value."""

    # Calculate d1
    numerator = math.log(stock_price / strike_price) + (
        risk_free_rate + 0.5 * volatility**2
    ) * time_to_maturity
    denominator = volatility * math.sqrt(time_to_maturity)

    return numerator / denominator


def _calculate_d2(d1, volatility, time_to_maturity):
    """Calculate the Black-Scholes d2 value."""

    # Calculate d2
    return d1 - volatility * math.sqrt(time_to_maturity)


def call_price(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
):
    """Price a European call option using Black-Scholes."""

    # Calculate values
    d1 = _calculate_d1(
        stock_price,
        strike_price,
        time_to_maturity,
        risk_free_rate,
        volatility,
    )
    d2 = _calculate_d2(d1, volatility, time_to_maturity)

    # Discount strike
    discounted_strike = strike_price * math.exp(-risk_free_rate * time_to_maturity)

    return stock_price * _normal_cdf(d1) - discounted_strike * _normal_cdf(d2)


def put_price(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
):
    """Price a European put option using Black-Scholes."""

    # Calculate values
    d1 = _calculate_d1(
        stock_price,
        strike_price,
        time_to_maturity,
        risk_free_rate,
        volatility,
    )
    d2 = _calculate_d2(d1, volatility, time_to_maturity)

    # Discount strike
    discounted_strike = strike_price * math.exp(-risk_free_rate * time_to_maturity)

    return discounted_strike * _normal_cdf(-d2) - stock_price * _normal_cdf(-d1)