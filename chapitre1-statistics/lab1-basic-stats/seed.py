"""
Lab 1 — Basic Statistics (student skeleton)
============================================

Time Series Analysis — Chapter 1
Author : Aymen Ben Brik
Email  : aymen.benbrik@esprit.tn
Esprit School of Business

Fill in the blocks marked TODO. Reproducibility: seed = 42.
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)


# =====================================================================
# Exercise 1 — Empirical moments
# =====================================================================

def empirical_moments(x):
    """Return (mean, variance, skewness, kurtosis) of array x."""
    # TODO
    raise NotImplementedError


def exercise1():
    # TODO (Q1) : draw N(2, 4), n = 10000, compute and compare
    # TODO (Q2) : plot mu_hat vs n
    pass


# =====================================================================
# Exercise 2 — MoM vs MLE for the Gaussian
# =====================================================================

def mom_gaussian(x):
    """Method-of-Moments estimator: returns (mu_hat, sigma2_hat)."""
    # TODO
    raise NotImplementedError


def mle_gaussian(x):
    """MLE estimator: returns (mu_hat, sigma2_hat).
    For Gaussian data this coincides with MoM."""
    # TODO
    raise NotImplementedError


def exercise2():
    # TODO (Q1) : verify MoM == MLE on a sample
    # TODO (Q2) : Monte Carlo bias study (n=20, B=1000)
    pass


# =====================================================================
# Exercise 3 — Sampling distribution of X-bar
# =====================================================================

def exercise3():
    # TODO (Q1, Q2) : 4 histograms for n in {10, 30, 100, 1000}
    # TODO (Q3) : repeat with Exp(1)
    pass


# =====================================================================
# Exercise 4 — CI and t-test on Atlanta data
# =====================================================================

def t_ci(x, alpha=0.05):
    """Two-sided (1-alpha) t-CI for the mean of x."""
    # TODO
    raise NotImplementedError


def t_test_one_sample(x, mu0):
    """One-sample t-test. Returns (T, p_value)."""
    # TODO
    raise NotImplementedError


def load_atlanta_monthly(path="data/AvTempAtlanta.txt"):
    """Load the dataset (header line + Year+12 monthly+Annual) and
    return the monthly series Jan..Dec stacked across years."""
    arr = np.loadtxt(path, skiprows=1)
    return arr[:, 1:13].flatten()


def exercise4():
    data = load_atlanta_monthly()
    # TODO (Q1) : CI 95% for the mean
    # TODO (Q2) : test H0: mu = 60
    # TODO (Q3) : compare with scipy.stats.ttest_1samp
    pass


# =====================================================================
# Exercise 5 — Bonus : bootstrap CI
# =====================================================================

def bootstrap_ci(x, B=5000, alpha=0.05):
    """Non-parametric bootstrap CI for the mean."""
    # TODO
    raise NotImplementedError


def exercise5():
    data = load_atlanta_monthly()
    # TODO : bootstrap vs t CI
    pass


# =====================================================================
if __name__ == "__main__":
    exercise1()
    exercise2()
    exercise3()
    exercise4()
    exercise5()
