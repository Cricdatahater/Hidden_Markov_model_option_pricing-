import math

import numpy as np

from src.pricing import black_scholes_price, expected_regime_occupancy


def test_put_call_parity():
    args = dict(spot=100, strike=105, maturity=0.5, rate=0.04, volatility=0.2)
    call = black_scholes_price(**args, option_type="call")
    put = black_scholes_price(**args, option_type="put")
    assert abs(call - put - (100 - 105 * math.exp(-0.04 * 0.5))) < 1e-10


def test_absorbing_state_occupancy():
    weights = expected_regime_occupancy([1, 0], [[1, 0], [0, 1]], 100)
    assert np.allclose(weights, [1, 0])
    assert np.isclose(weights.sum(), 1)

