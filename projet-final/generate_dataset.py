"""
Synthetic daily stock-price dataset for the integrative final project.

True data-generating process:
  log(P_t) = log(P_{t-1}) + mu + epsilon_t
  epsilon_t = sigma_t * z_t,  z_t ~ N(0,1)
  sigma_t^2 = alpha_0 + alpha_1 * eps_{t-1}^2 + beta_1 * sigma_{t-1}^2

Saved to data/stock_prices.csv.
"""
import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import pandas as pd

np.random.seed(42)

T   = 2000
mu  = 0.0004                    # ~10% per year, daily drift
P0  = 100.0
alpha0, alpha1, beta1 = 1e-5, 0.08, 0.90    # alpha+beta = 0.98 (high persistence)

sigma2 = np.zeros(T)
eps    = np.zeros(T)
sigma2[0] = alpha0 / max(1e-9, 1 - alpha1 - beta1)
eps[0]    = np.sqrt(sigma2[0]) * np.random.randn()
for t in range(1, T):
    sigma2[t] = alpha0 + alpha1 * eps[t-1] ** 2 + beta1 * sigma2[t-1]
    eps[t]    = np.sqrt(sigma2[t]) * np.random.randn()

logP = np.log(P0) + np.cumsum(mu + eps)
P    = np.exp(logP)

dates = pd.bdate_range("2018-01-02", periods=T)
df = pd.DataFrame({"Date": dates, "Price": P})
df.to_csv("data/stock_prices.csv", index=False)
print(f"  T = {T}, P[0]={P[0]:.2f}, P[-1]={P[-1]:.2f}, "
      f"min={P.min():.2f}, max={P.max():.2f}")
print(f"  daily log-return: mean={mu:.5f}, sd_uncond_true={np.sqrt(alpha0/(1-alpha1-beta1)):.5f}")
print(f"  saved to data/stock_prices.csv")
