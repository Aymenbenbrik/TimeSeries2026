"""
Lab 4 -- Unit roots and ARIMA (reference solution)
==================================================

Time Series Analysis -- Chapter 4 (Non-stationarity)
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss, acf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
np.random.seed(42)


# =====================================================================
# Helpers
# =====================================================================

def report_adf(name, y, regression="c"):
    stat, pval, lag, n, crit, _ = adfuller(y, regression=regression)
    decision = "REJECT H0 (stationary)" if pval < 0.05 else "fail to reject H0 (unit root)"
    print(f"  ADF on {name:<22} reg={regression}: "
          f"stat={stat:+.3f}, p={pval:.4f}, "
          f"crit5%={crit['5%']:+.3f} -> {decision}")
    return stat, pval


def report_kpss(name, y, regression="c"):
    stat, pval, lag, crit = kpss(y, regression=regression, nlags="auto")
    decision = "REJECT H0 (unit root)" if pval < 0.05 else "fail to reject H0 (stationary)"
    print(f"  KPSS on {name:<21} reg={regression}: "
          f"stat={stat:+.3f}, p={pval:.4f}, "
          f"crit5%={crit['5%']:+.3f} -> {decision}")
    return stat, pval


# =====================================================================
# Exercise 1 -- TS vs DS by simulation
# =====================================================================

def exercise1():
    print("=" * 64)
    print("Exercise 1 -- Trend-stationary vs random walk with drift")
    print("=" * 64)
    T = 200
    rng = np.random.default_rng(42)
    t = np.arange(T)

    # TS : Y_t = 0.05 t + eps_t
    eps = rng.standard_normal(T)
    Y = 0.05 * t + eps

    # DS : Z_t = Z_{t-1} + 0.05 + eta_t
    eta = rng.standard_normal(T)
    Z = np.zeros(T)
    for k in range(1, T):
        Z[k] = Z[k - 1] + 0.05 + eta[k]

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    axes[0, 0].plot(Y, lw=0.8); axes[0, 0].set_title(r"TS : $Y_t = 0.05\,t + \varepsilon_t$")
    axes[0, 1].plot(Z, lw=0.8); axes[0, 1].set_title(r"DS : $Z_t = Z_{t-1} + 0.05 + \eta_t$")

    # Detrending by OLS
    A = np.column_stack([np.ones(T), t])
    bY, *_ = np.linalg.lstsq(A, Y, rcond=None); resY = Y - A @ bY
    bZ, *_ = np.linalg.lstsq(A, Z, rcond=None); resZ = Z - A @ bZ
    axes[1, 0].plot(resY, lw=0.8); axes[1, 0].set_title("TS residual after OLS detrend (~ WN)")
    axes[1, 1].plot(resZ, lw=0.8); axes[1, 1].set_title("DS residual after OLS detrend (still wanders)")
    for ax in axes.flat: ax.axhline(0, color="black", lw=0.5)
    plt.tight_layout()
    fig.savefig("lab4_ex1_ts_vs_ds.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  TS detrended residual std = {resY.std(ddof=1):.3f}")
    print(f"  DS detrended residual std = {resZ.std(ddof=1):.3f}  (much larger)")
    print("  -> figure lab4_ex1_ts_vs_ds.png")
    return Y, Z


# =====================================================================
# Exercise 2 -- ADF
# =====================================================================

def exercise2(Y, Z):
    print("=" * 64)
    print("Exercise 2 -- ADF test")
    print("=" * 64)
    report_adf("Y_t (TS)", Y, regression="ct")
    report_adf("Z_t (RW+drift)", Z, regression="c")
    dZ = np.diff(Z)
    report_adf("dZ_t = Z_t - Z_{t-1}", dZ, regression="c")
    return dZ


# =====================================================================
# Exercise 3 -- KPSS
# =====================================================================

def exercise3(Y, Z):
    print("=" * 64)
    print("Exercise 3 -- KPSS test")
    print("=" * 64)
    report_kpss("Y_t (TS)", Y, regression="ct")
    report_kpss("Z_t (RW+drift)", Z, regression="c")


# =====================================================================
# Exercise 4 -- Differencing the random walk
# =====================================================================

def exercise4(Z, dZ):
    print("=" * 64)
    print("Exercise 4 -- Differencing the random walk")
    print("=" * 64)
    rho_Z  = acf(Z,  nlags=20, fft=False)
    rho_dZ = acf(dZ, nlags=20, fft=False)
    print(f"  ACF of Z_t  at lags 1..5  : {np.round(rho_Z[1:6], 3)}")
    print(f"  ACF of dZ_t at lags 1..5  : {np.round(rho_dZ[1:6], 3)}")

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    axes[0].bar(range(21), rho_Z,  alpha=0.7); axes[0].set_title(r"ACF of $Z_t$ (RW)")
    axes[1].bar(range(21), rho_dZ, alpha=0.7); axes[1].set_title(r"ACF of $\Delta Z_t$ (~ WN)")
    for ax in axes:
        ax.axhline(0, color="black", lw=0.5)
        ax.axhline( 1.96/np.sqrt(len(Z)), color="red", ls="--", lw=0.5)
        ax.axhline(-1.96/np.sqrt(len(Z)), color="red", ls="--", lw=0.5)
    plt.tight_layout()
    fig.savefig("lab4_ex4_acf_diff.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab4_ex4_acf_diff.png")

    report_adf("dZ_t", dZ, regression="c")
    report_kpss("dZ_t", dZ, regression="c")


# =====================================================================
# Exercise 5 -- ARIMA / SARIMA on Souvenir sales
# =====================================================================

def load_souvenir(path="data/SouvenirSales.csv"):
    df = pd.read_csv(path)
    return np.log(df["Sales"].to_numpy(float))


def exercise5():
    print("=" * 64)
    print("Exercise 5 -- SARIMA on log(SouvenirSales)")
    print("=" * 64)
    if not os.path.exists("data/SouvenirSales.csv"):
        print("  [data file not found -- skipped]")
        return

    y = load_souvenir()
    print(f"  T = {len(y)}, log(sales) in [{y.min():.2f}, {y.max():.2f}]")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(y, lw=1.0); ax.set_title("log Souvenir Sales (1995-2001)")
    ax.set_xlabel("month index"); ax.grid(alpha=0.3)
    fig.savefig("lab4_ex5_logy.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ADF / KPSS on raw log series
    report_adf("log(y)", y, regression="ct")
    report_kpss("log(y)", y, regression="ct")

    # Fit SARIMA(0,1,1)(0,1,1)_12
    model = SARIMAX(y, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12),
                    enforce_stationarity=False, enforce_invertibility=False)
    fit = model.fit(disp=False)
    print("\n  SARIMA(0,1,1)(0,1,1)_12 fit:")
    print(f"    theta_1   = {fit.params[0]:+.4f}")
    print(f"    Theta_1   = {fit.params[1]:+.4f}")
    print(f"    sigma2    = {fit.params[2]:.4f}")
    print(f"    AIC       = {fit.aic:.2f}")
    print(f"    BIC       = {fit.bic:.2f}")

    # Ljung-Box on residuals
    resid = fit.resid[13:]   # drop first season + diff
    lb = acorr_ljungbox(resid, lags=[24], return_df=True)
    print(f"    Ljung-Box(24)  Q = {lb['lb_stat'].iloc[0]:.2f}, "
          f"p = {lb['lb_pvalue'].iloc[0]:.4f}")

    # Forecast 12 months
    fc_res = fit.get_forecast(steps=12)
    fc_mean = fc_res.predicted_mean
    fc_ci = fc_res.conf_int(alpha=0.05)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(y, label="log(sales)", lw=1.0)
    fc_index = np.arange(len(y), len(y) + 12)
    ax.plot(fc_index, fc_mean, "r-", label="forecast", lw=1.4)
    ax.fill_between(fc_index, fc_ci[:, 0], fc_ci[:, 1],
                    color="red", alpha=0.2, label="95% CI")
    ax.set_title("SARIMA(0,1,1)(0,1,1)_12 -- 12-month forecast")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("lab4_ex5_forecast.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figures lab4_ex5_logy.png, lab4_ex5_forecast.png")


if __name__ == "__main__":
    Y, Z = exercise1()
    dZ = exercise2(Y, Z)
    exercise3(Y, Z)
    exercise4(Z, dZ)
    exercise5()
