# 📊 Options Greeks Simulator

An interactive **Streamlit app** to explore option pricing, Greeks, implied volatility smiles, and delta-hedged portfolios.  
Implements **Black–Scholes**, **SVI fitting**, and a simple **delta-hedging simulator**.

🔗 **Live Demo:** [Open App](https://quantfinanceproject-4bgfmqei4xmc9wlvb35wwu.streamlit.app/)

---

## 🚀 Features

### 1. Greeks Explorer
- Compute **Black–Scholes option price** (Call/Put).  
- Visualize Greeks (**Δ, Γ, Vega, Θ, ρ**).  
- Interactive plots of Greeks vs Spot Price.  

📸 *Screenshot placeholder:*  
![Greeks Explorer Screenshot](https://github.com/user-attachments/assets/YOUR_IMAGE_ID)

---

### 2. Implied Volatility Smile
- Download option chain data via **yfinance**.  
- Compute market implied vols.  
- Fit an **SVI curve** for smooth smiles.  
- Visualize *log-moneyness* vs implied vol.  

📸 *Screenshot placeholder:*  
![IV Smile Screenshot](https://github.com/user-attachments/assets/YOUR_IMAGE_ID)

---

### 3. Hedging / Delta-neutral
- Simulate **long option + short Δ shares of stock**.  
- Choose rebalancing frequency → study **hedging cost vs accuracy trade-off**.  
- Charts included:  
  - **Option vs Hedged Portfolio Value**  
  - **Option Δ vs Portfolio Δ**  
  - **Cumulative Hedging Cost**  

📸 *Screenshot placeholder:*  
![Delta Hedging Screenshot](https://github.com/user-attachments/assets/YOUR_IMAGE_ID)

---

## 📈 Hedging Trade-off (Intuition)

- Rebalancing **more often** → keeps portfolio Δ ≈ 0 (**better hedge accuracy**)  
- Rebalancing **less often** → lowers transaction costs but Δ drifts (**less accuracy**)  
- Trade-off = *accuracy vs cost*

---

## 🛠 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/options-greeks-simulator.git
cd options-greeks-simulator
pip install -r requirements.txt
