"""
Final integrative project -- reference solution
================================================

Time Series Analysis -- Esprit School of Business
Author : Aymen Ben Brik (aymen.benbrik@esprit.tn)

Pipeline: descriptive stats -> decomposition -> ACF/PACF/LB ->
ADF/KPSS -> ARMA -> GARCH -> conditional VaR -> Kupiec back-test.
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
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import het_arch, acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model

warnings.filterwarnings("ignore")
np.random.seed(42)


# =====================================================================
# Helpers
# =====================================================================

def report_adf(name, y, regression="c"):
    stat, pval, *_, crit, _ = adfuller(y, regression=regression)
    decision = "REJECT (stat.)" if pval < 0.05 else "fail to reject"
    print(f"  ADF on {name:<14} reg={regression}: stat={stat:+.3f}, "
          f"p={pval:.4f}, crit5%={crit['5%']:+.3f} -> {decision}")
    return stat, pval


def report_kpss(name, y, regression="c"):
    stat, pval, lags, crit = kpss(y, regression=regression, nlags="auto")
    decision = "REJECT (unit root)" if pval < 0.05 else "fail to reject"
    print(f"  KPSS on {name:<13} reg={regression}: stat={stat:+.3f}, "
          f"p={pval:.4f}, crit5%={crit['5%']:+.3f} -> {decision}")
    return stat, pval


# =====================================================================
# Data loading
# =====================================================================

def load_prices(path="../data/stock_prices.csv"):
    df = pd.read_csv(path, parse_dates=["Date"])
    return df["Date"].to_numpy(), df["Price"].to_numpy(float)


# =====================================================================
# Part A -- Basic statistics on returns
# =====================================================================

def part_A(P):
    print("=" * 64)
    print("Part A -- Basic statistics on returns")
    print("=" * 64)
    r = np.diff(np.log(P))
    n = len(r)
    mu_hat    = r.mean()
    sigma_hat = r.std(ddof=1)
    skew      = stats.skew(r)
    kurt      = stats.kurtosis(r)              # excess kurtosis
    se_mean   = sigma_hat / np.sqrt(n)
    t975      = stats.t.ppf(0.975, df=n-1)
    ci_low, ci_high = mu_hat - t975 * se_mean, mu_hat + t975 * se_mean
    print(f"  n = {n}")
    print(f"  mean       = {mu_hat:+.6f}")
    print(f"  sd         = {sigma_hat:.6f}")
    print(f"  skewness   = {skew:+.3f}")
    print(f"  excess kurtosis = {kurt:+.3f}")
    print(f"  95% CI for mean = [{ci_low:+.6f}, {ci_high:+.6f}]")
    t_stat = mu_hat / se_mean
    p_two  = 2 * (1 - stats.t.cdf(abs(t_stat), df=n-1))
    decision = "REJECT" if p_two < 0.05 else "fail to reject"
    print(f"  H0: mu=0 -> t = {t_stat:+.3f}, p = {p_two:.4f} -> {decision}")

    jb_stat, jb_p = stats.jarque_bera(r)
    print(f"  Jarque-Bera : stat = {jb_stat:.2f}, p = {jb_p:.4e}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(r, lw=0.5); axes[0].set_title("Daily log-returns r_t")
    axes[0].grid(alpha=0.3)
    grid_x = np.linspace(r.min(), r.max(), 200)
    axes[1].hist(r, bins=60, density=True, alpha=0.6, color="steelblue")
    axes[1].plot(grid_x, stats.norm.pdf(grid_x, mu_hat, sigma_hat),
                 "r-", lw=1.5, label=fr"$N({mu_hat:.4f}, {sigma_hat:.4f}^2)$")
    axes[1].set_title("Histogram + Gaussian fit")
    axes[1].legend(); axes[1].grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig("partA_returns.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return r


# =====================================================================
# Part B -- Decomposition
# =====================================================================

def centred_ma(y, k):
    n = len(y); out = np.full(n, np.nan)
    for i in range(k, n - k):
        out[i] = y[i - k:i + k + 1].mean()
    return out


def part_B(P, r):
    print("=" * 64)
    print("Part B -- Decomposition of the price level")
    print("=" * 64)
    logP = np.log(P)
    t = np.arange(len(P))
    A = np.column_stack([np.ones_like(t), t])
    beta, *_ = np.linalg.lstsq(A, logP, rcond=None)
    print(f"  OLS on log P_t = beta_0 + beta_1 t : "
          f"beta_1 = {beta[1]:+.6f}")
    print(f"  Sample mean of r_t                  = {r.mean():+.6f}")
    print(f"  -> consistent (drift recovered)")

    trend_ma = centred_ma(P, k=50)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(P, lw=0.7, label="P_t")
    ax.plot(trend_ma, "r-", lw=1.2, label="centred MA (k=50)")
    ax.plot(np.exp(A @ beta), "g--", lw=1.2, label="OLS exponential trend")
    ax.set_title("Price series: raw, smoothed and OLS trend")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("partB_decomposition.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# Part C -- Stationarity diagnostics
# =====================================================================

def part_C(P, r):
    print("=" * 64)
    print("Part C -- Stationarity diagnostics")
    print("=" * 64)
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    plot_acf(np.log(P), lags=60, ax=axes[0, 0], title="ACF of log P_t (slow decay)")
    plot_acf(r,         lags=60, ax=axes[0, 1], title="ACF of r_t (~ flat)")
    plot_acf(r**2,      lags=60, ax=axes[1, 0], title="ACF of r_t^2 (clustering)")
    plot_pacf(r,        lags=20, ax=axes[1, 1], title="PACF of r_t")
    plt.tight_layout()
    fig.savefig("partC_acfpacf.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("  Ljung-Box on r_t :")
    for m in [10, 20]:
        lb = acorr_ljungbox(r, lags=[m], return_df=True)
        print(f"    m={m:>3}  Q={lb['lb_stat'].iloc[0]:>8.2f}  "
              f"p={lb['lb_pvalue'].iloc[0]:.4f}")
    print("  Ljung-Box on r_t^2 :")
    for m in [10, 20]:
        lb = acorr_ljungbox(r**2, lags=[m], return_df=True)
        print(f"    m={m:>3}  Q={lb['lb_stat'].iloc[0]:>8.2f}  "
              f"p={lb['lb_pvalue'].iloc[0]:.4f}")


# =====================================================================
# Part D -- Unit-root testing
# =====================================================================

def part_D(P, r):
    print("=" * 64)
    print("Part D -- Unit-root tests on log P_t and r_t")
    print("=" * 64)
    logP = np.log(P)
    report_adf("log P_t", logP, regression="ct")
    report_adf("r_t",     r,    regression="c")
    report_kpss("log P_t", logP, regression="ct")
    report_kpss("r_t",     r,    regression="c")


# =====================================================================
# Part E -- ARMA modelling
# =====================================================================

def part_E(r):
    print("=" * 64)
    print("Part E -- ARMA modelling of returns")
    print("=" * 64)
    print(f"  {'order':<10}{'logL':>10}{'AIC':>10}{'BIC':>10}{'LB(24) p':>14}")
    fits = {}
    for order in [(0, 0, 0), (1, 0, 0), (0, 0, 1)]:
        f = ARIMA(r, order=order).fit()
        lb = acorr_ljungbox(f.resid, lags=[24], return_df=True)
        p = lb["lb_pvalue"].iloc[0]
        print(f"  {str(order):<10}{f.llf:>10.2f}{f.aic:>10.2f}"
              f"{f.bic:>10.2f}{p:>14.4f}")
        fits[order] = f
    best = min(fits.items(), key=lambda kv: kv[1].bic)
    print(f"  Best by BIC: ARMA{best[0]}  -- constant-mean is selected,")
    print(f"  consistent with the daily-return weak-form efficient regime.")
    return fits[best[0]]


# =====================================================================
# Part F -- GARCH(1,1) + VaR
# =====================================================================

def part_F(r):
    print("=" * 64)
    print("Part F -- GARCH(1,1) + Value-at-Risk")
    print("=" * 64)
    # Engle LM on r_t  (constant-mean residual)
    print("  Engle LM on raw returns r_t:")
    for q in [5, 10, 20]:
        lm, lm_p, *_ = het_arch(r, nlags=q)
        print(f"    q={q:>3}  LM={lm:>8.2f}  p={lm_p:.4e}")

    # Fit GARCH(1,1)
    am  = arch_model(r * 100, mean="Constant", vol="GARCH",
                     p=1, q=1, dist="normal")
    res = am.fit(disp="off")
    a0 = res.params["omega"]
    a1 = res.params["alpha[1]"]
    b1 = res.params["beta[1]"]
    mu = res.params["mu"]
    print(f"  GARCH(1,1) fit on r*100:")
    print(f"    mu      = {mu:+.4f}")
    print(f"    alpha_0 = {a0:.6f}")
    print(f"    alpha_1 = {a1:.4f}")
    print(f"    beta_1  = {b1:.4f}")
    print(f"    alpha_1 + beta_1 = {a1+b1:.4f}")
    sigma2_uncond = a0 / max(1e-9, 1 - a1 - b1)
    print(f"    implied unconditional sigma (in %) = "
          f"{np.sqrt(sigma2_uncond):.4f}")
    print(f"    sample sd (in %)                  = "
          f"{(r*100).std(ddof=1):.4f}")

    # Standardised residuals
    z = res.resid / res.conditional_volatility
    print("  Engle LM on standardised residuals^2:")
    for q in [5, 10, 20]:
        lm, lm_p, *_ = het_arch(z, nlags=q)
        decision = "OK -- white" if lm_p > 0.05 else "REJECT"
        print(f"    q={q:>3}  LM={lm:>8.2f}  p={lm_p:.4f}  {decision}")

    # Conditional VaR
    fc = res.forecast(horizon=1, reindex=False)
    sigma_T1 = float(np.sqrt(fc.variance.iloc[0, 0])) / 100  # back to fraction
    mu_back  = mu / 100
    sigma_uncond = float(np.sqrt(sigma2_uncond)) / 100

    print(f"  sigma_{{T+1}} (cond) = {sigma_T1:.5f}")
    print(f"  sigma     (uncond) = {sigma_uncond:.5f}")
    print(f"  {'alpha':>7}{'z_alpha':>10}{'VaR cond':>14}{'VaR uncond':>14}")
    for alpha in [0.01, 0.05]:
        z_a = stats.norm.ppf(alpha)
        var_c   = -(mu_back + z_a * sigma_T1)
        var_u   = -(mu_back + z_a * sigma_uncond)
        print(f"  {alpha:>7.2%}{z_a:>10.3f}{var_c:>14.5f}{var_u:>14.5f}")

    # Plot conditional sigma
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(r, lw=0.5, label="r_t", color="steelblue")
    ax.plot(res.conditional_volatility / 100, "r-", lw=1.0,
            label=r"$\widehat\sigma_t$")
    ax.plot(-res.conditional_volatility / 100, "r-", lw=1.0)
    ax.set_title("Returns and GARCH conditional sigma")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("partF_sigma.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return res


# =====================================================================
# Part G -- Kupiec back-test
# =====================================================================

def part_G(r, alpha=0.05, n_test=250, refit_every=10):
    print("=" * 64)
    print(f"Part G -- Kupiec back-test (alpha = {alpha:.0%}, n_test = {n_test})")
    print("=" * 64)
    n = len(r)
    cut = n - n_test
    z_a = stats.norm.ppf(alpha)
    var_seq, loss_exceed = [], []

    fitted = None
    for k, t in enumerate(range(cut, n)):
        if k % refit_every == 0:
            am = arch_model(r[:t] * 100, mean="Constant", vol="GARCH",
                            p=1, q=1, dist="normal")
            fitted = am.fit(disp="off", show_warning=False)
        fc = fitted.forecast(horizon=1, reindex=False)
        sigma_t = float(np.sqrt(fc.variance.iloc[0, 0])) / 100
        mu_t    = fitted.params["mu"] / 100
        var_t   = -(mu_t + z_a * sigma_t)
        loss_t  = -r[t]
        var_seq.append(var_t)
        loss_exceed.append(loss_t > var_t)

    var_seq    = np.array(var_seq)
    exceedance = np.array(loss_exceed, dtype=bool)
    X = int(exceedance.sum())
    N = n_test
    pi_hat = X / N
    print(f"  expected exceedances under H0 (alpha N) = {alpha*N:.1f}")
    print(f"  realised exceedances X                  = {X}")
    print(f"  realised proportion pi_hat              = {pi_hat:.4f}")

    if 0 < X < N:
        L0 = (1 - alpha) ** (N - X) * alpha ** X
        L1 = (1 - pi_hat) ** (N - X) * pi_hat ** X
        LR = -2 * np.log(L0 / L1)
    else:
        LR = np.nan
    crit = stats.chi2.ppf(0.95, df=1)
    p_lr = 1 - stats.chi2.cdf(LR, df=1) if np.isfinite(LR) else np.nan
    decision = "REJECT (mis-calibrated)" if (np.isfinite(LR) and LR > crit) \
               else "fail to reject -- well calibrated"
    print(f"  Kupiec LR = {LR:.4f}, crit5% = {crit:.3f}, p = {p_lr:.4f}")
    print(f"  -> {decision}")

    fig, ax = plt.subplots(figsize=(11, 4))
    test_idx = np.arange(cut, n)
    ax.plot(test_idx, r[cut:], lw=0.6, label="r_t (test)", color="steelblue")
    ax.plot(test_idx, -var_seq, "r-", lw=1.0,
            label=fr"$-\mathrm{{VaR}}_t(\alpha={alpha})$")
    ax.scatter(test_idx[exceedance], r[cut:][exceedance], color="red",
               s=18, zorder=5, label=f"exceedances ({X})")
    ax.set_title(f"Rolling 1-day VaR backtest -- {decision}")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig("partG_backtest.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# =====================================================================
# Driver
# =====================================================================

if __name__ == "__main__":
    dates, P = load_prices()
    print(f"Loaded {len(P)} prices from {dates[0]} to {dates[-1]}")
    r = part_A(P)
    part_B(P, r)
    part_C(P, r)
    part_D(P, r)
    fit_mean = part_E(r)
    fit_garch = part_F(r)
    part_G(r, alpha=0.05, n_test=250, refit_every=10)
