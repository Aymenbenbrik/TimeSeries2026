"""
Lab 3 — ACF / PACF / Ljung-Box (skeleton)
==========================================

Time Series Analysis — Chapter 3
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)


# =====================================================================
# Exercise 1 — White noise
# =====================================================================

def exercise1():
    # TODO : simulate WN(0,1) length 500, plot ACF up to lag 30
    # TODO : count lags outside Bartlett band, compare with 5% expected
    pass


# =====================================================================
# Exercise 2 — AR(1)
# =====================================================================

def simulate_ar1(phi, T=500, sigma=1.0, seed=42):
    """Simulate X_t = phi X_{t-1} + eps_t."""
    # TODO
    raise NotImplementedError


def exercise2():
    # TODO : phi in {0.3, 0.7, -0.7, 0.95}, plot ACF + theoretical
    pass


# =====================================================================
# Exercise 3 — MA(1)
# =====================================================================

def simulate_ma1(theta, T=500, sigma=1.0, seed=42):
    """Simulate X_t = eps_t + theta * eps_{t-1}."""
    # TODO
    raise NotImplementedError


def exercise3():
    # TODO : theta in {0.5, -0.5, 0.9}, plot ACF
    pass


# =====================================================================
# Exercise 4 — Atlanta
# =====================================================================

def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    arr = np.loadtxt(path, skiprows=1)
    return arr[:, 1:13].flatten()


def exercise4():
    y = load_atlanta_monthly()
    # TODO : raw ACF up to lag 60
    # TODO : decompose (centred MA + seasonal averaging)
    # TODO : ACF/PACF of residual
    pass


# =====================================================================
# Exercise 5 — Ljung-Box
# =====================================================================

def exercise5():
    # TODO : Ljung-Box on Atlanta residual at m in {12, 24, 36}
    # TODO bonus : Ljung-Box on white noise of Exercise 1
    pass


if __name__ == "__main__":
    exercise1(); exercise2(); exercise3(); exercise4(); exercise5()
