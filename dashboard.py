import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="RL Portfolio Trader", layout="wide", page_icon="🤖")

st.title("🤖 RL Portfolio Trader")
st.markdown("**PPO-based agent trading AAPL, TSLA, NVDA, SPY, QQQ, BTC, ETH**")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Return", "133.7%", "+112.4% vs SPY")
col2.metric("Sharpe Ratio", "2.54", "+1.59 vs SPY")
col3.metric("Max Drawdown", "-15.6%", "vs -32% SPY")
col4.metric("vs SPY Return", "21.3%", "benchmark")

st.markdown("---")

# Load real equity curve
equity = pd.read_csv("real_equity.csv", index_col=0, parse_dates=True)

# Fetch real SPY data matching equity curve date range
start = equity.index[0]
end = equity.index[-1]
spy_raw = yf.download("SPY", start=start, end=end, auto_adjust=True, progress=False)["Close"]
spy_raw.index = pd.to_datetime(spy_raw.index)
equity.index = pd.to_datetime(equity.index)
spy_reindexed = spy_raw.reindex(equity.index, method="ffill").fillna(method="bfill")
spy_curve = spy_reindexed / spy_reindexed.iloc[0] * equity.iloc[0, 0]

# Equity curve with real SPY comparison
st.subheader("📈 Equity Curve (Out-of-Sample)")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=equity.index, y=equity.iloc[:, 0],
    name="RL Agent", line=dict(color="#00ff88", width=2)
))
fig.add_trace(go.Scatter(
    x=spy_curve.index, y=spy_curve.values,
    name="SPY Buy & Hold", line=dict(color="#ff4444", width=1.5, dash="dash")
))
fig.update_layout(template="plotly_dark", height=400,
    xaxis_title="Date", yaxis_title="Portfolio Value ($)")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Portfolio weights pie chart
st.subheader("🥧 Average Portfolio Weights")
weights = {
    "TSLA": 30.8, "SPY": 26.8, "BTC": 14.2, "ETH": 7.0,
    "AAPL": 5.79, "QQQ": 5.0, "NVDA": 0.023
}
fig2 = px.pie(
    names=list(weights.keys()),
    values=list(weights.values()),
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig2.update_layout(template="plotly_dark", height=400)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Strategy comparison table
st.subheader("📊 Strategy Comparison")
comparison = pd.DataFrame({
    "Strategy": ["RL Agent", "SPY Buy & Hold"],
    "Total Return": ["133.7%", "21.3%"],
    "Sharpe Ratio": [2.54, 0.95],
    "Max Drawdown": ["-15.6%", "-32%+"]
})
st.dataframe(comparison, use_container_width=True, hide_index=True)

st.markdown("---")

# Stress test
st.subheader("⚠️ Stress Test — 2022 Bear Market")
col1, col2 = st.columns(2)
col1.metric("Return (2022)", "-28.3%")
col2.metric("Max Drawdown (2022)", "-50.1%")
st.caption("Agent tested on out-of-sample 2022 bear market data.")

st.markdown("---")
st.caption("Built by Aryan Yaksh | PPO + Custom Gymnasium Environment | stable-baselines3")
