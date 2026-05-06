"""
Lab 1 — Basic Statistics (reference solution)
==============================================

Time Series Analysis — Chapter 1
Author : Aymen Ben Brik
Email  : aymen.benbrik@esprit.tn
Esprit School of Business
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)


# =====================================================================
# Exercise 1 — Empirical moments
# =====================================================================

def empirical_moments(x):
    mu = x.mean()
    sigma2 = x.var(ddof=0)  # MLE / MoM (1/n)
    sigma = np.sqrt(sigma2)
    skew = ((x - mu) ** 3).mean() / sigma ** 3
    kurt = ((x - mu) ** 4).mean() / sigma ** 4
    return mu, sigma2, skew, kurt


def exercise1():
    print("=" * 60)
    print("Exercise 1 -- Empirical moments")
    print("=" * 60)

    # Q1
    np.random.seed(42)
    x = 2 + 2 * np.random.randn(10_000)  # N(2, 4)
    mu, sigma2, skew, kurt = empirical_moments(x)
    print(f"  N(2, 4), n = 10000 :")
    print(f"    mu_hat     = {mu:.4f}   (theoretical: 2)")
    print(f"    sigma2_hat = {sigma2:.4f}   (theoretical: 4)")
    print(f"    skew_hat   = {skew:.4f}   (theoretical: 0)")
    print(f"    kurt_hat   = {kurt:.4f}   (theoretical: 3)")

    # Q2
    ns = [10, 50, 100, 500, 1000, 5000, 10_000]
    means = []
    for n in ns:
        np.random.seed(42)
        means.append((2 + 2 * np.random.randn(n)).mean())
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogx(ns, means, "-o", label="$\\widehat\\mu_n$")
    ax.axhline(2, color="black", linestyle="--", label="$\\mu = 2$")
    ax.set_xlabel("n"); ax.set_ylabel("$\\widehat\\mu_n$")
    ax.set_title("Convergence of the sample mean (LLN)")
    ax.legend(); ax.grid(True, which="both", linestyle=":")
    fig.savefig("lab1_ex1_lln.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab1_ex1_lln.png")


# =====================================================================
# Exercise 2 — MoM vs MLE
# =====================================================================

def mom_gaussian(x):
    mu = x.mean()
    sigma2 = ((x - mu) ** 2).mean()  # 1/n divisor
    return mu, sigma2


def mle_gaussian(x):
    return mom_gaussian(x)  # identical for Gaussian


def exercise2():
    print("=" * 60)
    print("Exercise 2 -- MoM vs MLE for the Gaussian")
    print("=" * 60)

    np.random.seed(42)
    x = np.random.randn(50)
    print(f"  MoM(x) = {mom_gaussian(x)}")
    print(f"  MLE(x) = {mle_gaussian(x)}")
    print("  -> identical (as expected for Gaussian).")

    # Bias study
    sigma2 = 4.0
    n, B = 20, 1000
    mle_vars = np.empty(B); s2_vars = np.empty(B)
    for b in range(B):
        sample = 2 + np.sqrt(sigma2) * np.random.randn(n)
        _, mle_vars[b] = mle_gaussian(sample)
        s2_vars[b] = sample.var(ddof=1)  # unbiased S^2
    print(f"  E[sigma2_MLE] empirical = {mle_vars.mean():.3f}  (theory: {(n-1)/n*sigma2:.3f})")
    print(f"  E[S^2]        empirical = {s2_vars.mean():.3f}   (theory: {sigma2:.3f})")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(mle_vars, bins=30, alpha=0.6, label=r"$\widehat\sigma^2_{\rm MLE}$", color="tab:red")
    ax.hist(s2_vars, bins=30, alpha=0.6, label=r"$S^2_n$ (unbiased)", color="tab:blue")
    ax.axvline(sigma2, color="black", linestyle="--", label="$\\sigma^2 = 4$")
    ax.set_xlabel("variance estimate"); ax.set_ylabel("frequency")
    ax.set_title(f"Bias of the variance estimator (n={n}, B={B})")
    ax.legend()
    fig.savefig("lab1_ex2_bias.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab1_ex2_bias.png")


# =====================================================================
# Exercise 3 — Sampling distribution of X-bar
# =====================================================================

def exercise3():
    print("=" * 60)
    print("Exercise 3 -- Sampling distribution of X-bar")
    print("=" * 60)

    mu, sigma2 = 2.0, 4.0
    sigma = np.sqrt(sigma2)
    B = 1000
    sizes = [10, 30, 100, 1000]

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, n in zip(axes.flat, sizes):
        np.random.seed(42)
        means = np.array([(mu + sigma * np.random.randn(n)).mean() for _ in range(B)])
        ax.hist(means, bins=30, density=True, alpha=0.7, color="tab:blue")
        xs = np.linspace(means.min(), means.max(), 200)
        ax.plot(xs, stats.norm.pdf(xs, mu, sigma / np.sqrt(n)), "r-",
                label=f"$N({mu},{sigma2/n:.3f})$")
        ax.set_title(f"n = {n}, var = {means.var():.4f} (theory {sigma2/n:.4f})")
        ax.legend(fontsize=8)
    plt.tight_layout()
    fig.savefig("lab1_ex3_sampling.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Q3 : Exp(1)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, n in zip(axes.flat, sizes):
        np.random.seed(42)
        means = np.array([np.random.exponential(1.0, n).mean() for _ in range(B)])
        ax.hist(means, bins=30, density=True, alpha=0.7, color="tab:green")
        xs = np.linspace(means.min(), means.max(), 200)
        ax.plot(xs, stats.norm.pdf(xs, 1.0, 1.0 / np.sqrt(n)), "r-")
        ax.set_title(f"Exp(1), n = {n}, var = {means.var():.4f} (theory {1/n:.4f})")
    plt.tight_layout()
    fig.savefig("lab1_ex3_clt_exp.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figures lab1_ex3_*.png")


# =====================================================================
# Exercise 4 — CI and t-test on Atlanta temperatures
# =====================================================================

def t_ci(x, alpha=0.05):
    n = len(x)
    mean = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    h = stats.t.ppf(1 - alpha / 2, df=n - 1) * se
    return mean - h, mean + h


def t_test_one_sample(x, mu0):
    n = len(x)
    mean = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    T = (mean - mu0) / se
    p = 2 * (1 - stats.t.cdf(abs(T), df=n - 1))
    return T, p


def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    """Load Atlanta temperatures and return monthly series (Jan..Dec stacked)."""
    arr = np.loadtxt(path, skiprows=1)  # cols: Year, Jan..Dec, Annual
    monthly = arr[:, 1:13].flatten()  # 12 monthly values per year
    return monthly


def exercise4():
    print("=" * 60)
    print("Exercise 4 -- CI and t-test on Atlanta temperatures")
    print("=" * 60)
    path = "data/AvTempAtlanta.txt"
    if not os.path.exists(path):
        print(f"  [data file {path} not found — skipped]")
        return
    data = load_atlanta_monthly(path)
    print(f"  n = {len(data)},  mean = {data.mean():.2f},  std = {data.std(ddof=1):.2f}")

    lo, hi = t_ci(data, alpha=0.05)
    print(f"  95% CI for mu : [{lo:.2f}, {hi:.2f}]")

    T, p = t_test_one_sample(data, mu0=60)
    print(f"  H0: mu = 60   ->   T = {T:.3f},  p-value = {p:.4f}")

    T_sci, p_sci = stats.ttest_1samp(data, 60)
    print(f"  scipy ttest_1samp -> T = {T_sci:.3f},  p-value = {p_sci:.4f}")


# =====================================================================
# Exercise 5 — Bonus : bootstrap CI
# =====================================================================

def bootstrap_ci(x, B=5000, alpha=0.05):
    n = len(x)
    rng = np.random.default_rng(42)
    boots = np.empty(B)
    for b in range(B):
        sample = rng.choice(x, size=n, replace=True)
        boots[b] = sample.mean()
    lo = np.quantile(boots, alpha / 2)
    hi = np.quantile(boots, 1 - alpha / 2)
    return lo, hi


def exercise5():
    print("=" * 60)
    print("Exercise 5 -- Bonus : bootstrap CI")
    print("=" * 60)
    path = "data/AvTempAtlanta.txt"
    if not os.path.exists(path):
        print(f"  [data file {path} not found — skipped]")
        return
    data = load_atlanta_monthly(path)
    lo_t, hi_t = t_ci(data)
    lo_b, hi_b = bootstrap_ci(data, B=5000)
    print(f"  t-CI       : [{lo_t:.2f}, {hi_t:.2f}]")
    print(f"  bootstrap  : [{lo_b:.2f}, {hi_b:.2f}]")


# =====================================================================
if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
