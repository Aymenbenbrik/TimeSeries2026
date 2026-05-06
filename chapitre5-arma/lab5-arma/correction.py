"""
Lab 5 -- ARMA estimation and forecasting (reference solution)
=============================================================

Time Series Analysis -- Chapter 5
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
np.random.seed(42)


# =====================================================================
# Helpers
# =====================================================================

def fit_table(y, orders, lb_lag=24):
    """Fit each order and print a comparison table."""
    print(f"  {'order':<10}{'logL':>10}{'AIC':>10}{'BIC':>10}"
          f"{'sigma2':>10}{'LB({})  p'.format(lb_lag):>14}")
    fits = {}
    for order in orders:
        try:
            f = ARIMA(y, order=order).fit()
            lb = acorr_ljungbox(f.resid, lags=[lb_lag], return_df=True)
            p = lb["lb_pvalue"].iloc[0]
            sig2 = f.params[-1] if "sigma2" in f.param_names else np.var(f.resid, ddof=1)
            print(f"  {str(order):<10}{f.llf:>10.2f}{f.aic:>10.2f}"
                  f"{f.bic:>10.2f}{sig2:>10.4f}{p:>14.4f}")
            fits[order] = f
        except Exception as exc:
            print(f"  {str(order):<10} fit failed: {exc}")
    return fits


# =====================================================================
# Exercise 1 -- AR(2) simulation and estimation
# =====================================================================

def exercise1():
    print("=" * 64)
    print("Exercise 1 -- AR(2) simulation and estimation")
    print("=" * 64)
    T = 500
    rng = np.random.default_rng(42)
    eps = rng.standard_normal(T)
    X = np.zeros(T)
    for t in range(2, T):
        X[t] = 0.6 * X[t-1] - 0.3 * X[t-2] + eps[t]

    fig, axes = plt.subplots(3, 1, figsize=(9, 8))
    axes[0].plot(X, lw=0.7); axes[0].set_title(r"AR(2): $X_t = 0.6 X_{t-1} - 0.3 X_{t-2} + \varepsilon_t$")
    plot_acf(X, lags=20, ax=axes[1], title="Sample ACF")
    plot_pacf(X, lags=20, ax=axes[2], title="Sample PACF -- cut after lag 2")
    plt.tight_layout()
    fig.savefig("lab5_ex1_ar2.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fit_table(X, [(1, 0, 0), (2, 0, 0), (3, 0, 0)])
    f2 = ARIMA(X, order=(2, 0, 0)).fit()
    print(f"\n  AR(2) fit: phi1 = {f2.params[1]:+.4f}, phi2 = {f2.params[2]:+.4f}")
    print(f"  (true: phi1 = +0.6, phi2 = -0.3)")
    print("  -> figure lab5_ex1_ar2.png")


# =====================================================================
# Exercise 2 -- MA(1)
# =====================================================================

def exercise2():
    print("=" * 64)
    print("Exercise 2 -- MA(1) identification")
    print("=" * 64)
    T = 500
    rng = np.random.default_rng(42)
    eps = rng.standard_normal(T + 1)
    X = eps[1:] + 0.7 * eps[:-1]

    rho = acf(X, nlags=5, fft=False)
    print(f"  Empirical rho(1..5) = {np.round(rho[1:6], 3)}")
    print(f"  Theory rho(1) = 0.7 / 1.49 = {0.7 / (1 + 0.7**2):.4f}")

    fits = fit_table(X, [(0, 0, 1), (1, 0, 0)])
    print(f"\n  MA(1) fit: theta = {fits[(0, 0, 1)].params[1]:+.4f}  (true 0.7)")


# =====================================================================
# Exercise 3 -- ARMA(1,1)
# =====================================================================

def exercise3():
    print("=" * 64)
    print("Exercise 3 -- ARMA(1,1) on simulated data")
    print("=" * 64)
    T = 500
    rng = np.random.default_rng(42)
    eps = rng.standard_normal(T + 1)
    X = np.zeros(T)
    for t in range(1, T):
        X[t] = 0.5 * X[t-1] + eps[t+1] + 0.4 * eps[t]

    fits = fit_table(X, [(1, 0, 0), (0, 0, 1), (1, 0, 1), (2, 0, 2)])
    f11 = fits[(1, 0, 1)]
    print(f"\n  ARMA(1,1) fit: phi = {f11.params[1]:+.4f}, "
          f"theta = {f11.params[2]:+.4f}  (true 0.5, 0.4)")


# =====================================================================
# Exercise 4 -- Box-Jenkins on Atlanta residual
# =====================================================================

def load_atlanta():
    arr = np.loadtxt("data/AvTempAtlanta.txt", skiprows=1)
    return arr[:, 1:13].flatten()


def centred_ma(y, k):
    n = len(y); out = np.full(n, np.nan)
    for i in range(k, n - k):
        out[i] = y[i - k:i + k + 1].mean()
    return out


def seasonal_average(detrended, d=12):
    n = len(detrended); s = np.zeros(d)
    for k in range(d):
        idx = np.arange(k, n, d)
        s[k] = np.nanmean(detrended[idx])
    return s - s.mean()


def atlanta_residual():
    y = load_atlanta()
    trend = centred_ma(y, k=6)
    detrended = y - trend
    s12 = seasonal_average(detrended, d=12)
    n = len(y); t = np.arange(n)
    season = s12[t % 12]
    residual = y - trend - season
    valid = ~np.isnan(residual)
    return residual[valid]


def exercise4():
    print("=" * 64)
    print("Exercise 4 -- Box-Jenkins on Atlanta residual")
    print("=" * 64)
    if not os.path.exists("data/AvTempAtlanta.txt"):
        print("  [data file not found -- skipped]")
        return None
    res = atlanta_residual()
    print(f"  Residual: n = {len(res)}, std = {res.std(ddof=1):.3f}")

    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    plot_acf(res, lags=36, ax=axes[0], title="Atlanta residual -- ACF")
    plot_pacf(res, lags=36, ax=axes[1], title="Atlanta residual -- PACF")
    plt.tight_layout()
    fig.savefig("lab5_ex4_atlanta_acfpacf.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fits = fit_table(res, [(1, 0, 0), (2, 0, 0), (0, 0, 1),
                           (1, 0, 1), (2, 0, 1)])
    print("  -> figure lab5_ex4_atlanta_acfpacf.png")
    return res, fits


# =====================================================================
# Exercise 5 -- Forecasting
# =====================================================================

def exercise5(res, fits):
    print("=" * 64)
    print("Exercise 5 -- 24-step forecast on chosen model")
    print("=" * 64)
    if res is None: return
    # pick best by BIC
    best = min(fits.items(), key=lambda kv: kv[1].bic)
    order, fit = best
    print(f"  Selected model: ARIMA{order}, BIC = {fit.bic:.2f}")

    fc = fit.get_forecast(steps=24)
    mean = fc.predicted_mean
    ci = fc.conf_int(alpha=0.05)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(res, label="residual", lw=0.8)
    fc_idx = np.arange(len(res), len(res) + 24)
    ax.plot(fc_idx, mean, "r-", label="forecast", lw=1.2)
    ax.fill_between(fc_idx, ci[:, 0], ci[:, 1], color="red", alpha=0.2,
                    label="95% CI")
    ax.set_title(f"24-step forecast -- ARIMA{order}")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("lab5_ex5_forecast.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # bonus : hold-out
    n = len(res); cut = int(0.8 * n)
    train, test = res[:cut], res[cut:]
    f_train = ARIMA(train, order=order).fit()
    fc_test = f_train.get_forecast(steps=len(test)).predicted_mean
    rmse = np.sqrt(np.mean((test - fc_test) ** 2))
    print(f"  Hold-out: train n={cut}, test n={len(test)}, "
          f"RMSE = {rmse:.3f}, residual std (train) = {f_train.resid.std(ddof=1):.3f}")
    print("  -> figure lab5_ex5_forecast.png")


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    out = exercise4()
    if out is not None:
        res, fits = out
        exercise5(res, fits)
