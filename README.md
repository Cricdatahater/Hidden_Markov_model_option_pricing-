# Hidden_Markov_model_option_pricing-
# 📈 Option Pricing via Hidden Markov Models (HMM) & Real-Time Market Volatility

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![yfinance](https://img.shields.io/badge/data-yfinance-green.svg)](https://pypi.org/project/yfinance/)

An end-to-end Quantitative Finance library in Python that fits a 2-State Gaussian Hidden Markov Model (HMM) to historical asset returns, projects multi-period forward regime transitions, and evaluates option pricing against standard Realized Volatility and real-time market options quotes via `yfinance`.

---

## 📌 Project Overview

Traditional Black-Scholes pricing assumes constant volatility ($\sigma$). However, financial markets exhibit structural regime switching between low-volatility (bullish/sideways) and high-volatility (bearish/crisis) states.

This project implements:
1. **Regime Identification**: Uses EM (`hmmlearn`) to fit a 2-state Gaussian HMM to historical asset log-returns.
2. **Forward State Occupancy**: Projects forward state probability vectors $\pi_t = \pi_0 P^t$ across option maturity $T$.
3. **Effective Volatility Estimation**: Calculates time-weighted variance $\text{Var}(r) = w_0 \sigma_0^2 + w_1 \sigma_1^2$ to produce $\sigma_{\text{HMM}}$.
4. **Market Benchmarking**: Fetches live options chains via Yahoo Finance (`yfinance`) and compares HMM model prices against 30-day Realized Volatility and actual market trading prices.
5. **Bayesian Framework**: Utilises Bayesian Inferential techniques to calculate regime volatility, reducing the bias from initialising wrong values. 

---

## 📌 Features

* **Real-Time Data Pipeline:** Automatically fetches historical daily returns and live options chain data directly from Yahoo Finance (`yfinance`).
* **Bayesian Regime Estimation:** Fits a 2-State Gaussian HMM using Gibbs Sampling with Forward-Filtering Backward-Sampling (FFBS) to estimate transition probabilities $P$ and regime variances $\sigma_k^2$.
* **Convex Mixture Option Pricing:** Preserves fat-tail optionality by evaluating state-mixture Black-Scholes pricing per posterior sample draw rather than pre-averaging variances.
* **Posterior Uncertainty Quantification:** Generates 95% Bayesian Credible Intervals for option prices to assess model parameter uncertainty against live market quotes.
* **Robust Data Filtering:** Handles Yahoo Finance quoting artifacts and illiquid contracts by filtering out zero-bid and corrupt implied volatility rows.

---

## 🧮 Mathematical Framework

### 1. Daily Transition Probability Matrix
Given daily return observations $r_t = \ln(S_t / S_{t-1})$, the underlying state transitions follow a Markov process with transition matrix $P$:

$$P = \begin{bmatrix} P_{00} & P_{01} \\ P_{10} & P_{11} \end{bmatrix}$$

### 2. Forward Time-Occupancy Projection
For $N = \text{round}(T \times 252)$ trading days until expiration, cumulative regime occupancy vector $\mathbf{w} = [w_0, w_1]$ is derived via matrix exponentiation:

$$\mathbf{w} = \frac{1}{N} \sum_{t=1}^{N} \pi_0 P^t, \quad \text{where } \sum w_i = 1.0$$

### 3. Effective HMM Volatility
$$\sigma_{\text{HMM}} = \sqrt{w_0 \sigma_0^2 + w_1 \sigma_1^2}$$

### 4. Bayesian Gaussian HMM (Gibbs Sampler + FFBS)
 Daily log-returns $r_t = \ln(S_t / S_{t-1})$ follow a Gaussian distribution conditioned on unobserved latent regime $z_t \in \{0, 1\}$:$$r_t \mid z_t = k \sim \mathcal{N}(0, \sigma_k^2)$$The Gibbs sampler updates parameters sequentially:Hidden States ($z_{1:T}$): Sampled via Forward-Filtering Backward-Sampling (FFBS).Transition Matrix ($P$): Sampled using a Dirichlet conjugate prior $\text{Dirichlet}(\alpha_0 + N_{ij})$.Regime Variances ($\sigma_k^2$): Sampled using a Conjugate Inverse-Gamma prior $\text{Inv-Gamma}\left(a_0 + \frac{N_k}{2}, b_0 + \frac{\sum r_t^2}{2}\right)$.Identifiability is maintained by enforcing $\sigma_0 < \sigma_1$ across draws (State 0 = Low Volatility, State 1 = High Volatility).
### 5. Convex Regime-Switching Mixture Pricing
 For an option expiring in $T$ years ($N = T \times 252$ steps), state occupancy probabilities $\mathbf{w} = [w_0, w_1]$ are projected using matrix powers $\mathbf{\pi}_0 P^N$.Rather than averaging variance ($\mathbb{E}[BS(\sigma)] \neq BS(\mathbb{E}[\sigma])$), options are priced using Convex Mixture Pricing per posterior draw:$$C_{\text{mixture}} = w_0 \cdot \text{BS}(S_0, K, T, r, \sigma_{0,\text{ann}}) + w_1 \cdot \text{BS}(S_0, K, T, r, \sigma_{1,\text{ann}})$$

---


