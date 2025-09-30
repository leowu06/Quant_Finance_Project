# Finance and Derivatives

This repository contains a collection of projects in **Portfolio Analysis, Strategy Backtesting** and **Options Greeks Simulation**. These were coded through Python, so I included **README** files in each folder with screenshots of each functionality and visual graphs, so the reader can interpret the purpose.

Furthermore, I have made a 3-tab **Streamlit app** that allows the user to interact with the input and simulation parameters (Options): [App (Streamlit UI)](OptionGreeksSimulator/README.md).

---

## ([Portfolio Analysis & Simulation](https://github.com/leowu06/Quant_Finance_Project/tree/1e122639db5233b4c7780bbd1587d137db01a67f/Portfolio%20Analysis%20%26%20Simulation)).
For the main file "PortfolioSimulationMonteCarlo" I simulated **21 years of investing** in [QQQ, MSCI, GLD, VOO] 40€ a month with an initial 1600€ vs **saving 40€ in cash a month**
- **Assets:** QQQ, MSCI, GLD, VOO.
- Simulates with **Monte Carlo**. Included a overlap percentage of these select tickers and a final 'worst-case' scenario of α **Value at Risk (VaR)**, and **Conditional VaR (CVaR)**.

---

## [Backtesting Strategies](https://github.com/leowu06/Quant_Finance_Project/tree/ab3f402c3db01ad1648f234dc10e923deeed267c/BacktestStrategies)

Tested trading strategies with historical data on 'GOOGL' using the `backtesting.py` framework. For example:

- **`MomentumTrendStrat`**:
  Combines RSI with trend filters (stacked moving averages: Price > MA10 > MA20 > MA50 > MA100). Entered position only when both momentum and trend aligned. Exits when below the 10-day MA.

- **`BBMeanReversion`**:
  Uses Bollinger Bands based on mean-reverting behaviour of stock price. It buys when price bounces above the lower band, sells when it comes down from the upper band.

Each strategy includes parameter optimisation and visualisation of performance metrics.

---

## [([Option Greeks Simulator]) (https://github.com/leowu06/Quant_Finance_Project/tree/7a385ce9a94b2fefbab622d81db491be66875a93/OptionGreeksSimulator)]
In my main project I showcased three tabs on Options Greeks, their behaviour and simulation of how traders base investments on greeks.
- **`Greeks Explorer`**: Implements the functionality of Black-Scholes formula and includes sliders for user input. There is option to graph the behaviour of select greek vs price of underlying
- **`IV-Smile`**: Exposes the assumption Black-Scholes has on flat volatility, by extracting data on option chains we visualise that volatility is higher OTM and deep ITM than ATM - reveals traders take on a hedge against market crash.
- **`Dynamic Delta-Hedging`**: To reduce directional risk of owning options, traders hedge by trading the underlying in the opposite direction. Due to gamma's effect re-hedging or so dynamic hedging is needed which is costly.
