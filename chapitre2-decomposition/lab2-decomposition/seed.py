"""
Lab 2 — Decomposition (student skeleton)
=========================================

Time Series Analysis — Chapter 2
Author : Aymen Ben Brik
Email  : aymen.benbrik@esprit.tn
Esprit School of Business
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)


# =====================================================================
# Exercise 1 — Synthetic series
# =====================================================================

def generate_synthetic(T=240, seed=42):
    """Y_t = 20 + 0.05*t + 5*sin(2 pi t / 12) + N(0, 1).
    Returns t (1..T), Y, T_true, S_true, eps_true."""
    # TODO
    raise NotImplementedError


def exercise1():
    # TODO : 4-panel figure (Y, T, S, eps)
    pass


# =====================================================================
# Exercise 2 — Trend
# =====================================================================

def centred_ma(y, k):
    """Centred MA of window 2k+1. Returns array of same length with NaN at edges."""
    # TODO
    raise NotImplementedError


def exercise2():
    # TODO : MA(k=6), linear regression, LOESS — compute RMSE vs truth
    pass


# =====================================================================
# Exercise 3 — Seasonality
# =====================================================================

def seasonal_average(detrended, d=12):
    """Return array of d seasonal indices, recentered to sum to 0."""
    # TODO
    raise NotImplementedError


def exercise3():
    # TODO : 3 methods (averaging, dummies, Fourier) on the synthetic
    pass


# =====================================================================
# Exercise 4 — Atlanta temperatures
# =====================================================================

def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    arr = np.loadtxt(path, skiprows=1)
    return arr[:, 1:13].flatten()


def exercise4():
    y = load_atlanta_monthly()
    # TODO : full decomposition workflow on Atlanta
    pass


# =====================================================================
# Exercise 5 — Bonus : multiplicative
# =====================================================================

def exercise5():
    # TODO : multiplicative synthetic, compare additive vs log-additive
    pass


# =====================================================================
if __name__ == "__main__":
    exercise1(); exercise2(); exercise3(); exercise4(); exercise5()
