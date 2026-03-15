# 🤖 RL Portfolio Trader

A reinforcement learning agent that learns to trade a multi-asset portfolio using PPO (Proximal Policy Optimization). Built end-to-end from data pipeline to live Streamlit dashboard.

**[Live Dashboard](https://rl-portfolio-trader-s4dynp4sgwtjr2r6wxejik.streamlit.app)**

---

## Results (Out-of-Sample Backtest)

| Metric | RL Agent | SPY Buy & Hold |
|---|---|---|
| Total Return | **133.7%** | 21.3% |
| Sharpe Ratio | **2.54** | 0.95 |
| Max Drawdown | **-15.6%** | ~-32% |

> Test period: Mar 2025 – Mar 2026 (never seen during training). 0.1% slippage applied per trade.

### Stress Test — 2022 Bear Market
| Metric | Result |
|---|---|
| Return | -28.3% |
| Max Drawdown | -50.1% |

The agent is long-only and struggles in sustained bear markets — an honest limitation documented in the dashboard.

---

## How It Works

**Data pipeline** — yfinance fetches OHLCV data for 7 assets: AAPL, TSLA, NVDA, SPY, QQQ, BTC-USD, ETH-USD

**Feature engineering** — 38 features per timestep including RSI, MACD, Bollinger Bands, rolling volatility, cross-asset correlations, momentum signals

**Custom Gymnasium environment** — continuous action space (portfolio weights), transaction cost penalty (0.1% slippage), reward = risk-adjusted daily return

**PPO agent** — trained with stable-baselines3 for 500k timesteps

**Train/Test split**
- Train: 2021-05-08 → 2025-03-20 (80%)
- Test: 2025-03-21 → 2026-03-09 (20%, never seen during training)

---

## Tech Stack

Python · pandas · numpy · yfinance · Gymnasium · stable-baselines3 · Streamlit · Plotly

---

## Limitations

1. **Long-only** — cannot short, so bear markets cause large drawdowns
2. **Survivorship bias** — universe limited to known winners (AAPL, NVDA, BTC, etc.)
3. **Optimistic slippage** — 0.1% is conservative; real crypto costs can be 0.2–0.5%+
4. **Bull market test period** — out-of-sample period was predominantly bullish
5. **Not live tested** — backtests don't capture liquidity or order book impact

---

## Next Steps

- Add short positions to handle bear markets
- Train across multiple market regimes
- Paper trade live via broker API to validate real-world performance

---

Built by Aryan Yaksh | PPO + Custom Gymnasium Environment | stable-baselines3
