# hedge_simple.py
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from bs import bs_price, bs_greeks
import matplotlib.pyplot as plt

def get_portfolio_pnl(ticker, shares, r, q, sigma, T, rebalance_every=5):
    endDate = datetime.now()
    startDate = endDate - timedelta(days=int(T*365))
    S_series = yf.download(ticker, startDate, endDate)
    S_series = S_series["Close"]

    # If it's a DataFrame (multi-ticker), reduce to a Series
    if isinstance(S_series, pd.DataFrame):
        S_series = S_series.iloc[:, 0]

    # Force float, drop NaN
    S_series = pd.to_numeric(S_series, errors="coerce").dropna()

    n = len(S_series)
    T_grid = [T - i*(T/(n-1)) for i in range(n)]
    K = float(S_series.median())  # ATM strike

    hedged_delta, unhedged_delta, option_vals, hedge_vals, portfolio_vals, costs = [], [], [], [], [], []

    cash = 0.0
    hedge_pos = 0.0
    total_cost = 0.0
    i = 0

    for S, t in zip(S_series, T_grid):
        opt_val = bs_price(S, K, r, q, sigma, max(t, 1e-6)) * shares
        delta = bs_greeks(S, K, r, q, sigma, max(t, 1e-6))["delta"] * shares

        if i % rebalance_every == 0 or i == 0:
            new_hedge = -delta
            trade = (new_hedge - hedge_pos) * S
            cash -= trade       # Difference of short position when rebalancing, depending on delta and S
            total_cost += trade
            hedge_pos = new_hedge

        hedge_val = hedge_pos * S
        port_val = opt_val + hedge_val + cash

        unhedged_delta.append(delta)
        hedged_delta.append(delta + hedge_pos)
        option_vals.append(opt_val)
        hedge_vals.append(hedge_val)
        portfolio_vals.append(port_val)
        costs.append(total_cost)

        i += 1

    df = pd.DataFrame({
        "Stock": S_series.values,
        "Option": option_vals,
        "Hedge": hedge_vals,
        "Portfolio": portfolio_vals,
        "TotalCost": costs,
        "OptionDelta": unhedged_delta,
        "PortfolioDelta": hedged_delta
        }, index=S_series.index)

    df.attrs["FinalCost"] = total_cost

    return df


# Example run
df = get_portfolio_pnl("TSLA", shares=1, r=0.05, q=0.0, sigma=0.25, T=1)
df[["Option", "Portfolio"]].plot(title="Option vs Hedged Portfolio", figsize=(8,5))
plt.ylabel("Value"); plt.grid(True, alpha=0.3); plt.show()

df[["TotalCost"]].plot(title="Total Money Put In", figsize=(8,4))
plt.ylabel("Cumulative $"); plt.grid(True, alpha=0.3); plt.show()
