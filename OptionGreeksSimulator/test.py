# smile_demo_simple.py
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from math import log, sqrt, exp
from scipy.stats import norm
from scipy.optimize import brentq, curve_fit
from datetime import datetime
import pandas as pd
from bs import bs_price


# For a given option price we use brent root function to find implied vol for it and other params
def implied_vol(price, S, K, r, q, T, option="call"):
    f = lambda sigma: bs_price(S,K,r,q,sigma,T,option) - price  # lambda gives function for difference with sigma as parameter
    try:
        return brentq(f, 1e-6, 3.0)
    except:
        return np.nan

# --- SVI total variance ---
def svi_w(k, a, b, rho, m, sig):
    return a + b*(rho*(k-m) + np.sqrt((k-m)**2 + sig**2))   #formula for SVI

# --- Core pipeline ---
def plot_smile(ticker="TSLA", expiry="2025-12-19", r=0.05, q=0.0):
    S = float(yf.download(ticker, period="1d")["Close"].iloc[-1].item())    # Last closing price for Tesla
    T = (datetime.strptime(expiry, "%Y-%m-%d") - datetime.now()).days / 365     # Time difference now until expiry (string to datetime)
    F = S*exp((r-q)*T)  # Forward price

    chain = yf.Ticker(ticker).option_chain(expiry)
    calls, puts = chain.calls, chain.puts

    # OTM only since they are most liquid and easy to plot, so F > K take OTM puts, and F < K OTM calls
    df_calls = calls[calls["strike"] > S]
    df_puts  = puts[puts["strike"] < S]
    df = pd.concat([
    df_calls[["strike","lastPrice"]].assign(type="call"),
    df_puts[["strike","lastPrice"]].assign(type="put")
], ignore_index=True)

    # Compute IVs from the data
    ivs = []
    for row in df.itertuples(index=False):
        ivs.append(implied_vol(row.lastPrice, S, row.strike, r, q, T, row.type))
    df["iv"] = ivs
    df = df[(df["iv"] > 0.02) & (df["iv"] < 2.0)]       # Only conserve rows of df if IV is within safe bounds 
    df["logk"] = np.log(df["strike"]/F)         # Compute the log moneyness
    df = df.dropna()

    # Fit SVI
    w = (df["iv"]**2)*T
    params, _ = curve_fit(svi_w, df["logk"], w, p0=[0.1,0.2,-0.3,0,0.1])        # Use nonlinear least squares to fit parameters that yield
    k_grid = np.linspace(df["logk"].min(), df["logk"].max(), 200)
    iv_fit = np.sqrt(svi_w(k_grid,*params)/T)       # Total variance back to volatility

    # Plot
    plt.scatter(df["logk"], df["iv"], label="Market IV")
    plt.plot(k_grid, iv_fit, "r-", label="SVI fit")
    plt.axvline(0, ls="--", c="grey")
    plt.xlabel("log-moneyness")
    plt.ylabel("Implied Volatility")
    plt.legend(); plt.show()

plot_smile()