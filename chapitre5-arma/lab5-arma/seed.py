"""
Lab 5 -- ARMA estimation and forecasting (skeleton)
====================================================

Time Series Analysis -- Chapter 5
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import matplotlib.pyplot as plt
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.stattools import acf, pacf
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from statsmodels.stats.diagnostic import acorr_ljungbox

np.random.seed(42)


# =====================================================================
# Exercise 1 -- AR(2)
# =====================================================================

def exercise1():
    # TODO : simulate X_t = 0.6 X_{t-1} - 0.3 X_{t-2} + eps_t  (T=500)
    # TODO : plot series, ACF, PACF up to lag 20
    # TODO : fit ARIMA(p, 0, 0) for p in {1, 2, 3}, compare AIC/BIC/LB
    pass


# =====================================================================
# Exercise 2 -- MA(1)
# =====================================================================

def exercise2():
    # TODO : simulate X_t = eps_t + 0.7 eps_{t-1}  (T=500)
    # TODO : check empirical rho(1) ~ 0.470
    # TODO : fit ARIMA(0,0,1) and (1,0,0); compare AIC
    pass


# =====================================================================
# Exercise 3 -- ARMA(1,1)
# =====================================================================

def exercise3():
    # TODO : simulate X_t = 0.5 X_{t-1} + eps_t + 0.4 eps_{t-1}  (T=500)
    # TODO : fit (1,0,0), (0,0,1), (1,0,1), (2,0,2)
    # TODO : show that (1,0,1) wins on BIC, (2,0,2) over-fits
    pass


# =====================================================================
# Exercise 4 -- Box-Jenkins on Atlanta residual
# =====================================================================

def exercise4():
    # TODO : load AvTempAtlanta.txt
    # TODO : decompose (centred MA k=6 + seasonal averaging)
    # TODO : fit AR(1), AR(2), MA(1), ARMA(1,1), ARMA(2,1)
    # TODO : pick best by (AIC, BIC, LB) triplet
    pass


# =====================================================================
# Exercise 5 -- Forecasting
# =====================================================================

def exercise5():
    # TODO : 24-step forecast on the chosen model
    # TODO : plot in-sample fit + forecast with 95% CI
    # TODO bonus : 80/20 hold-out, RMSE
    pass


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
