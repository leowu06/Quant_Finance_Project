# Backtesting Strategies

---



This directory contains Python files for backtesting various  trading strategies. I included screenshots of outputs and conclusion.

## **Momentum-Trend Strategy**

**Self-defined indicator:** Moving average, rolling mean on a panda table.

**Strategy Logic:**
Opens a position when two conditions are met:
1.  **Momentum:** Daily RSI is lagging behind weekly RSI which is already signalling strong enough.
2.  **Trend:** Price > MA10 > MA20 > MA50 > MA100. This is the “uptrend alignment,” requiring all moving averages to be stacked upward. The trend is verified.

**Exit Condition:** Exit if there is a 2% drop below the 10-day MA.

<img width="1652" height="775" alt="image" src="https://github.com/user-attachments/assets/4c020da3-7af0-4524-b3dd-9bae95676de5" />


Duration                   3116 days 00:00:00, 
Exposure Time [%]                    26.16387, 
Equity Final [$]                   22339.8475, 
Equity Peak [$]                   22937.61394, 
Commissions [$]                     1693.5681, 
**Return [%]                          123.39848, 
Buy & Hold Return [%]                313.3036**

The strategy obtained significantly lower returns than buy-and-hold (123% vs 313%), but did so while being exposed to the market only ~25% of the time. This illustrates the trade-off: overall reduced exposure leads to lower risk exposure, but also limits total return.
---

## **RSIOscillator**

**Strategy Logic:**
- **Buy:** When the RSI index shows the market is oversold (<= 30). Buy 50% of the position with our current cash.
- **Sell/Close:** Close positions when RSI is above 70.

**Parameter Optimisation:**
- The bounds (30/70) were optimised based on historic data with the **Sharpe Ratio** as the objective function.
- Among the trades, score them based on money made per unit of time spent in the market.

  <img width="401" height="431" alt="image" src="https://github.com/user-attachments/assets/1538de80-ffc6-4ec6-b375-42347c925675" />


Heatmap of RSIupper, RSIlower as a function of 'Sharpe ratio'.

---

## **RSI-Swing Strategy**

**Strategy Logic:**
- Similar to the regular RSI strategy, but when closing a long position, also **open a short** position, predicting the market is going down. The same logic is applied to the upside for short covering.

---

## **Bollinger-Band Mean Reversion**

**Strategy Logic:**
Uses Bollinger Bands to capture mean reversion.
- **Buy Signal:** When price crosses back **above** the **lower** Bollinger Band. A stop-loss at 8% below the entry price protects downside.
- **Sell Signal:** When price crosses back **below** the **upper** Bollinger Band (overbought reversal).

**Parameter Optimisation:**
- Window of the moving average.
- Deviations of the bounds, which control the bandwidth of the Bollinger Bands.
- The objective function for optimisation is maximising the **Sharpe Ratio**.
