"""
Lab 3 — ACF / PACF / Ljung-Box (reference solution)
====================================================

Time Series Analysis — Chapter 3
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)
"""

import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import os
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

np.random.seed(42)


# =====================================================================
# Exercise 1 — White noise
# =====================================================================

def exercise1():
    print("=" * 60)
    print("Exercise 1 -- White noise")
    print("=" * 60)
    T = 500
    np.random.seed(42)
    eps = np.random.randn(T)
    band = 1.96 / np.sqrt(T)
    rho = acf(eps, nlags=30, fft=False)[1:]  # skip rho(0) = 1
    n_out = int(np.sum(np.abs(rho) > band))
    print(f"  T = {T}, Bartlett band = +/- {band:.4f}")
    print(f"  Lags 1..30, |rho| > band : {n_out} (expected ~ {0.05*30:.1f} under H0)")

    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    axes[0].plot(eps, lw=0.5); axes[0].set_title("White noise N(0,1), T=500")
    plot_acf(eps, lags=30, ax=axes[1], title="Sample ACF")
    plt.tight_layout()
    fig.savefig("lab3_ex1_wn.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab3_ex1_wn.png")


# =====================================================================
# Exercise 2 — AR(1)
# =====================================================================

def simulate_ar1(phi, T=500, sigma=1.0, seed=42):
    rng = np.random.default_rng(seed)
    eps = sigma * rng.standard_normal(T)
    X = np.zeros(T)
    for t in range(1, T):
        X[t] = phi * X[t - 1] + eps[t]
    return X


def exercise2():
    print("=" * 60)
    print("Exercise 2 -- AR(1) ACF")
    print("=" * 60)
    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    for ax, phi in zip(axes.flat, [0.3, 0.7, -0.7, 0.95]):
        X = simulate_ar1(phi, T=500)
        rho_emp = acf(X, nlags=20, fft=False)
        rho_th = phi ** np.arange(21)
        ax.bar(np.arange(21), rho_emp, alpha=0.6, label="empirical")
        ax.plot(np.arange(21), rho_th, "ro-", markersize=4, label=fr"theory $\phi^h$")
        ax.set_title(fr"AR(1), $\phi = {phi}$"); ax.legend(fontsize=8)
        ax.axhline(0, color="black", lw=0.5)
    plt.tight_layout()
    fig.savefig("lab3_ex2_ar1.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # PACF for phi=0.7
    X = simulate_ar1(0.7, T=500)
    pa = pacf(X, nlags=10)
    print(f"  AR(1), phi=0.7 : PACF[1] = {pa[1]:.3f}, PACF[2..5] = {np.round(pa[2:6], 3)}")
    print("  -> figure lab3_ex2_ar1.png")


# =====================================================================
# Exercise 3 — MA(1)
# =====================================================================

def simulate_ma1(theta, T=500, sigma=1.0, seed=42):
    rng = np.random.default_rng(seed)
    eps = sigma * rng.standard_normal(T + 1)
    return eps[1:] + theta * eps[:-1]


def exercise3():
    print("=" * 60)
    print("Exercise 3 -- MA(1) ACF")
    print("=" * 60)
    for theta in [0.5, -0.5, 0.9]:
        X = simulate_ma1(theta, T=500)
        rho_emp = acf(X, nlags=5, fft=False)
        rho_th = theta / (1 + theta ** 2)
        print(f"  theta = {theta:>5} : rho(1) empirical = {rho_emp[1]:+.3f}, "
              f"theory = {rho_th:+.3f}, rho(2..5) = {np.round(rho_emp[2:5], 3)}")


# =====================================================================
# Exercise 4 — Atlanta ACF/PACF
# =====================================================================

def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    arr = np.loadtxt(path, skiprows=1)
    return arr[:, 1:13].flatten()


def centred_ma(y, k):
    n = len(y)
    out = np.full(n, np.nan)
    for i in range(k, n - k):
        out[i] = y[i - k:i + k + 1].mean()
    return out


def seasonal_average(detrended, d=12):
    n = len(detrended)
    s = np.zeros(d)
    for k in range(d):
        idx = np.arange(k, n, d)
        s[k] = np.nanmean(detrended[idx])
    return s - s.mean()


def exercise4():
    print("=" * 60)
    print("Exercise 4 -- ACF/PACF on Atlanta")
    print("=" * 60)
    if not os.path.exists("data/AvTempAtlanta.txt"):
        print("  [data file not found — skipped]")
        return None

    y = load_atlanta_monthly()
    fig, ax = plt.subplots(figsize=(8, 4))
    plot_acf(y, lags=60, ax=ax, title="Atlanta raw — ACF")
    fig.savefig("lab3_ex4_atlanta_raw.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # decomposition
    trend = centred_ma(y, k=6)
    detrended = y - trend
    s12 = seasonal_average(detrended, d=12)
    n = len(y); t = np.arange(n)
    season = s12[t % 12]
    residual = y - trend - season
    valid = ~np.isnan(residual)
    res = residual[valid]

    fig, axes = plt.subplots(2, 1, figsize=(8, 7))
    plot_acf(res, lags=60, ax=axes[0], title="Atlanta residual — ACF")
    plot_pacf(res, lags=60, ax=axes[1], title="Atlanta residual — PACF")
    plt.tight_layout()
    fig.savefig("lab3_ex4_atlanta_residual.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Residual : n = {len(res)}, mean = {res.mean():.3f}, std = {res.std(ddof=1):.3f}")
    print("  -> figures lab3_ex4_*.png")
    return res


# =====================================================================
# Exercise 5 — Ljung-Box
# =====================================================================

def exercise5(residual=None):
    print("=" * 60)
    print("Exercise 5 -- Ljung-Box test")
    print("=" * 60)
    if residual is None:
        residual = exercise4()
        if residual is None: return

    out = acorr_ljungbox(residual, lags=[12, 24, 36], return_df=True)
    print("  Atlanta residual Ljung-Box :")
    print(out.to_string())

    # Bonus : white noise
    np.random.seed(42)
    wn = np.random.randn(500)
    out_wn = acorr_ljungbox(wn, lags=[12, 24, 36], return_df=True)
    print("\n  Simulated white noise Ljung-Box :")
    print(out_wn.to_string())


if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    res = exercise4()
    exercise5(res)
