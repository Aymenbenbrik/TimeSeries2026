"""
Generates a reproducible synthetic 'daily returns' dataset
for Lab 6 -- saved to data/synthetic_returns.csv.

True data-generating process: GARCH(1,1) with Gaussian innovations.
"""
import sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

import numpy as np
import pandas as pd

np.random.seed(42)
T = 1500
alpha0, alpha1, beta1, mu = 0.05, 0.10, 0.85, 0.0
sigma2 = np.zeros(T)
eps    = np.zeros(T)
sigma2[0] = alpha0 / max(1e-9, 1 - alpha1 - beta1)  # unconditional var
eps[0]    = np.sqrt(sigma2[0]) * np.random.randn()
for t in range(1, T):
    sigma2[t] = alpha0 + alpha1 * eps[t-1]**2 + beta1 * sigma2[t-1]
    eps[t]    = np.sqrt(sigma2[t]) * np.random.randn()
r = mu + eps

dates = pd.bdate_range("2018-01-02", periods=T)
df = pd.DataFrame({"Date": dates, "Return": r})
df.to_csv("data/synthetic_returns.csv", index=False)
print(f"  T = {T}, sample mean = {r.mean():+.4f}, sample std = {r.std(ddof=1):.4f}")
print(f"  unconditional sd (true) = {np.sqrt(alpha0/(1-alpha1-beta1)):.4f}")
print(f"  saved to data/synthetic_returns.csv")
