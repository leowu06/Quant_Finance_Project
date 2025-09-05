# 📂 Finance & Trading Projects

This repository collects projects I have been working on around finance, trading strategies, and portfolio analysis in Python. Each folder consists of a different topic—from backtesting technical trading strategies and simulating long-term investing to option pricing models.

---

## 📊 Portfolio Simulation & Analysis

Monte Carlo simulation of a long-term portfolio with monthly contributions (Dollar-Cost Averaging).

- **Assets:** QQQ, MSCI, GLD, VOO.
- **Strategy:** Simulates investing **40 €/month** + an **initial 1600 €** until age 40.
- **Features:** Includes diversification overlap analysis, portfolio volatility, **Value at Risk (VaR)**, and **Conditional VaR (CVaR)**.
- **Output:** Models thousands of random portfolio paths and compares them to simply saving the money.
- **Goal:** Shows how small, regular investments can grow (and what the risks look like) under realistic, fat-tailed market randomness.

---

## 🤖 Backtesting Strategies

Testing trading strategies with historical data using the `backtesting.py` framework.

- **`RSIOptimisation`**:
  Buy when RSI < 30 (oversold), close when RSI > 70 (overbought). Includes parameter optimisation with the Sharpe Ratio.

- **`RSISwingStrat`**:
  Similar to the oscillator, but flips long ↔ short. Always in the market, betting on both upside and downside swings.

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
