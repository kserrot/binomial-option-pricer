"""Binomial option pricing logic."""

import math


def price_option_binomial(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
    steps,
    option_type="call",
    exercise_style="european",
):
    """Price an option using the Cox-Ross-Rubinstein binomial model."""

    # Validate inputs
    if stock_price <= 0:
        raise ValueError("Stock price must be positive.")

    if strike_price <= 0:
        raise ValueError("Strike price must be positive.")

    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")

    if volatility <= 0:
        raise ValueError("Volatility must be positive.")

    if steps <= 0:
        raise ValueError("Steps must be positive.")

    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")

    if exercise_style not in ["european", "american"]:
        raise ValueError("Exercise style must be 'european' or 'american'.")

    # Time step
    dt = time_to_maturity / steps

    # Up/down factors
    up_factor = math.exp(volatility * math.sqrt(dt))
    down_factor = 1 / up_factor

    # Growth factor
    growth_factor = math.exp(risk_free_rate * dt)

    # Risk-neutral probability
    probability = (growth_factor - down_factor) / (up_factor - down_factor)

    # Validate probability
    if probability < 0 or probability > 1:
        raise ValueError(
            "Invalid risk-neutral probability. Check input assumptions."
        )

    # Discount factor
    discount_factor = math.exp(-risk_free_rate * dt)

    # Build stock prices
    stock_prices = []

    for i in range(steps + 1):
        # Terminal price
        price = stock_price * (up_factor ** i) * (down_factor ** (steps - i))
        stock_prices.append(price)

    # Terminal option values
    option_values = []

    for price in stock_prices:
        # Call payoff
        if option_type == "call":
            payoff = max(price - strike_price, 0)

        # Put payoff
        else:
            payoff = max(strike_price - price, 0)

        option_values.append(payoff)

    # Work backward
    for step in range(steps - 1, -1, -1):
        new_values = []

        for i in range(step + 1):
            # Continuation value
            continuation_value = discount_factor * (
                probability * option_values[i + 1]
                + (1 - probability) * option_values[i]
            )

            # Current stock price
            current_stock_price = (
                stock_price * (up_factor ** i) * (down_factor ** (step - i))
            )

            # Intrinsic value
            if option_type == "call":
                intrinsic_value = max(current_stock_price - strike_price, 0)
            else:
                intrinsic_value = max(strike_price - current_stock_price, 0)

            # American exercise
            if exercise_style == "american":
                option_value = max(intrinsic_value, continuation_value)

            # European exercise
            else:
                option_value = continuation_value

            new_values.append(option_value)

        option_values = new_values

    # Final option price
    return option_values[0]

def build_stock_price_tree(
    stock_price,
    time_to_maturity,
    volatility,
    steps,
):
    """Build a stock price tree for display."""

    # Validate inputs
    if stock_price <= 0:
        raise ValueError("Stock price must be positive.")

    if time_to_maturity <= 0:
        raise ValueError("Time to maturity must be positive.")

    if volatility <= 0:
        raise ValueError("Volatility must be positive.")

    if steps <= 0:
        raise ValueError("Steps must be positive.")

    # Time step
    dt = time_to_maturity / steps

    # Up/down factors
    up_factor = math.exp(volatility * math.sqrt(dt))
    down_factor = 1 / up_factor

    # Build tree
    tree = []

    for step in range(steps + 1):
        row = []

        for up_moves in range(step + 1):
            # Calculate price
            price = stock_price * (up_factor ** up_moves) * (
                down_factor ** (step - up_moves)
            )
            row.append(round(price, 4))

        # Pad row
        while len(row) < steps + 1:
            row.append(None)

        tree.append(row)

    return tree


def build_option_value_tree(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
    steps,
    option_type="call",
    exercise_style="european",
):
    """Build an option value tree for display."""

    # Validate inputs
    if option_type not in ["call", "put"]:
        raise ValueError("Option type must be 'call' or 'put'.")

    if exercise_style not in ["european", "american"]:
        raise ValueError("Exercise style must be 'european' or 'american'.")

    # Time step
    dt = time_to_maturity / steps

    # Up/down factors
    up_factor = math.exp(volatility * math.sqrt(dt))
    down_factor = 1 / up_factor

    # Risk-neutral probability
    growth_factor = math.exp(risk_free_rate * dt)
    probability = (growth_factor - down_factor) / (up_factor - down_factor)
    discount_factor = math.exp(-risk_free_rate * dt)

    # Terminal values
    option_values = []

    for up_moves in range(steps + 1):
        # Terminal stock price
        terminal_stock_price = stock_price * (up_factor ** up_moves) * (
            down_factor ** (steps - up_moves)
        )

        # Terminal payoff
        if option_type == "call":
            payoff = max(terminal_stock_price - strike_price, 0)
        else:
            payoff = max(strike_price - terminal_stock_price, 0)

        option_values.append(payoff)

    # Store tree rows
    tree = [[round(value, 4) for value in option_values]]

    # Work backward
    for step in range(steps - 1, -1, -1):
        new_values = []

        for up_moves in range(step + 1):
            # Continuation value
            continuation_value = discount_factor * (
                probability * option_values[up_moves + 1]
                + (1 - probability) * option_values[up_moves]
            )

            # Current stock price
            current_stock_price = stock_price * (up_factor ** up_moves) * (
                down_factor ** (step - up_moves)
            )

            # Intrinsic value
            if option_type == "call":
                intrinsic_value = max(current_stock_price - strike_price, 0)
            else:
                intrinsic_value = max(strike_price - current_stock_price, 0)

            # Exercise style
            if exercise_style == "american":
                option_value = max(intrinsic_value, continuation_value)
            else:
                option_value = continuation_value

            new_values.append(option_value)

        option_values = new_values
        tree.insert(0, [round(value, 4) for value in option_values])

    # Pad rows
    padded_tree = []

    for row in tree:
        while len(row) < steps + 1:
            row.append(None)

        padded_tree.append(row)

    return padded_tree

def price_european_option_binomial(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
    steps,
    option_type="call",
):
    """Price a European option using a binomial tree."""

    # European wrapper
    return price_option_binomial(
        stock_price=stock_price,
        strike_price=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        steps=steps,
        option_type=option_type,
        exercise_style="european",
    )


def price_american_option_binomial(
    stock_price,
    strike_price,
    time_to_maturity,
    risk_free_rate,
    volatility,
    steps,
    option_type="call",
):
    """Price an American option using a binomial tree."""

    # American wrapper
    return price_option_binomial(
        stock_price=stock_price,
        strike_price=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        steps=steps,
        option_type=option_type,
        exercise_style="american",
    )