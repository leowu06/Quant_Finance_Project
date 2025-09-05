from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import talib
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import seaborn as sns
import matplotlib.pyplot as plt

class RSIOscillator(Strategy):

    upperBound = 70
    lowerBound = 30
    RSIWindow = 14

    def init(self):
        self.dailyRsi = self.I(talib.RSI, self.data.Close, self.RSIWindow)   
        # Initialize the RSI indicator using talib's RSI function over the Close prices with a 14-period window.
        # self.I registers it so it updates automatically during backtesting.

    def next(self):
         # Check if the RSI just crossed *above* the defined upper bound.
        # If so, close any open position — assuming RSI signals overbought conditions.
        if crossover(self.dailyRsi, self.upperBound):
            if self.position.is_long:
                self.position.close()
                self.sell(size=0.5)
        elif crossover(self.lowerBound, self.dailyRsi):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy()

def optimFunc(series):
    if series['# Trades'] < 10:
        return -1
    return series['Equity Final [$]']/ series['Exposure Time [%]']

bt = Backtest(GOOG, RSIOscillator, cash= 10000)

stats = bt.run()
print(stats)

