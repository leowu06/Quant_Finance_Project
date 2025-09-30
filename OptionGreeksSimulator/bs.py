import numpy as np
from scipy.stats import norm
from math import log, sqrt, exp

def _d1_d2(S, K, r, q, sigma, T):
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return d1, d2
def bs_price(S, K, r, q, sigma, T, option="call"):
    d1 = (log(S/K) + (r - q + 0.5*sigma*sigma)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    if option == "call":
        return S*exp(-q*T)*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    else:
        return K*exp(-r*T)*norm.cdf(-d2) - S*exp(-q*T)*norm.cdf(-d1)
    
def bs_greeks(S, K, r, q, sigma, T, option='Call'):
    d1, d2 = _d1_d2(S, K, r, q, sigma, T)
    pdf_d1 = norm.pdf(d1)
    delta = (np.exp(-q*T) * norm.cdf(d1) if option=='Call' else np.exp(-q*T) * (norm.cdf(d1)-1))
    gamma = np.exp(-q*T) * pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * np.exp(-q*T) * pdf_d1 * np.sqrt(T)
    theta_call = (-S * pdf_d1 * sigma * np.exp(-q*T) / (2*np.sqrt(T))
                  - r*K*np.exp(-r*T)*norm.cdf(d2) + q*S*np.exp(-q*T)*norm.cdf(d1))
    theta_put = (-S * pdf_d1 * sigma * np.exp(-q*T) / (2*np.sqrt(T))
                 + r*K*np.exp(-r*T)*norm.cdf(-d2) - q*S*np.exp(-q*T)*norm.cdf(-d1))
    rho_call = K*T*np.exp(-r*T)*norm.cdf(d2)
    rho_put = -K*T*np.exp(-r*T)*norm.cdf(-d2)
    theta = theta_call if option=='Call' else theta_put
    rho = rho_call if option=='Call' else rho_put
    return {'delta': delta, 'gamma': gamma, 'vega': vega/100, 'theta': theta/365, 'rho': rho/100}


if __name__ == "__main__":
    # quick test
    S = 100      # stock price today
    K = 100      # strike price
    r = 0.05     # 5% risk-free rate
    q = 0.0      # no dividend
    sigma = 0.2  # 20% annual volatility
    T = 1        # 1 year to expiry
    print("Price:", bs_price(S,K,r,q,sigma,T))
    print("Greeks:", bs_greeks(S,K,r,q,sigma,T))