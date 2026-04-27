"""Utility helpers for the binomial option pricer."""


def format_decimal(value, decimals=4):
    """Format a number with fixed decimals."""

    # Format number
    return f"{value:.{decimals}f}"


def format_currency(value, decimals=2):
    """Format a number as currency."""

    # Format money
    return f"${value:.{decimals}f}"


def format_percent(value, decimals=2):
    """Format a decimal as a percentage."""

    # Format percent
    return f"{value * 100:.{decimals}f}%"


def validate_positive_number(value, name):
    """Validate that a number is positive."""

    # Check positive
    if value <= 0:
        raise ValueError(f"{name} must be positive.")

    return value