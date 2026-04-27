"""Plot helpers for the binomial option pricer."""

import matplotlib.pyplot as plt

from src.binomial import price_option_binomial
from src.black_scholes import call_price, put_price


def build_convergence_data(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
    option_type,
    step_values=None,
):
    """Build binomial convergence data against Black-Scholes."""

    # Default steps
    if step_values is None:
        step_values = [5, 10, 25, 50, 100, 250, 500]

    # Black-Scholes price
    if option_type == "call":
        black_scholes_price = call_price(
            stock_price,
            strike_price,
            time_to_maturity,
            risk_free_rate,
            volatility,
        )
    else:
        black_scholes_price = put_price(
            stock_price,
            strike_price,
            time_to_maturity,
            risk_free_rate,
            volatility,
        )

    # Build rows
    rows = []

    for steps in step_values:
        binomial_price = price_option_binomial(
            stock_price=stock_price,
            strike_price=strike_price,
            time_to_maturity=time_to_maturity,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            steps=steps,
            option_type=option_type,
            exercise_style="european",
        )

        rows.append(
            {
                "steps": steps,
                "binomial_price": binomial_price,
                "black_scholes_price": black_scholes_price,
                "absolute_difference": abs(binomial_price - black_scholes_price),
            }
        )

    return rows


def create_convergence_plot(convergence_data):
    """Create a convergence chart for binomial prices."""

    # Extract values
    steps = [row["steps"] for row in convergence_data]
    binomial_prices = [row["binomial_price"] for row in convergence_data]
    black_scholes_price = convergence_data[0]["black_scholes_price"]

    # Create chart
    fig, ax = plt.subplots()
    ax.plot(steps, binomial_prices, marker="o", label="Binomial Price")
    ax.axhline(
        black_scholes_price,
        linestyle="--",
        label="Black-Scholes Price",
    )

    # Label chart
    ax.set_xlabel("Number of Steps")
    ax.set_ylabel("Option Price")
    ax.set_title("Binomial Convergence to Black-Scholes")
    ax.legend()
    ax.grid(True)

    return fig