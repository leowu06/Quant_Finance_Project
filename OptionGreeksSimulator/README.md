# 📊 Options Greeks Simulator

An interactive **Streamlit app** to explore option pricing, Greeks, implied volatility smiles, and delta-hedged portfolios.  
Implements **Black–Scholes**, **SVI fitting**, and a simple **delta-hedging simulator**.

**Live Demo:** [Open App](https://quantfinanceproject-4bgfmqei4xmc9wlvb35wwu.streamlit.app/)

---

## Tabs

### 1. Greeks Explorer
- Compute **Black–Scholes option price** (Call/Put).  
- Visualize Greeks (**Δ, Γ, Vega, Θ, ρ**) through interactive plots of Greek vs Spot Price.
  eg: (Put) Delta ATM ∼ 0.5, Delta ITM ∼ 1, Gamma ATM (highest)

<img width="1554" height="856" alt="image" src="https://github.com/user-attachments/assets/3c947b50-afad-493a-960f-80d5dd12a79b" />


---

### 2. Implied Volatility Smile
- Extracted option chain data via **yfinance**. 
- Compute market implied vols by implementing Black-Scholes.
- Concatenated OTM calls left of Spot price and OTM puts on its right - leads to a more noticeable smile since deep ITM can be illiquid or have lower trading volume.
- Fit an **SVI curve** with least for smooth smiles
- Visualize *log-moneyness* vs implied vol.

  Here’s a concise, copy-paste ready README block you can use to show the math clearly:

⸻

SVI Smile Fit

We fit the implied volatility smile using the SVI (Stochastic Volatility Inspired) parameterization:

w(k) = a + b \Big( \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \Big)

where w(k) = \sigma^2 T is the total variance at log-moneyness k = \ln(K/F).
Parameters (a,b,\rho,m,\sigma) are estimated via nonlinear least squares to best match market option quotes.
This produces a smooth, arbitrage-free implied volatility curve from sparse market data.

⸻



<img width="1089" height="825" alt="image" src="https://github.com/user-attachments/assets/efc34d70-f334-4fd9-9734-e964e8ffd6be" />

---

### 3. Hedging / Delta-neutral
- Simulate **long option + short Δ shares of stock**.  
- Choose rebalancing frequency → study **hedging cost vs accuracy trade-off**.  
- Charts included:  
  - **Option vs Hedged Portfolio Value**  
  - **Option Δ vs Portfolio Δ**  
  - **Cumulative Hedging Cost**  


<img width="1561" height="774" alt="image" src="https://github.com/user-attachments/assets/b5670720-b9e1-4dbd-a2e8-6ec874b5d6a9" />

---

## 📈 Hedging Trade-off (Intuition)

- Rebalancing **more often** → keeps portfolio Δ ≈ 0 (**better hedge accuracy**)  
- Rebalancing **less often** → lowers transaction costs but Δ drifts (**less accuracy**)  
- Trade-off = *accuracy vs cost*


