import streamlit as st
from bs import bs_price, bs_greeks
from plotter import compute_series_vs_spot
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd            
import yfinance as yf
import svi as svi
import altair as alt


st.set_page_config(page_title="Options Greeks Simulator", layout="wide")
st.title("Options Greeks Simulator")

# App tabs
tab1, tab2, tab3 = st.tabs(["Greeks Explorer", "IV Smile", "Hedging / Delta-neutral"])


with tab1:
    st.subheader("Greeks Explorer")
    st.caption("Black–Scholes Option Pricing with Continuous Dividend Yield (q). Parameters: S, K, r, q, σ, T. Outputs: Greeks (Δ, Γ, Vega, Θ, ρ)")

    # Inputs
    col_inputs, col_outputs = st.columns([1,2])
    with col_inputs:
        option_type = st.selectbox("Option Type", ["Call", "Put"], index=0)
        S = st.number_input("Spot Price S", min_value=1.0, max_value=1e6, value=100.0, step=1.0, format="%0.2f")
        K = st.number_input("Strike Price K", min_value=1.0, max_value=1e6, value=100.0, step=1.0, format="%0.2f")
        sigma = st.slider("Volatility σ", min_value=0.01, max_value=2.0, value=0.20, step=0.01)
        T = st.slider("Time to Maturity T (years)", min_value=0.01, max_value=5.0, value=1.00, step=0.01)
        r = st.slider("Risk-free Rate r", min_value=0.00, max_value=0.20, value=0.05, step=0.005)
        q = st.slider("Dividend Yield q", min_value=0.00, max_value=0.20, value=0.00, step=0.005)
        plot_greeks = st.checkbox("Plot greeks vs S (±30%)", value=True)

    # Safety guards for numerical stability
    sigma_eff = max(float(sigma), 1e-8)
    T_eff = max(float(T), 1e-8)

    # Price and greeks
    price = bs_price(S, K, r, q, sigma_eff, T_eff, option=option_type)
    greeks = bs_greeks(S, K, r, q, sigma_eff, T_eff, option_type)

    with col_outputs:
        st.markdown("### Price")
        st.metric(label=f"{option_type} Price", value=f"{price:,.4f}")

        # Display values for Greeks chosen by user
        st.markdown("### Greeks")
        c1, c2, c3 = st.columns(3)
        c4, c5, _ = st.columns(3)
        c1.metric("Delta", f"{greeks['delta']:.4f}")
        c2.metric("Gamma", f"{greeks['gamma']:.6f}")
        c3.metric("Vega (per 1% σ)", f"{greeks['vega']:.4f}")
        c4.metric("Theta (per day)", f"{greeks['theta']:.4f}")
        c5.metric("Rho (per 1% r)", f"{greeks['rho']:.4f}")

        if plot_greeks:
            # Let user choose which to plot (clear y-axis units)
            series_name = st.selectbox(
                "Choose a series to plot",
                ["Price", "Delta", "Gamma", "Vega (per 1% σ)", "Theta (per day)", "Rho (per 1% r)"],
                index=0,
            )
            st.subheader(f"{series_name} vs Spot S")

            s_grid, y_vals, y_label = compute_series_vs_spot(series_name,S,K,r,q,sigma,T,option_type)

            # Interactive line chart
            chart_df = pd.DataFrame(
                {y_label: y_vals},
                index=pd.Index(s_grid, name="Spot S"),
            )
            st.line_chart(chart_df, height=280, use_container_width=True)
            st.caption(f"X: Spot Price S    •    Y: {y_label}")

 


with tab2:
    st.subheader("Implied Volatility Smile")
    st.caption("Market implied vols from option prices, with an SVI curve fit for a smooth function")

    ticker = st.selectbox("Choose ticker to plot", ["INTC", "GLD", "NKE", "PLTR", "AAPL", "TSLA", "AMZN", "KO", "NKE"], index = 0)
    if ticker:
        good_exps = svi.usable_expiries(ticker, 5)
        if not good_exps:
            st.warning(f"No usable expiries found for {ticker}")
        else:
            expiry = st.selectbox("Expiry Dates", good_exps, index= 0)
            market_df, svi_df = svi.compute_smile(ticker, expiry)
            try:
                market_df, svi_df = svi.compute_smile(ticker, expiry)

                # Market points
                market_chart = (alt.Chart(market_df).mark_point(color="blue", size=50, opacity=0.9).encode(x=alt.X("logk:Q", title="Log-moneyness"),
                        y=alt.Y("iv:Q",title="Implied Volatility",scale=alt.Scale(domain=[0.5* market_df["iv"].min(), market_df["iv"].max()*1.3]))))

                # SVI smooth line
                svi_chart = (alt.Chart(svi_df).mark_line(color="red", strokeWidth=2).encode(x="logk:Q",y="iv:Q"))

                # ATM vertical line
                atm_line = (alt.Chart(pd.DataFrame({"logk":[0]})).mark_rule(strokeDash=[4,4], color="white").encode(x="logk:Q"))
                chart = (market_chart + svi_chart + atm_line).properties(width=700, height=800)

                st.altair_chart(chart, use_container_width=False)
                st.caption(f"{ticker} | {expiry} | Points: {len(market_df)}")

            except Exception as e:
                st.error(f"Could not compute smile: {e}")

with tab3:
    st.subheader("Hedging / Delta-neutral")
    st.caption(
        "Simulate a simple delta-hedged portfolio: long option + short Δ shares of stock. "
        "Shows portfolio value, delta exposure, and cumulative hedging cost."
    )

    ticker = st.selectbox("Choose ticker", ["AAPL", "TSLA", "INTC", "AMZN"], index=0)
    vol = st.slider("Volatility σ", min_value=0.05, max_value=1.0, value=0.25, step=0.05)
    rebalance_every = st.slider("Rebalance frequency (days)", min_value=1, max_value=30, value=5, step=1)

    from hedge import get_portfolio_pnl
    try:
        df = get_portfolio_pnl(
            ticker, shares=100, r=0.05,q=0, sigma=vol, T=1, rebalance_every=rebalance_every
        )

        st.markdown("### Portfolio Value")
        st.line_chart(df[["Option", "Portfolio"]], height=320, use_container_width=True)
        st.caption("Option value vs hedged portfolio (long call + short Δ shares)")

        if "OptionDelta" in df.columns and "PortfolioDelta" in df.columns:
            st.markdown("### Portfolio Delta")
            st.line_chart(df[["OptionDelta", "PortfolioDelta"]], height=320, use_container_width=True)
            st.caption("Option Δ vs Portfolio Δ (hedge aims to keep Portfolio Δ ≈ 0)")
            st.caption(f"Hedging Cost for total period: {df.attrs["FinalCost"]:.2f}")

    except Exception as e:
        st.error(f"Simulation failed: {e}")