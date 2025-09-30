# Options Greeks Simulator

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
Black-Scholes formula assumes that the market has flat volatility, we showcase a more realistic behaviour where traders buy 'insurance' for a 'black swan' crash. They are willing to pay for OTM options leading to higher volatility, hence fat tails
- Extracted option chain data via **yfinance**. 
- Compute market implied vols by implementing Black-Scholes.
- Concatenated OTM calls left of Spot price and OTM puts on its right - leads to a more noticeable smile since deep ITM can be illiquid or have lower trading volume.
- Fit an **SVI curve** with least for smooth smiles
- Visualize *log-moneyness* vs implied vol.

## **SVI Smile Fit**

We fit the implied volatility smile using the **SVI (Stochastic Volatility Inspired)** parameterisation:

$$
w(k) = a + b \Big( \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \Big)
$$

where $w(k) = \sigma^2 T$ is the **total variance** at log-moneyness $k = \ln(K/F)$.  
Parameters $(a,b,\rho,m,\sigma)$ are estimated through **nonlinear least squares** to match the previously calculated implied vols.  
This produces a **smooth implied volatility curve**.



<img width="1089" height="825" alt="image" src="https://github.com/user-attachments/assets/efc34d70-f334-4fd9-9734-e964e8ffd6be" />

---

### 3. Dynamic Hedging / Delta-neutral
Trading firms/traders stay delta-neutral to reduce exposure to directional risk (like owning the stock). If they own a call option with Δ, they short Δ stocks in order to have a conjoined portfolio delta = 0. (With gamma > 0, rebalancing often needed)

$$
\Delta_{\text{portfolio}} = \Delta_{\text{option}} \cdot N_{\text{options}} + \Delta_{\text{stock}} \cdot N_{\text{stocks}} = 0
$$

Since $\Delta_{\text{stock}} = 1$, the hedge requires:

$$
N_{\text{stocks}} = - \Delta_{\text{option}} \cdot N_{\text{options}}
$$
$$
text{Since} \frac{d\Delta}{dS} = \Gamma > 0 \ \ \Rightarrow\ \text{hedge must be rebalanced.}
$$

- We simulate hedging with user-chosen rebalancing frequency → study **hedging cost vs accuracy trade-off**.  
- Charts included:  
  - **Option vs Hedged Portfolio Value**  
  - **Option Δ vs Portfolio Δ**  


<img width="1561" height="774" alt="image" src="https://github.com/user-attachments/assets/b5670720-b9e1-4dbd-a2e8-6ec874b5d6a9" />

Dynamic Hedging comes at a cost:
- Rebalancing **more often** → keeps portfolio Δ ≈ 0 (**better hedge accuracy**)  
- Rebalancing **less often** → lowers transaction costs but Δ drifts (**less accuracy**)  
This is displayed in the app, user can modify rebalancing frequency.


