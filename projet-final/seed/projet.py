"""
Final integrative project (skeleton)
=====================================

Time Series Analysis -- Esprit School of Business
Author : <your name>

Pipeline to complete: descriptive stats -> decomposition -> ACF/PACF
-> ADF/KPSS -> ARMA -> GARCH -> conditional VaR -> Kupiec back-test.

Reproducibility: numpy.random.seed(42).
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from scipy import stats
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.stattools import adfuller, kpss
# from statsmodels.stats.diagnostic import het_arch, acorr_ljungbox
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from arch import arch_model

np.random.seed(42)


def load_prices(path="../data/stock_prices.csv"):
    df = pd.read_csv(path, parse_dates=["Date"])
    return df["Date"].to_numpy(), df["Price"].to_numpy(float)


# =====================================================================
# Part A -- Basic statistics on returns
# =====================================================================

def part_A(P):
    # TODO : compute r_t = log(P_t / P_{t-1})
    # TODO : sample mean, sd, skewness, excess kurtosis
    # TODO : 95% CI for the mean (Student t)
    # TODO : test H0: mu = 0
    # TODO : Jarque-Bera normality test
    # TODO : histogram + Gaussian fit
    pass


# =====================================================================
# Part B -- Decomposition
# =====================================================================

def part_B(P, r):
    # TODO : centred MA on P_t with k = 50
    # TODO : OLS on log(P_t) = beta_0 + beta_1 t
    # TODO : compare beta_1 with the sample mean of r_t
    # TODO : plot P_t + MA + exponential trend
    pass


# =====================================================================
# Part C -- Stationarity diagnostics
# =====================================================================

def part_C(P, r):
    # TODO : ACF of log P_t (slow decay), of r_t (~ flat), of r_t^2 (clustering)
    # TODO : Ljung-Box on r_t at m in {10, 20}
    # TODO : Ljung-Box on r_t^2 at m in {10, 20}
    pass


# =====================================================================
# Part D -- Unit-root testing
# =====================================================================

def part_D(P, r):
    # TODO : adfuller(log P, regression="ct"), adfuller(r, regression="c")
    # TODO : kpss(log P, regression="ct"), kpss(r, regression="c")
    # TODO : combine -> ADF/KPSS matrix; conclude that log P ~ I(1), r ~ I(0)
    pass


# =====================================================================
# Part E -- ARMA modelling
# =====================================================================

def part_E(r):
    # TODO : ARMA(0,0,0), (1,0,0), (0,0,1) by MLE
    # TODO : compare AIC, BIC, Ljung-Box(24)
    # TODO : justify why constant-mean is selected on daily returns
    pass


# =====================================================================
# Part F -- GARCH(1,1) + VaR
# =====================================================================

def part_F(r):
    # TODO : Engle LM on r_t at q in {5, 10, 20}
    # TODO : fit GARCH(1,1) (multiply r by 100 for numerical stability)
    # TODO : recover alpha_0, alpha_1, beta_1, mu and check alpha_1 + beta_1 < 1
    # TODO : standardised residuals z_t -> Engle LM (must be NOT rejected)
    # TODO : conditional VaR(1%, 5%) vs unconditional
    pass


# =====================================================================
# Part G -- Kupiec back-test
# =====================================================================

def part_G(r, alpha=0.05, n_test=250, refit_every=10):
    # TODO : split into train/test
    # TODO : rolling re-fit every 10 days; predict 1-day VaR
    # TODO : count exceedances X in the n_test test days
    # TODO : compute LR_Kupiec = -2 log[ ((1-a)^(N-X) a^X) / ((1-pi)^(N-X) pi^X) ]
    # TODO : compare to chi^2_1 critical value 3.841
    pass


if __name__ == "__main__":
    dates, P = load_prices()
    r = part_A(P)
    part_B(P, r)
    part_C(P, r)
    part_D(P, r)
    part_E(r)
    part_F(r)
    part_G(r, alpha=0.05, n_test=250, refit_every=10)
