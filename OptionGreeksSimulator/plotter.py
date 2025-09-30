from simulator import monte_carlo_paths
import matplotlib.pyplot as plt
from typing import Callable, Tuple
import numpy as np
from bs import bs_greeks, bs_price

def compute_series_vs_spot(
        series_name,
        S,K,r,q,sigma,T, option_type,
        span = 0.3, n=51, mode = "level" # mode: "change" or "level"
):
    S_grid = np.linspace((1-span) * S, (1+span) * S, n)
    S_grid = np.clip(S_grid, 1e-8, None)

    prices, deltas, gammas, vegas, thetas, rhos = [], [], [], [], [], []
    for dollar in S_grid:
        p = bs_price(dollar, K, r, q, sigma, T, option_type)
        g = bs_greeks(dollar,K,r,q,sigma,T,option_type)
        prices.append(p)
        deltas.append(g['delta'])
        gammas.append(g['gamma'])
        vegas.append(g['vega'])
        thetas.append(g['theta'])
        rhos.append(g['rho'])

    series_map = {
        "Price": (prices, "Option Prices"),
        "Delta": (deltas, "Delta"),
        "Gamma": (gammas, "Gamma"),
        "Vega (per 1% σ)": (vegas, "Vega (per 1% σ)"),
        "Theta (per day)": (thetas, "Theta (per day)"),
        "Rho (per 1% r)": (rhos, "Rhos (per 1% r)")
    }
    y_vals, y_label = series_map[series_name]

    if mode == "change":
        base_p = bs_price(S, K, r, q, sigma, T, option=option_type)
        base_g = bs_greeks(S, K, r, q, sigma, T, option_type)
        base_map = {
            "Price": base_p,
            "Delta": base_g["delta"],
            "Gamma": base_g["gamma"],
            "Vega (per 1% σ)": base_g["vega"],
            "Theta (per day)": base_g["theta"],
            "Rho (per 1% r)": base_g["rho"],
        }
        base = base_map[series_name]
        y_vals = [v - base for v in y_vals]
        y_label = f"Δ {y_label} (vs S={S:.2f})"

    return S_grid, y_vals, y_label


def plot_gbm_paths(paths, title="GBM Monte Carlo Paths", n_paths_to_plot=10):
    """
    Plot a first n simulated paths from a Monte Carlo simulation.
    
    paths: np.array of shape (n_steps+1, n_paths)
    n_paths_to_plot: int, how many paths to show
    """
    n_paths_to_plot = min(n_paths_to_plot, paths.shape[1]) # makes it so that we don't try to plot more than we have
    plt.figure(figsize=(8,5))
    for i in range(n_paths_to_plot):
        plt.plot(paths[:, i], lw=1)
    plt.xlabel("Time step")
    plt.ylabel("Price")
    plt.title(title)
    plt.grid(True)
    plt.show()

def plot_greek_vs_variable(variable_values, greek_values, variable_name="Underlying Price", greek_name="Delta", title=None):
    """
    Plot any Greek vs a variable (price, vol, time, etc.)
    """
    plt.figure(figsize=(7,4))
    plt.plot(variable_values, greek_values, marker='o')
    plt.xlabel(variable_name)
    plt.ylabel(greek_name)
    if title is None:
        title = f"{greek_name} vs {variable_name}"
    plt.title(title)
    plt.grid(True)
    plt.show()


