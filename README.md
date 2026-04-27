

# Binomial Option Pricer

A Streamlit application for pricing European and American call and put options using a binomial tree model. The app also compares European option prices against the Black-Scholes model and shows convergence as the number of binomial steps increases.

## Project Overview

This project builds an interactive option pricing tool using Python. The main goal is to show how a numerical binomial model can price options step by step and how European binomial prices converge toward the Black-Scholes closed-form benchmark.

The binomial model is useful because it is flexible. Unlike Black-Scholes, it can naturally handle American options where early exercise may be optimal.

## Features

- Price European call options
- Price European put options
- Price American call options
- Price American put options
- Compare European binomial prices to Black-Scholes prices
- Display the absolute difference between the two models
- Show a convergence chart as the number of steps increases
- Show stock price and option value tree previews for small step counts
- Run automated tests with pytest

## How the Binomial Model Works

The binomial model assumes that the stock price can move up or down during each time step. At expiration, the option payoff is calculated. Then the model works backward through the tree to calculate the option value today.

For each step, the model calculates:

```text
dt = T / N
u = e^(sigma * sqrt(dt))
d = 1 / u
p = (e^(r * dt) - d) / (u - d)
```

Where:

- `S` = stock price
- `K` = strike price
- `T` = time to maturity
- `r` = risk-free rate
- `sigma` = volatility
- `N` = number of steps
- `u` = up factor
- `d` = down factor
- `p` = risk-neutral probability

For European options, the model only uses the discounted continuation value.

For American options, the model compares early exercise against continuation value at each node:

```text
option value = max(intrinsic value, continuation value)
```

## Black-Scholes Comparison

For European options, the app calculates the Black-Scholes price as a benchmark. As the number of binomial steps increases, the binomial price should move closer to the Black-Scholes price.

The app shows:

- Binomial price
- Black-Scholes price
- Absolute difference
- Convergence chart
- Convergence data table

## Project Structure

```text
binomial_option_pricer/
|
|-- app.py
|-- requirements.txt
|-- README.md
|
|-- src/
|   |-- binomial.py
|   |-- black_scholes.py
|   |-- plots.py
|   |-- utils.py
|
|-- tests/
    |-- test_binomial.py
    |-- test_black_scholes_compare.py
```

## File Descriptions

### `app.py`

Streamlit interface for the project. It collects user inputs, displays option prices, shows model summaries, compares European prices against Black-Scholes, and displays charts and tree previews.

### `src/binomial.py`

Contains the main binomial option pricing logic. It supports European and American exercise styles for both calls and puts. It also includes helper functions to build stock price and option value trees.

### `src/black_scholes.py`

Contains Black-Scholes pricing formulas for European call and put options.

### `src/plots.py`

Builds convergence data and creates the convergence chart comparing binomial prices against the Black-Scholes benchmark.

### `src/utils.py`

Contains simple formatting and validation helpers.

### `tests/`

Contains pytest tests for the binomial pricing engine, tree-building functions, Black-Scholes formulas, and convergence behavior.

## Installation

Clone the repository:

```bash
git clone https://github.com/kserrot/binomial-option-pricer.git
cd binomial-option-pricer
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL in your browser.

## Run Tests

Run all tests with:

```bash
python -m pytest -q
```

## Example Inputs

```text
Stock Price: 100
Strike Price: 100
Time to Maturity: 1 year
Risk-Free Rate: 0.05
Volatility: 0.20
Steps: 100
Option Type: call
Exercise Style: european
```

With these inputs, the European call price from the binomial model should be close to the Black-Scholes price.


## Author

Kaique Torres