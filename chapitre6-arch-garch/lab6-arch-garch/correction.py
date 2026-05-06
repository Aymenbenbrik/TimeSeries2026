"""
Lab 6 -- ARCH effects, GARCH and VaR (reference solution)
==========================================================

Time Series Analysis -- Chapter 6
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
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import het_arch
from arch import arch_model

warnings.filterwarnings("ignore")
np.random.seed(42)


def load_returns(path="data/synthetic_returns.csv"):
    df = pd.read_csv(path)
    return df["Return"].to_numpy(float)


# =====================================================================
# Exercise 1 -- Visualising volatility clustering
# =====================================================================

def exercise1(r):
    print("=" * 64)
    print("Exercise 1 -- Visualising volatility clustering")
    print("=" * 64)
    print(f"  T = {len(r)}, mean = {r.mean():+.4f}, std = {r.std(ddof=1):.4f}")
    print(f"  excess kurtosis = {stats.kurtosis(r):.3f}")

    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    axes[0].plot(r, lw=0.5); axes[0].set_title("Synthetic daily returns")
    axes[0].grid(alpha=0.3)
    plot_acf(r,    lags=20, ax=axes[1], title="ACF of r_t (~ flat)")
    plot_acf(r**2, lags=20, ax=axes[2], title="ACF of r_t^2 (volatility clustering)")
    plt.tight_layout()
    fig.savefig("lab6_ex1_clustering.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  -> figure lab6_ex1_clustering.png")


# =====================================================================
# Exercise 2 -- Engle's LM test
# =====================================================================

def exercise2(r):
    print("=" * 64)
    print("Exercise 2 -- Engle's LM test for ARCH effects")
    print("=" * 64)
    print(f"  {'lag':>5}{'LM stat':>12}{'crit 5%':>12}{'p-value':>12}  decision")
    for q in [5, 10, 20]:
        lm, lm_p, f_stat, f_p = het_arch(r, nlags=q)
        crit = stats.chi2.ppf(0.95, df=q)
        decision = "REJECT (ARCH)" if lm_p < 0.05 else "fail to reject"
        print(f"  {q:>5}{lm:>12.2f}{crit:>12.2f}{lm_p:>12.4e}  {decision}")


# =====================================================================
# Exercise 3 -- ARCH(q)
# =====================================================================

def exercise3(r):
    print("=" * 64)
    print("Exercise 3 -- ARCH(q) fitting (q in {1, 3, 5})")
    print("=" * 64)
    print(f"  {'q':>3}{'logL':>10}{'AIC':>10}{'sum_alphas':>14}  alphas")
    for q in [1, 3, 5]:
        am  = arch_model(r, mean="Constant", vol="ARCH", p=q, dist="normal", rescale=False)
        res = am.fit(disp="off")
        alphas = [res.params[f"alpha[{i}]"] for i in range(1, q + 1)]
        print(f"  {q:>3}{res.loglikelihood:>10.2f}{res.aic:>10.2f}"
              f"{sum(alphas):>14.4f}  {[round(a, 4) for a in alphas]}")


# =====================================================================
# Exercise 4 -- GARCH(1,1)
# =====================================================================

def exercise4(r):
    print("=" * 64)
    print("Exercise 4 -- GARCH(1,1)")
    print("=" * 64)
    am  = arch_model(r, mean="Constant", vol="GARCH", p=1, q=1, dist="normal", rescale=False)
    res = am.fit(disp="off")
    a0 = res.params["omega"]
    a1 = res.params["alpha[1]"]
    b1 = res.params["beta[1]"]
    mu = res.params["mu"]
    print(f"  mu       = {mu:+.4f}")
    print(f"  alpha_0  = {a0:.4f}")
    print(f"  alpha_1  = {a1:.4f}")
    print(f"  beta_1   = {b1:.4f}")
    print(f"  alpha_1 + beta_1 = {a1 + b1:.4f}  ({'< 1, stationary' if a1+b1<1 else '>= 1'})")
    sigma2_uncond = a0 / max(1e-9, 1 - a1 - b1)
    print(f"  implied unconditional variance = {sigma2_uncond:.4f}  "
          f"(sample var = {r.var(ddof=1):.4f})")
    print(f"  log-likelihood = {res.loglikelihood:.2f}, AIC = {res.aic:.2f}")
    return res


# =====================================================================
# Exercise 5 -- Standardised-residual diagnostics
# =====================================================================

def exercise5(res, r):
    print("=" * 64)
    print("Exercise 5 -- Standardised residuals")
    print("=" * 64)
    sigma_hat = res.conditional_volatility
    z = res.resid / sigma_hat

    fig, axes = plt.subplots(3, 1, figsize=(10, 9))
    plot_acf(z,    lags=20, ax=axes[0], title="ACF of standardised residuals z_t")
    plot_acf(z**2, lags=20, ax=axes[1], title="ACF of z_t^2")
    stats.probplot(z, dist="norm", plot=axes[2])
    axes[2].set_title("QQ-plot of z_t vs N(0,1)")
    plt.tight_layout()
    fig.savefig("lab6_ex5_zdiag.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  {'lag':>5}{'LM stat':>12}{'p-value':>12}  decision (on z_t^2)")
    for q in [5, 10, 20]:
        lm, lm_p, *_ = het_arch(z, nlags=q)
        decision = "REJECT (ARCH residual)" if lm_p < 0.05 else "OK -- white"
        print(f"  {q:>5}{lm:>12.2f}{lm_p:>12.4f}  {decision}")
    print("  -> figure lab6_ex5_zdiag.png")


# =====================================================================
# Exercise 6 -- Forecast and VaR
# =====================================================================

def exercise6(res, r):
    print("=" * 64)
    print("Exercise 6 -- Volatility forecast and VaR")
    print("=" * 64)
    a0 = res.params["omega"]
    a1 = res.params["alpha[1]"]
    b1 = res.params["beta[1]"]
    mu = res.params["mu"]
    sigma2_uncond = a0 / (1 - a1 - b1)

    H = 30
    fc = res.forecast(horizon=H, reindex=False)
    sigma2_fc = fc.variance.iloc[0].to_numpy()
    sigma2_T1 = sigma2_fc[0]

    # Closed-form check
    h = np.arange(1, H + 1)
    closed = sigma2_uncond + (a1 + b1) ** (h - 1) * (sigma2_T1 - sigma2_uncond)
    err = np.max(np.abs(sigma2_fc - closed))
    print(f"  max |arch_forecast - closed-form| = {err:.2e}  "
          f"({'OK' if err<1e-8 else 'mismatch'})")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(h, sigma2_fc, "ro-", label=r"$\widehat\sigma^2_{T+h}$")
    ax.axhline(sigma2_uncond, color="k", ls="--",
               label=fr"unconditional $\sigma^2 = {sigma2_uncond:.3f}$")
    ax.set_xlabel("horizon h")
    ax.set_ylabel(r"$\widehat\sigma^2_{T+h}$")
    ax.set_title("GARCH(1,1) variance forecast (mean reversion)")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("lab6_ex6_forecast.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    sigma_T1 = np.sqrt(sigma2_T1)
    sigma_un = np.sqrt(sigma2_uncond)
    print(f"  sigma_{{T+1}} (conditional) = {sigma_T1:.4f}")
    print(f"  sigma     (unconditional) = {sigma_un:.4f}")

    print(f"  {'alpha':>7}{'z_alpha':>10}{'VaR cond':>14}{'VaR uncond':>14}")
    for alpha in [0.01, 0.05]:
        z_a = stats.norm.ppf(alpha)
        var_cond   = -(mu + z_a * sigma_T1)
        var_uncond = -(mu + z_a * sigma_un)
        print(f"  {alpha:>7.2%}{z_a:>10.3f}{var_cond:>14.4f}{var_uncond:>14.4f}")
    print("  -> figure lab6_ex6_forecast.png")


if __name__ == "__main__":
    r = load_returns()
    exercise1(r)
    exercise2(r)
    exercise3(r)
    res = exercise4(r)
    exercise5(res, r)
    exercise6(res, r)
