import streamlit as st
from stock_ai import Market, Account, AITrader, RandomTrader, log_trade

# =========================
# 初始化
# =========================
if "market" not in st.session_state:
    st.session_state.market = Market()

    st.session_state.accounts = {
        "AI": Account("AI"),
        "Random": Account("Random"),
        "You": Account("You")
    }

    st.session_state.ai = AITrader()
    st.session_state.random = RandomTrader()

# =========================
# UI
# =========================
st.title("📈 股票 AI 模擬器")

market = st.session_state.market.next_day()

st.subheader("📊 今日價格")
st.write(market)

# =========================
# AI交易
# =========================
if st.button("🤖 AI交易"):
    ai = st.session_state.ai
    acc = st.session_state.accounts["AI"]

    ai.trade(acc, market, st.session_state.market.history, st.session_state.market.day)

    stock = list(market.keys())[0]
    log_trade("AI", stock, market[stock], "buy", 100)

    st.success("AI 完成交易")

# =========================
# Random交易
# =========================
if st.button("🎲 Random交易"):
    rnd = st.session_state.random
    acc = st.session_state.accounts["Random"]

    rnd.trade(acc, market, st.session_state.market.history, st.session_state.market.day)

    stock = list(market.keys())[0]
    log_trade("Random", stock, market[stock], "buy", 100)

    st.success("Random 完成交易")

# =========================
# 玩家交易
# =========================
stock = st.selectbox("選股票", list(market.keys()))

if st.button("💰 我買！"):
    acc = st.session_state.accounts["You"]

    price = market[stock]
    acc.cash -= price * 100
    acc.positions[stock] = acc.positions.get(stock, 0) + 100

    log_trade("You", stock, price, "buy", 100)

    st.success("已買入")

# =========================
# 顯示資產
# =========================
st.subheader("💰 資產")

for name, acc in st.session_state.accounts.items():
    st.write(f"{name}: {acc.cash}")