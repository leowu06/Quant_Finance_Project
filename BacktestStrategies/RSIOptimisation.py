from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import talib
from backtesting.lib import crossover, plot_heatmaps
import seaborn as sns
import matplotlib.pyplot as plt

class RSIOscillator(Strategy):

    upperBound = 70
    lowerBound = 30
    RSIWindow = 14

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.RSIWindow)   
        # Initialize the RSI indicator using talib's RSI function over the Close prices with a 14-period window.
        # self.I registers it so it updates automatically during backtesting.

    def next(self):
         # Check if the RSI just crossed *above* the defined upper bound.
        # If so, close any open position — assuming RSI signals overbought conditions.
        if crossover(self.rsi, self.upperBound):
            self.position.close()
        elif crossover(self.lowerBound, self.rsi):
            self.buy(size=0.5)  # Buy 50% of possible position

def optimFunc(series):
    if series['# Trades'] < 10:
        return -1
    return series['Equity Final [$]']/ series['Exposure Time [%]']

bt = Backtest(GOOG, RSIOscillator, cash= 10000)

stats, heatmap = bt.optimize(upperBound = range(55,85,5), lowerBound = range(10,45,5), RSIWindow = range(10,45,5), maximize='Sharpe Ratio',
                    constraint= lambda param: param.upperBound > param.lowerBound, return_heatmap = True)
# optimising the backtesting strategy with parameters/variables, upperbound lower bound. maximising the Sharpe, with 
# constraint lambda: upper > lower


hm = heatmap.groupby(['upperBound', 'lowerBound']).mean().unstack()


sns.heatmap(hm, cmap = 'plasma')
plot_heatmaps(heatmap, agg='mean')

