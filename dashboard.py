import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="RL Portfolio Trader", layout="wide", page_icon="🤖")

st.title("🤖 RL Portfolio Trader")
st.markdown("**PPO-based agent trading AAPL, TSLA, NVDA, SPY, QQQ, BTC, ETH**")

# Load equity curve
equity = pd.read_csv("real_equity.csv", index_col=0, parse_dates=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Return", "133.7%", "+112.4% vs SPY")
col2.metric("Sharpe Ratio", "2.54", "+1.59 vs SPY")
col3.metric("Max Drawdown", "-15.6%", "vs -50% bear market")
col4.metric("vs SPY Return", "21.3%", "benchmark")

st.divider()

# Equity curve
st.subheader("📈 Equity Curve")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=equity.index,
    y=equity.iloc[:, 0],
    name="RL Agent",
    line=dict(color="#00ff88", width=2)
))
fig.update_layout(template="plotly_dark", height=450,
    xaxis_title="Date", yaxis_title="Portfolio Value")
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("⚠️ Stress Test — 2022 Bear Market")
col1, col2 = st.columns(2)
col1.metric("Return (2022)", "-28.3%")
col2.metric("Max Drawdown (2022)", "-50.1%")
