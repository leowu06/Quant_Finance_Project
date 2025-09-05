import numpy as np
import pandas as pd
import yfinance as yf
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

# Monthly Log Returns
tickers = ['QQQ', 'MSCI', 'GLD', 'VOO']
years = 15

endDate = datetime.today()
startDate = endDate - timedelta(days = years*12)

adjClosedDf = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start = startDate, end = endDate)
    adjClosedDf[ticker] = data['Close']

monthlyPrices = adjClosedDf.resample('M').last()
monthlyLogReturns = np.log(monthlyPrices / monthlyPrices.shift(1)).dropna()

# Preliminary info
weights = np.array([2/(2+3+3+5), 3/(2+3+3+5), 3/(2+3+3+5), 5/(2+3+3+5)])
covMatrix = monthlyLogReturns.cov()
assetVol = monthlyLogReturns.std() * np.sqrt(12) 
annualPortVol = np.sqrt(np.dot(weights.T, np.dot(covMatrix * 12, weights)))   # Stand Dev
monthlyPortVol = annualPortVol / np.sqrt(12)

# Calculate the Overlap percentage for Diversification
uncorrelatedVar = np.sum((assetVol*weights)**2)
overlapVar = 1 - (uncorrelatedVar/annualPortVol**2)

print(f"Portfolio Volatility: {annualPortVol:.4f}")
print(f"Overlap Percentage: {overlapVar*100:.2f}%")

# Simulate an active portfolio with DCA for 21 years (until 40)
years = 21
monthlyInvestment = 40
initialValue = 1600
expectedMonthlyLogReturn = monthlyLogReturns.mean()@weights 
expectedMonthlyReturn = np.exp(expectedMonthlyLogReturn)

def randomZScore():
    return np.random.standard_t(df=3)  # df=3 for heavy tails

def annualDCA(value,monthlyInvestment,expectedMonthlyReturn):
    result = value
    for i in range(12):
        randomness = randomZScore() * monthlyPortVol
        result = (result + monthlyInvestment) * (expectedMonthlyReturn + randomness)
    return result

#def scenarioGainLoss(initialValue, monthlyInvestment, expectedMonthlyReturn, annualPortVol, zScore):
    randomness = zScore * annualPortVol
    annualreturn = annualDCA(initialValue, monthlyInvestment, expectedMonthlyReturn)
    return (randomness + annualreturn) * initialValue

# Simulations
simulations = 1000
paths = np.zeros((years, simulations))
paths[0,:] = initialValue
for s in range(simulations):
    value = initialValue
    for y in range(1,years):
        paths[y,s] = annualDCA(value,monthlyInvestment,expectedMonthlyReturn)
        value = paths[y,s]

# Calculating the Value at Risk
finalPortfolio = paths[-1,:]
gainsLosses = finalPortfolio -  initialValue # can be negative or positive
alpha = 0.9
VaR = np.percentile(gainsLosses, 100*(1-alpha))
cutOff = VaR + initialValue
cVar = np.mean(finalPortfolio[finalPortfolio<= VaR])
cutoff2 = cVar + initialValue

mean = np.mean(finalPortfolio)
noInvestment = initialValue + 40*12*20

plt.plot(paths[:, :100])  # first 100 paths
plt.title("Monte-Carlo Portfolio Paths (100 of 1 000)")
plt.xlabel("Year")
plt.ylabel("Portfolio Value (€)")
plt.axhline(noInvestment, color = 'blue', linewidth = 2, label = f"Portfolio just by saving 40 € monthly: {noInvestment:.0f} €")
plt.axhline(mean, color = 'green', linewidth = 2, label = f"Average Portfolio at 40 years of age: {mean:.0f} €")
plt.axhline(cutOff, color = 'red', linewidth = 2, label = f"VaR ({alpha:.0%}) = {-VaR:.0f} €")
plt.axhline(cutoff2, color = 'yellow', linewidth = 2, label = f"CVaR = {cVar:.0f} €")
plt.legend()
plt.grid(True)
plt.show()


