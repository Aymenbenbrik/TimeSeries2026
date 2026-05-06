"""
Lab 4 -- Unit roots and ARIMA (skeleton)
=========================================

Time Series Analysis -- Chapter 4
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import matplotlib.pyplot as plt
# from statsmodels.tsa.stattools import adfuller, kpss, acf
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.stats.diagnostic import acorr_ljungbox

np.random.seed(42)


# =====================================================================
# Exercise 1 -- TS vs DS
# =====================================================================

def exercise1():
    # TODO : simulate Y_t = 0.05 t + eps_t  (TS)
    # TODO : simulate Z_t = Z_{t-1} + 0.05 + eta_t  (DS, RW+drift)
    # TODO : plot both, then plot OLS-detrended residuals
    pass


# =====================================================================
# Exercise 2 -- ADF
# =====================================================================

def exercise2():
    # TODO : adfuller on Y_t (regression="ct"), Z_t (regression="c"), dZ_t
    # TODO : print stat, p-value, critical values, decision
    pass


# =====================================================================
# Exercise 3 -- KPSS
# =====================================================================

def exercise3():
    # TODO : kpss on Y_t (regression="ct"), Z_t (regression="c")
    # TODO : combine with ADF to fill the 2x2 matrix
    pass


# =====================================================================
# Exercise 4 -- Differencing
# =====================================================================

def exercise4():
    # TODO : compute dZ_t = Z_t - Z_{t-1}
    # TODO : plot ACF of Z_t and dZ_t up to lag 20
    # TODO : adfuller + kpss on dZ_t
    pass


# =====================================================================
# Exercise 5 -- SARIMA on log SouvenirSales
# =====================================================================

def exercise5():
    # TODO : load data/SouvenirSales.csv, take log
    # TODO : adfuller + kpss with regression="ct"
    # TODO : fit SARIMAX(order=(0,1,1), seasonal_order=(0,1,1,12))
    # TODO : Ljung-Box on residuals at lag 24
    # TODO : 12-month forecast with 95% CI
    pass


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
