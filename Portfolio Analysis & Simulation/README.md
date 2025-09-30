# Portfolio Simulation & Analysis

This directory contains projects focused on simulating portfolio performance and analyzing risk using Monte Carlo methods.

---

## **PortfolioSimulationMonteCarlo**

Simulates investing **40 €/month** into a diversified portfolio (**QQQ, MSCI, GLD, VOO**) for **21 years** until age 40.
- Employs **Dollar-Cost Averaging** with an initial investment of **1600 €**.
- Calculates the portfolio’s diversification overlap.

### Method:
- **Monte Carlo Simulation** with **1000 paths**.
- Models **fat-tailed returns** using a **Student-t distribution** to better represent real-life higher frequency tail events, moving beyond the normal distribution assumption.
- Portfolio weights are fixed at `[2,3,3,5]` and then normalized.

### Key Outputs:
The simulation tracks:
- **Compounding** growth
- **Volatility**
- **Diversification overlap**

### Risk Metrics Calculated:
- **VaR (90%):** The worst-case cutoff (10th percentile) of the final portfolio value.
- **CVaR:** The average value of the worst 10% of scenarios (Conditional Value at Risk).
- **Overlap %:** A quantitative measure of the portfolio's diversification.

**Note:** This project was created after understanding the core concepts of VaR, CVaR, and Monte Carlo simulation, and it serves as a comprehensive representation of the skills applied in this folder.

---

## **VaRPortfolioComparison**

Compares the risk profiles of different portfolio strategies by calculating their **Value at Risk (VaR)**.
- Compares **Balanced**, **Tech-heavy**, and **Low-risk** portfolios.
- Uses a similar **Monte Carlo methodology** to simulate outcomes.
- Plots and visualizes the distribution of the three final portfolio values for comparison.

  <img width="593" height="455" alt="image" src="https://github.com/user-attachments/assets/27b349b8-12eb-48c7-829f-795869ec4d23" />


---

## **StockOptimisation**

Takes a user-defined set of stock tickers and optimizes for the best risk-adjusted returns.
- The core function is to algorithmically **change the weighting** of the investments in the portfolio.
- The optimization process seeks the allocation that maximizes returns for a given level of risk (or minimizes risk for a given return target).
