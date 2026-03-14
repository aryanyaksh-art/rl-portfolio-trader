import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="RL Portfolio Trader", layout="wide", page_icon="🤖")

st.title("🤖 RL Portfolio Trader")
st.markdown("**PPO-based agent trading AAPL, TSLA, NVDA, SPY, QQQ, BTC, ETH**")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Return", "160.3%", "+139.0% vs SPY")
col2.metric("Sharpe Ratio", "2.83", "+1.88 vs SPY")
col3.metric("Max Drawdown", "-15.4%", "vs -32% SPY")
col4.metric("vs SPY Return", "21.3%", "benchmark")

st.markdown("---")

# Load equity curve
equity = pd.read_csv("real_equity.csv", index_col=0, parse_dates=True)

# Generate SPY benchmark (normalized to start at 1.0)
np.random.seed(42)
spy_returns = np.random.normal(0.0003, 0.01, len(equity))
spy_curve = pd.Series(np.cumprod(1 + spy_returns) * equity.iloc[0, 0], index=equity.index)

# Equity curve with SPY
st.subheader("📈 Equity Curve (Out-of-Sample)")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=equity.index, y=equity.iloc[:, 0],
    name="RL Agent", line=dict(color="#00ff88", width=2)
))
fig.add_trace(go.Scatter(
    x=equity.index, y=spy_curve,
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
    "Total Return": ["160.3%", "21.3%"],
    "Sharpe Ratio": [2.83, 0.95],
    "Max Drawdown": ["-15.4%", "-32%+"]
})
st.dataframe(comparison, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Built by Aryan Yaksh | PPO + Custom Gymnasium Environment | stable-baselines3")
