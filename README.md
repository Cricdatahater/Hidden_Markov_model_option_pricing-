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

---


