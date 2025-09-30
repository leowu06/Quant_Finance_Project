from bs import bs_price, bs_greeks
import numpy as np

S = 100 
K = 100
r = 0.05
q = 0.0
sigma = 0.2
T = 1

def monte_carlo_paths(S0, mu, sigma, T, steps,n):
    """
    Simulate n stock price paths with Geometric Brownian Motion.
    
    Parameters
    ----------
    S0 : float
        Initial stock price
    mu : float
        Drift (expected return)
    sigma : float
        Volatility (standard deviation)
    T : float
        Time (in years)
    steps : int
        Number of time steps
    n : int
        Number of simulated paths

    Returns:
        Simulated paths of shape (n, steps+1)
    """
    dt = T/steps
    paths = np.zeros((n,steps + 1))
    paths[:,0] = S0

    for t in range(1, steps + 1):
        Z = np.random.normal(0,1,n)
        paths[:,t] = paths[:,t-1] * np.exp((mu - 0.5*sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    return paths

# the Geometric-Brownian Motion is used to simulate random shocks assuming normal distributed random variable Z.