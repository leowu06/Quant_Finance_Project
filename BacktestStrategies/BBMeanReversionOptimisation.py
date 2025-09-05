from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas as pd
import talib
import numpy as np

class BBMeanReversion(Strategy):
    time = 10
    dev_up = 2
    dev_down = 2
    def init(self):
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod = self.time, nbdevup = self.dev_up, nbdevdn = self.dev_down, matype= 0
        )

    def next(self):
        price = self.data.Close[-1]

        # Buy signal, when price crosses from under the lower Bollinger Band
        if (not self.position and self.data.Close[-2] < self.bb_lower[-2] 
           and price > self.bb_lower[-1]):
            self.buy(sl = 0.92 * price)
        # Sell signal, price crosses DOWN below upper band
        elif (self.position and self.data.Close[-2] > self.bb_upper[-2]
              and price < self.bb_upper[-1]):
            self.position.close()

bt = Backtest(GOOG, BBMeanReversion, commission=0.002)
stats = bt.optimize(
    time = range(10, 40, 5),
    dev_up = list(np.arange(1.5,2.9,0.2)),
    dev_down = list(np.arange(1.5,2.6,0.2)),
    maximize= 'Sharpe Ratio'
)
print(stats)
print("Optimal parameters:")
print(stats._strategy)