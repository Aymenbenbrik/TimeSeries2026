"""
Lab 6 -- ARCH effects, GARCH and VaR (skeleton)
================================================

Time Series Analysis -- Chapter 6
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from scipy import stats
# from statsmodels.stats.diagnostic import het_arch
# from arch import arch_model

np.random.seed(42)


# =====================================================================
# Exercise 1 -- Volatility clustering
# =====================================================================

def exercise1():
    # TODO : load data/synthetic_returns.csv
    # TODO : plot r_t, ACF of r_t, ACF of r_t^2
    pass


# =====================================================================
# Exercise 2 -- Engle LM
# =====================================================================

def exercise2():
    # TODO : het_arch(r, nlags=q) for q in {5, 10, 20}
    pass


# =====================================================================
# Exercise 3 -- ARCH(q)
# =====================================================================

def exercise3():
    # TODO : arch_model(r, vol="ARCH", p=q) for q in {1, 3, 5}
    # TODO : print alphas, sum(alphas), AIC
    pass


# =====================================================================
# Exercise 4 -- GARCH(1,1)
# =====================================================================

def exercise4():
    # TODO : arch_model(r, vol="GARCH", p=1, q=1, mean="Constant")
    # TODO : extract mu, alpha_0, alpha_1, beta_1; check alpha_1 + beta_1
    # TODO : compute implied unconditional variance, compare with sample
    pass


# =====================================================================
# Exercise 5 -- Standardised residual diagnostics
# =====================================================================

def exercise5():
    # TODO : z_t = resid / conditional_volatility
    # TODO : ACF of z_t and z_t^2
    # TODO : Engle LM on z_t^2
    # TODO : QQ-plot
    pass


# =====================================================================
# Exercise 6 -- Forecast and VaR
# =====================================================================

def exercise6():
    # TODO : res.forecast(horizon=30)
    # TODO : closed-form check sigma2_{T+h} = sigma2 + (a1+b1)^(h-1)(sigma2_{T+1} - sigma2)
    # TODO : VaR at 1% and 5%, conditional vs unconditional
    pass


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
    exercise6()
