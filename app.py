"""Streamlit app for binomial option pricing."""

import pandas as pd
import streamlit as st

from src.binomial import (
    build_option_value_tree,
    build_stock_price_tree,
    price_american_option_binomial,
    price_european_option_binomial,
    price_option_binomial,
)
from src.black_scholes import call_price, put_price
from src.plots import build_convergence_data, create_convergence_plot
from src.utils import format_currency, format_percent

st.set_page_config(
    page_title="Binomial Option Pricer",
    layout="wide",
)

st.title("Binomial Option Pricer")

st.write(
    "This app prices call and put options using a binomial tree model. "
    "It supports European and American exercise styles."
)

# Sidebar inputs
st.sidebar.header("Option Inputs")

stock_price = st.sidebar.number_input(
    "Stock Price",
    min_value=0.01,
    value=100.00,
    step=1.00,
)

strike_price = st.sidebar.number_input(
    "Strike Price",
    min_value=0.01,
    value=100.00,
    step=1.00,
)

time_to_maturity = st.sidebar.number_input(
    "Time to Maturity in Years",
    min_value=0.01,
    value=1.00,
    step=0.25,
)

risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate",
    min_value=0.00,
    value=0.05,
    step=0.01,
    format="%.4f",
)

volatility = st.sidebar.number_input(
    "Volatility",
    min_value=0.01,
    value=0.20,
    step=0.01,
    format="%.4f",
)

steps = st.sidebar.number_input(
    "Number of Steps",
    min_value=1,
    max_value=1000,
    value=100,
    step=1,
)

option_type = st.sidebar.selectbox(
    "Option Type",
    options=["call", "put"],
)

exercise_style = st.sidebar.selectbox(
    "Exercise Style",
    options=["european", "american"],
)

# Price option
try:
    option_price = price_option_binomial(
        stock_price=stock_price,
        strike_price=strike_price,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        steps=steps,
        option_type=option_type,
        exercise_style=exercise_style,
    )

    # Output section
    st.subheader("Option Price")

    st.metric(
        label=f"{exercise_style.title()} {option_type.title()} Price",
        value=format_currency(option_price),
    )

    # Summary section
    st.subheader("Model Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Stock Price:**", format_currency(stock_price))
        st.write("**Strike Price:**", format_currency(strike_price))

    with col2:
        st.write("**Maturity:**", f"{time_to_maturity:.2f} years")
        st.write("**Steps:**", steps)

    with col3:
        st.write("**Risk-Free Rate:**", format_percent(risk_free_rate))
        st.write("**Volatility:**", format_percent(volatility))

    # Small tree preview
    st.subheader("Binomial Tree Preview")

    if steps <= 5:
        stock_tree = build_stock_price_tree(
            stock_price=stock_price,
            time_to_maturity=time_to_maturity,
            volatility=volatility,
            steps=steps,
        )

        option_tree = build_option_value_tree(
            stock_price=stock_price,
            strike_price=strike_price,
            time_to_maturity=time_to_maturity,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            steps=steps,
            option_type=option_type,
            exercise_style=exercise_style,
        )

        tree_col1, tree_col2 = st.columns(2)

        with tree_col1:
            st.write("**Stock Price Tree**")
            st.dataframe(pd.DataFrame(stock_tree), width="stretch")

        with tree_col2:
            st.write("**Option Value Tree**")
            st.dataframe(pd.DataFrame(option_tree), width="stretch")
    else:
        st.info(
            "Tree preview is shown only when the number of steps is 5 or less. "
            "Lower the steps in the sidebar to view the tree."
        )


    # European benchmark
    if exercise_style == "european":
        st.subheader("Black-Scholes Comparison")

        # Calculate benchmark
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

        # Calculate difference
        absolute_difference = abs(option_price - black_scholes_price)

        comp_col1, comp_col2, comp_col3 = st.columns(3)

        with comp_col1:
            st.metric("Binomial Price", format_currency(option_price))

        with comp_col2:
            st.metric("Black-Scholes Price", format_currency(black_scholes_price))

        with comp_col3:
            st.metric("Absolute Difference", format_currency(absolute_difference))

        st.subheader("Convergence Chart")

        # Build chart data
        convergence_data = build_convergence_data(
            stock_price=stock_price,
            strike_price=strike_price,
            time_to_maturity=time_to_maturity,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            option_type=option_type,
        )

        # Show chart
        convergence_df = pd.DataFrame(convergence_data)
        convergence_fig = create_convergence_plot(convergence_data)
        st.pyplot(convergence_fig, clear_figure=True)

        # Show data
        with st.expander("View convergence data"):
            st.dataframe(convergence_df, width="stretch")

        # Download data
        csv_data = convergence_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download convergence data as CSV",
            data=csv_data,
            file_name="binomial_convergence_data.csv",
            mime="text/csv",
        )

    # American note
    else:
        st.info(
            "Black-Scholes comparison is shown only for European options. "
            "American options may allow early exercise, so they do not use "
            "the same closed-form benchmark."
        )

    # Early exercise comparison
    if option_type == "put":
        st.subheader("Early Exercise Comparison")

        european_put_price = price_european_option_binomial(
            stock_price=stock_price,
            strike_price=strike_price,
            time_to_maturity=time_to_maturity,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            steps=steps,
            option_type="put",
        )

        american_put_price = price_american_option_binomial(
            stock_price=stock_price,
            strike_price=strike_price,
            time_to_maturity=time_to_maturity,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            steps=steps,
            option_type="put",
        )

        early_exercise_premium = american_put_price - european_put_price

        early_col1, early_col2, early_col3 = st.columns(3)

        with early_col1:
            st.metric("European Put", format_currency(european_put_price))

        with early_col2:
            st.metric("American Put", format_currency(american_put_price))

        with early_col3:
            st.metric(
                "Early Exercise Premium",
                format_currency(early_exercise_premium),
            )

        st.write(
            "American puts can be worth more than European puts because the "
            "holder may exercise early when it is optimal."
        )

    # Explanation section
    st.subheader("How the Binomial Model Works")

    st.write(
        "The binomial model builds a price tree where the stock can move up "
        "or down at each step. The option value is calculated at expiration "
        "and then discounted backward to today."
    )

    if exercise_style == "american":
        st.write(
            "For American options, the model checks at every step whether "
            "early exercise is better than holding the option."
        )
    else:
        st.write(
            "For European options, the model only uses the continuation value "
            "because early exercise is not allowed."
        )

except ValueError as error:
    st.error(str(error))