# Regime-Switching Volatility & Option-Pricing Experiments

An exploratory quantitative-finance project that uses two-state Gaussian hidden Markov models to study volatility regimes and feed regime-weighted volatility assumptions into European option-pricing experiments.

## Implemented work

- frequentist two-state Gaussian HMM fitting with `hmmlearn`;
- forward regime-occupancy projection over an option horizon;
- a custom Gibbs sampler with forward-filtering backward-sampling for a zero-mean Bayesian Gaussian HMM;
- posterior option-price distributions and credible intervals;
- optional comparison with current AAPL prices and option-chain quotes from `yfinance`.

The notebook is an experiment, not a trading system. It does not include transaction costs, dividends, early exercise, slippage, survivorship-bias controls, or a historical out-of-sample backtest.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
jupyter lab HMM_Black_Scholes.ipynb
```

Live-data cells depend on Yahoo Finance availability and will change over time. The tests cover deterministic mathematical invariants without network access.

## Verified pricing API

```python
from src.pricing import black_scholes_price, expected_regime_occupancy

call = black_scholes_price(spot=100, strike=100, maturity=0.5,
                           rate=0.04, volatility=0.20, option_type="call")
weights = expected_regime_occupancy([1, 0], [[0.98, 0.02], [0.10, 0.90]], 126)
```

## Important audit notes

- The original notebook's `option_type == ['call', 'Call']` comparison never matches a string, so that function returns the put branch for `"call"`. The tested module corrects this.
- Sorting regimes requires relabelling every state-dependent object consistently. This should receive additional simulation-recovery tests before research use.
- A convex mixture of Black–Scholes prices is a modelling choice; it is not equivalent to a complete regime-switching option-pricing derivation.
- Credible intervals reflect the stated HMM and priors, not total market/model uncertainty.

## Structure

```text
.
├── HMM_Black_Scholes.ipynb  # exploratory frequentist/Bayesian experiments
├── src/pricing.py            # tested pricing and occupancy primitives
├── tests/test_pricing.py
├── requirements.txt
└── README.md
```

## Highest-value next steps

1. Split the HMM sampler, data acquisition, diagnostics, and pricing engine into modules.
2. Add trace plots, effective sample size, convergence diagnostics, and prior-sensitivity checks.
3. Freeze a dated market-data snapshot and add a walk-forward evaluation against simple volatility baselines.
4. Report error metrics by moneyness and maturity; document dividends and rate sources.

