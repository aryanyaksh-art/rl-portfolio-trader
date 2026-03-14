
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="RL Portfolio Trader", layout="wide")

st.title("🤖 RL Portfolio Trader")
st.markdown("**PPO-based agent trading AAPL, TSLA, NVDA, SPY, QQQ, BTC, ETH**")

# Real metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Return", "133.7%", "+112.4% vs SPY")
col2.metric("Sharpe Ratio", "2.54", "+1.59 vs SPY")
col3.metric("Max Drawdown", "-15.6%", "vs -50% bear market")
col4.metric("vs SPY Return", "21.3%", "benchmark")

st.markdown("---")

# Load real equity curve
equity = pd.read_csv('/content/drive/MyDrive/RL Portfolio Trader/quant_trader/real_equity.csv', index_col=0, parse_dates=True)

# Real equity curve chart
st.subheader("📈 Equity Curve (Out-of-Sample, with 0.1% slippage)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=equity.index, y=equity['portfolio_value'], name="RL Agent", line=dict(color="#00ff88", width=2)))
fig.add_trace(go.Scatter(x=equity.index, y=equity['spy_value'], name="SPY Buy & Hold", line=dict(color="#ff6b6b", width=2)))
fig.update_layout(template="plotly_dark", height=400, yaxis_title="Portfolio Value ($1 invested)")
st.plotly_chart(fig, use_container_width=True)

# Stress test results
st.subheader("🔥 Stress Test (2022 Bear Market)")
col1, col2, col3 = st.columns(3)
col1.metric("Return", "-28.3%", "vs -18% SPY")
col2.metric("Sharpe", "-0.28", "negative in bear market")
col3.metric("Max Drawdown", "-50.1%", "worst case")
st.warning("⚠️ Agent trained on bull market data — underperforms in sustained downturns. Next step: train on diverse market regimes.")

st.markdown("---")

# Comparison table
st.subheader("📊 Strategy Comparison")
df = pd.DataFrame({
    "Strategy":      ["RL Agent (bull)", "RL Agent (bear)", "SPY Buy & Hold"],
    "Total Return":  ["133.7%", "-28.3%", "21.3%"],
    "Sharpe Ratio":  [2.54, -0.28, 0.95],
    "Max Drawdown":  ["-15.6%", "-50.1%", "-18%"],
})
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("Built by Aryan Yaksh | PPO + Custom Gymnasium Environment | stable-baselines3 | Includes 0.1% slippage")
