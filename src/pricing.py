"""Testable mathematical primitives for the option-pricing notebook."""

from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np


def black_scholes_price(spot: float, strike: float, maturity: float, rate: float,
                        volatility: float, option_type: str = "call") -> float:
    """Return a European call or put price under Black–Scholes."""
    if min(spot, strike, maturity, volatility) <= 0:
        raise ValueError("spot, strike, maturity, and volatility must be positive")
    kind = option_type.lower()
    if kind not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")
    root_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * volatility**2) * maturity) / (volatility * root_t)
    d2 = d1 - volatility * root_t
    normal = NormalDist()
    if kind == "call":
        return spot * normal.cdf(d1) - strike * math.exp(-rate * maturity) * normal.cdf(d2)
    return strike * math.exp(-rate * maturity) * normal.cdf(-d2) - spot * normal.cdf(-d1)


def expected_regime_occupancy(initial, transition, n_steps: int) -> np.ndarray:
    """Average expected regime probabilities over ``n_steps`` transitions."""
    initial = np.asarray(initial, dtype=float)
    transition = np.asarray(transition, dtype=float)
    if n_steps < 1 or transition.shape != (initial.size, initial.size):
        raise ValueError("invalid dimensions or n_steps")
    if not np.allclose(initial.sum(), 1) or not np.allclose(transition.sum(axis=1), 1):
        raise ValueError("probabilities must sum to one")
    occupancy = np.zeros_like(initial)
    distribution = initial.copy()
    for _ in range(n_steps):
        occupancy += distribution
        distribution = distribution @ transition
    return occupancy / n_steps

