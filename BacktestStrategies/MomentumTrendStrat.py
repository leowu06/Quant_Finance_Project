from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import pandas as pd
import talib
from backtesting.lib import crossover, plot_heatmaps, resample_apply
import seaborn as sns
import matplotlib.pyplot as plt

def SMA(array, n):
    return pd.Series(array).rolling(n).mean()

class MomTrendStrat(Strategy):
    rsi_window1 = 30
    rsi_window2 = 30
    level = 70


    def init(self):
        self.dailyRsi = self.I(talib.RSI, self.data.Close, self.rsi_window1)   
        self.weeklyRsi = resample_apply('W-FRI', talib.RSI, self.data.Close, self.rsi_window2)
        self.ma10 = self.I(SMA, self.data.Close, 10)
        self.ma20 = self.I(SMA, self.data.Close, 20)
        self.ma50 = self.I(SMA, self.data.Close, 50)
        self.ma100 = self.I(SMA, self.data.Close, 100)

    def next(self):
        price = self.data.Close[-1]
        # If we don't already have a position, and
        # if all conditions are satisfied, enter long.
        if (not self.position and self.weeklyRsi[-1] > self.dailyRsi[-1] > self.level and
        price > self.ma10[-1] > self.ma20[-1] > self.ma50[-1] > self.ma100[-1]): 
            # Buy at market price on next open, but do
            # set 8% fixed stop loss.
            self.buy(sl=.92 * price)
        # If the price closes 2% or more below 10-day MA
        # close the position, if any.
        elif price < .98 * self.ma10[-1]:
            self.position.close()
    

backtest = Backtest(GOOG, MomTrendStrat, commission=0.002)
stats = backtest.optimize(rsi_window1 = range(10, 35, 5),
                  rsi_window2 = range(10, 35, 5),
                  level = range(30, 80, 10))
print(stats)
print( "best parameteres: ")
print(stats._strategy)
