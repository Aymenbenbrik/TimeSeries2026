"""
Lab 2 — Decomposition (reference solution)
===========================================

Time Series Analysis — Chapter 2
Author : Aymen Ben Brik
Email  : aymen.benbrik@esprit.tn
Esprit School of Business
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

np.random.seed(42)


# =====================================================================
# Exercise 1 — Synthetic series
# =====================================================================

def generate_synthetic(T=240, seed=42):
    np.random.seed(seed)
    t = np.arange(1, T + 1)
    T_true = 20.0 + 0.05 * t
    S_true = 5.0 * np.sin(2 * np.pi * t / 12)
    eps = np.random.randn(T)
    Y = T_true + S_true + eps
    return t, Y, T_true, S_true, eps


def exercise1():
    print("=" * 60)
    print("Exercise 1 -- Synthetic decomposition")
    print("=" * 60)
    t, Y, T_, S_, eps_ = generate_synthetic()

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(t, Y, color="black"); axes[0].set_title("Observed $Y_t$")
    axes[1].plot(t, T_, color="tab:blue"); axes[1].set_title("True trend $T_t$")
    axes[2].plot(t, S_, color="tab:orange"); axes[2].set_title("True seasonality $S_t$")
    axes[3].plot(t, eps_, color="tab:green"); axes[3].set_title("Residual $\\varepsilon_t$")
    axes[3].set_xlabel("t (month)")
    plt.tight_layout()
    fig.savefig("lab2_ex1_synth.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Y: mean={Y.mean():.2f}, std={Y.std(ddof=1):.2f}")
    print("  -> figure lab2_ex1_synth.png")


# =====================================================================
# Exercise 2 — Trend estimation
# =====================================================================

def centred_ma(y, k):
    n = len(y)
    out = np.full(n, np.nan)
    for i in range(k, n - k):
        out[i] = y[i - k:i + k + 1].mean()
    return out


def rmse(a, b, mask=None):
    diff = (a - b) ** 2
    if mask is not None:
        diff = diff[mask]
    return float(np.sqrt(np.nanmean(diff)))


def exercise2():
    print("=" * 60)
    print("Exercise 2 -- Trend estimation: MA / OLS / LOESS")
    print("=" * 60)
    t, Y, T_, S_, eps = generate_synthetic()
    n = len(Y)

    # 1) Centred MA
    T_ma = centred_ma(Y, k=6)
    valid = ~np.isnan(T_ma)

    # 2) Linear regression
    lin = LinearRegression().fit(t.reshape(-1, 1), Y)
    T_lin = lin.predict(t.reshape(-1, 1))

    # 3) LOESS
    T_loess = lowess(Y, t, frac=0.2, return_sorted=False)

    # RMSE
    rmse_ma    = rmse(T_ma, T_, mask=valid)
    rmse_lin   = rmse(T_lin, T_)
    rmse_loess = rmse(T_loess, T_)
    print(f"  RMSE MA(k=6)         = {rmse_ma:.3f}")
    print(f"  RMSE linear regress. = {rmse_lin:.3f}")
    print(f"  RMSE LOESS frac=0.2  = {rmse_loess:.3f}")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, Y, color="lightgray", lw=0.7, label="$Y_t$")
    ax.plot(t, T_, "k--", label="true trend")
    ax.plot(t, T_ma, "tab:blue", label="centred MA")
    ax.plot(t, T_lin, "tab:orange", label="linear regr.")
    ax.plot(t, T_loess, "tab:green", label="LOESS")
    ax.set_xlabel("t"); ax.set_ylabel("level")
    ax.set_title("Trend estimation: three methods"); ax.legend()
    fig.savefig("lab2_ex2_trend.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab2_ex2_trend.png")


# =====================================================================
# Exercise 3 — Seasonality
# =====================================================================

def seasonal_average(detrended, d=12):
    n = len(detrended)
    s = np.zeros(d)
    for k in range(d):
        idx = np.arange(k, n, d)
        s[k] = np.nanmean(detrended[idx])
    return s - s.mean()


def exercise3():
    print("=" * 60)
    print("Exercise 3 -- Seasonality: averaging / dummies / Fourier")
    print("=" * 60)
    t, Y, T_, S_, eps = generate_synthetic()
    detrended = Y - lowess(Y, t, frac=0.2, return_sorted=False)

    # 1) Averaging
    S_avg = seasonal_average(detrended, d=12)

    # 2) Dummy regression (11 dummies + intercept)
    season_idx = ((t - 1) % 12)  # 0..11
    D = np.zeros((len(t), 11))
    for k in range(1, 12):
        D[:, k - 1] = (season_idx == k).astype(float)
    X = sm.add_constant(D)
    model_d = sm.OLS(detrended, X).fit()
    # Convert to 12 indices, recentered
    coefs = np.zeros(12)
    coefs[0] = model_d.params[0]
    coefs[1:] = model_d.params[0] + model_d.params[1:]
    S_dum = coefs - coefs.mean()

    # 3) Cosine-sine
    omega = 2 * np.pi / 12
    Xf = np.column_stack([np.cos(omega * t), np.sin(omega * t)])
    Xf = sm.add_constant(Xf)
    model_f = sm.OLS(detrended, Xf).fit()
    a, b = model_f.params[1], model_f.params[2]
    S_fou_full = a * np.cos(omega * t) + b * np.sin(omega * t)
    # Take 12 indices (one cycle)
    S_fou = np.array([S_fou_full[k] for k in range(12)])
    S_fou -= S_fou.mean()

    # Truth: 5 sin(2 pi k / 12), k = 1..12 (centered already)
    S_truth = 5 * np.sin(2 * np.pi * np.arange(1, 13) / 12)

    print(f"  RMSE averaging   = {rmse(S_avg, S_truth):.3f}")
    print(f"  RMSE dummies     = {rmse(S_dum, S_truth):.3f}")
    print(f"  RMSE Fourier (1) = {rmse(S_fou, S_truth):.3f}")

    fig, ax = plt.subplots(figsize=(8, 4))
    months = np.arange(1, 13)
    ax.plot(months, S_truth, "k--", label="truth", lw=2)
    ax.plot(months, S_avg, "o-", label="averaging")
    ax.plot(months, S_dum, "s-", label="dummies")
    ax.plot(months, S_fou, "^-", label="Fourier (1 harm.)")
    ax.set_xlabel("month"); ax.set_ylabel("seasonal index")
    ax.set_title("Seasonal patterns: 3 methods vs truth"); ax.legend()
    fig.savefig("lab2_ex3_season.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab2_ex3_season.png")


# =====================================================================
# Exercise 4 — Atlanta temperatures
# =====================================================================

def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    arr = np.loadtxt(path, skiprows=1)
    return arr[:, 1:13].flatten()


def exercise4():
    print("=" * 60)
    print("Exercise 4 -- Atlanta full decomposition")
    print("=" * 60)
    if not os.path.exists("data/AvTempAtlanta.txt"):
        print("  [data file not found — skipped]")
        return
    y = load_atlanta_monthly()
    n = len(y)
    t = np.arange(n)

    # 2x12 centred MA
    # Approximation: 13-window MA (good enough here)
    trend = centred_ma(y, k=6)

    # detrended
    detrended = y - trend
    # seasonal average
    s12 = seasonal_average(detrended, d=12)
    season = s12[t % 12]
    residual = y - trend - season

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(t, y, color="black", lw=0.5); axes[0].set_title("Atlanta monthly temp")
    axes[1].plot(t, trend, color="tab:blue"); axes[1].set_title("Trend (MA, k=6)")
    axes[2].plot(t, season, color="tab:orange", lw=0.5); axes[2].set_title("Seasonality")
    axes[3].plot(t, residual, color="tab:green", lw=0.5); axes[3].set_title("Residual")
    axes[3].set_xlabel("t (months from Jan 1879)")
    plt.tight_layout()
    fig.savefig("lab2_ex4_atlanta.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  Trend mean (over valid range)   = {np.nanmean(trend):.2f}")
    print(f"  Seasonal range                  = [{s12.min():.2f}, {s12.max():.2f}]")
    print(f"  Residual std                    = {np.nanstd(residual, ddof=1):.2f}")
    print("  Monthly seasonal indices (Jan -> Dec):")
    for k in range(12):
        print(f"    month {k+1:2d}: {s12[k]:+6.2f} F")
    print("  -> figure lab2_ex4_atlanta.png")


# =====================================================================
# Exercise 5 — Bonus : multiplicative
# =====================================================================

def exercise5():
    print("=" * 60)
    print("Exercise 5 -- Bonus: multiplicative model")
    print("=" * 60)
    np.random.seed(42)
    T = 240
    t = np.arange(1, T + 1)
    trend_true = 20 + 0.1 * t
    season_mult = 1 + 0.3 * np.sin(2 * np.pi * t / 12)
    eta = 0.05 * np.random.randn(T)
    Y = trend_true * season_mult * np.exp(eta)

    # Additive workflow on Y
    trend_a = lowess(Y, t, frac=0.2, return_sorted=False)
    detr_a = Y - trend_a
    s12_a = seasonal_average(detr_a, d=12)
    season_a = s12_a[(t - 1) % 12]
    res_a = Y - trend_a - season_a

    # Additive workflow on log(Y)
    logY = np.log(Y)
    trend_l = lowess(logY, t, frac=0.2, return_sorted=False)
    detr_l = logY - trend_l
    s12_l = seasonal_average(detr_l, d=12)
    season_l = s12_l[(t - 1) % 12]
    res_l = logY - trend_l - season_l

    print(f"  Std residual (additive on Y)     = {res_a.std(ddof=1):.4f}")
    print(f"  Std residual (additive on log Y) = {res_l.std(ddof=1):.4f}")
    print("  -> the log-additive workflow gives a much more homoscedastic residual.")


# =====================================================================
if __name__ == "__main__":
    exercise1(); exercise2(); exercise3(); exercise4(); exercise5()
