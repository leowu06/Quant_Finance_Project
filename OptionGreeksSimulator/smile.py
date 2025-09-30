import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from bs import bs_price, _d1_d2
from datetime import datetime

def fetch_option(ticker: str, expiry: str):
    ticker = yf.Ticker(ticker)
    chain = ticker.option_chain(expiry)
    calls = chain.calls.copy()
    puts = chain.puts.copy()
    return calls, puts

def get_spot_price(ticker: str):
    spot = yf.download(ticker, period="1d")['Close'].iloc[-1]
    return spot

def call_put_pairs(calls, puts):
    calls = calls.copy()
    puts = puts.copy()
    calls['call_mid'] = (calls['bid'].clip(lower=0) + calls['ask']) / 2
    puts['put_mid']   = (puts['bid'].clip(lower=0) + puts['ask']) / 2

    calls = calls[(calls["strike"] > 0) & (calls["call_mid"] > 0) & np.isfinite(calls["call_mid"])]
    puts  = puts[(puts["strike"] > 0) & (puts["put_mid"] > 0) & np.isfinite(puts["put_mid"])]

    pairs = pd.merge(calls[["strike", "call_mid"]], puts[["strike", "put_mid"]], on = "strike", how = "inner")
    return pairs

def forward_and_df_from_parity(pairs_df):
    """
    Input: DataFrame with ['strike','call_mid','put_mid'] (cleaned).
    Output: (F, DF) inferred via OLS on y = C-P = a + b*K.
    """
    import numpy as np

    if pairs_df is None or pairs_df.empty:
        return None, None

    y = pairs_df["call_mid"] - pairs_df["put_mid"]
    K = pairs_df["strike"]

    m = np.isfinite(y) & np.isfinite(K)
    y, K = y[m], K[m]
    if len(y) < 3 or np.var(K) <= 0:
        return None, None

    cov = np.cov(K, y, bias=True)  # population moments
    varK = cov[0, 0]
    covKy = cov[0, 1]
    b = covKy / varK
    a = float(y.mean() - b * K.mean())

    DF = float(-b)
    if DF <= 0 or DF > 1.2:  # sanity
        return None, None
    F = a / DF
    if not np.isfinite(F) or F <= 0:
        return None, None
    return float(F), float(DF)

def implied_vol(S,K, price_market,F,DF,T,option_type ="call"):
    S = float(S)
    K = float(K)
    price_market = float(price_market)
    T = float(T)
    if T <= 0 or S <= 0 or K<= 0:
        return np.nan
    
    r = -np.log(DF) / T
    q = r- (np.log(F/S)/T)

    def objective(sigma):
        return bs_price(S,K,r,q,sigma,T,option_type) - price_market
    try:
        iv = brentq(objective, 1e-6, 5, maxiter = 100, xtol=1e-6)
        return float(iv)
    except Exception:
        return np.nan
    
def iv_smile(ticker:str, expiry: str):
    """
    Fetch options, for ticker and expiry, clean data, infers
    forward and discount factor, compute implied vols across strikes
    """
    calls, puts = fetch_option(ticker, expiry)

    pairs = call_put_pairs(calls,puts)
    if pairs.empty:
        raise RuntimeError("No valid call-put pairs found")
    
    F,DF = forward_and_df_from_parity(pairs)
    if F is None or DF is None:
        raise RuntimeError("Failed to infer forward/DF from parity")
    
    S = get_spot_price(ticker)

    expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")
    today = datetime.now()
    T = (expiry_dt - today).days / 365.0
    if T <= 0:
        raise RuntimeError("Expiry already passed or invalid")
    
    r = -np.log(DF) / T
    q = r - (np.log(F / S) / T)

    ivs = []
    for _, row in pairs.iterrows():
        iv = implied_vol(S, row["strike"], row["call_mid"], F, DF, T, option_type="call")
        ivs.append(iv)
    pairs["implied_vol"] = ivs

    # 8. Package metadata
    meta = {"F": F, "DF": DF, "S": S, "T": T, "r": r, "q": q}
    return pairs, meta

from scipy.optimize import curve_fit

# SVI function: takes log-moneyness k
def svi_total_variance(k, a, b, rho, m, sigma):
    return a + b*(rho*(k-m) + np.sqrt((k-m)**2 + sigma**2))

def fit_svi(log_moneyness, ivs, T):
    """
    Fit SVI to implied vol data.
    Returns optimal params.
    """
    w = (ivs**2) * T  # total variance
    popt, _ = curve_fit(
        svi_total_variance, log_moneyness, w,
        bounds=([-1, 0, -0.999, -2, 1e-6],  # lower bounds
                [ 5, 10, 0.999,  2, 2])     # upper bounds
    )
    return popt

def svi_curve(log_moneyness_grid, params, T):
    a, b, rho, m, sigma = params
    w = svi_total_variance(log_moneyness_grid, a, b, rho, m, sigma)
    return np.sqrt(w / T)  # implied vol

pairs, meta = iv_smile("SPY", "2025-12-19")   # or any liquid expiry
pairs = pairs[(pairs["implied_vol"] > 0.02) & (pairs["implied_vol"] < 5)]
pairs["log_moneyness"] = np.log(pairs["strike"] / meta["F"])

# Fit SVI
params = fit_svi(pairs["log_moneyness"].values, pairs["implied_vol"].values, meta["T"])

# Smooth curve
k_grid = np.linspace(pairs["log_moneyness"].min(), pairs["log_moneyness"].max(), 200)
iv_fit = svi_curve(k_grid, params, meta["T"])

# Plot
import matplotlib.pyplot as plt
plt.scatter(pairs["log_moneyness"], pairs["implied_vol"], label="Market IV", color="blue")
plt.plot(k_grid, iv_fit, label="SVI Fit", color="red")
plt.axvline(0, color="grey", linestyle="--")  # ATM
plt.xlabel("Log-moneyness")
plt.ylabel("Implied Volatility")
plt.legend()
plt.show()