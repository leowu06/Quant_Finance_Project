# Finance and Derivatives

This repository contains a collection of projects in **Portfolio Analysis, Strategy Backtesting** and **Options Greeks Simulation**. These were coded through Python, so I included **README** files in each folder with screenshots of each functionality and visual graphs, so the reader can interpret the purpose.

Furthermore, I have made a 3-tab **Streamlit app** that allows the user to interact with the input and simulation parameters (Options): [App (Streamlit UI)](OptionGreeksSimulator/README.md).

---

## Portfolio Simulation & Analysis: ([Portfolio Analysis & Simulation](https://github.com/leowu06/Quant_Finance_Project/tree/1e122639db5233b4c7780bbd1587d137db01a67f/Portfolio%20Analysis%20%26%20Simulation)).
For the main file I simulated **21 years of investing** in [QQQ, MSCI, GLD, VOO] 40€ a month with an initial 1600€ vs **saving 40€ in cash a month**
- **Assets:** QQQ, MSCI, GLD, VOO.
- Simulates with **Monte Carlo**. Included a overlap percentage of these select tickers and a final 'worst-case' scenario of α **Value at Risk (VaR)**, and **Conditional VaR (CVaR)**.

---

## Backtesting Strategies

Testing trading strategies with historical data using the `backtesting.py` framework.

- **`RSIOptimisation`**:
  Buy when RSI < 30 (oversold), close when RSI > 70 (overbought). Includes parameter optimisation with the Sharpe Ratio.

- **`RSISwingStrat`**:
  Similar to the 'RSIOptimisation', but flips long ↔ short. Always in the market, betting on both upside and downside swings.

- **`MomentumTrendStrat`**:
  Combines RSI with trend filters (stacked moving averages: Price > MA10 > MA20 > MA50 > MA100). Enters only when both momentum and trend align. Exits on a breakdown below the 10-day MA.

- **`BBMeanReversion`**:
  Uses Bollinger Bands. Buys when price bounces above the lower band, sells when it breaks down from the upper band.

Each strategy includes parameter tuning and visualisation of equity and performance metrics.

---

## 💸 Pricing Models

Models for option pricing and risk — e.g., Black-Scholes, Monte Carlo, and binomial trees.

- **`BinomialOptionPricing`**: Implements a multi-period binomial tree model for option valuation.
- **`BlackScholesPricing`**: Implements the closed-form Black-Scholes-Merton formula for pricing European options.
