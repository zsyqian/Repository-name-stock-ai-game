import streamlit as st
from stock_ai import Market, Account, AITrader, RandomTrader
import pandas as pd
import os
from datetime import datetime


def log_trade(player, action, stock, price, qty):
    file = "trade_log.csv"

    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "player": player,
        "action": action,
        "stock": stock,
        "price": price,
        "qty": qty
    }

    df = pd.DataFrame([data])

    if os.path.exists(file):
        df.to_csv(file, mode='a', header=False, index=False)
    else:
        df.to_csv(file, index=False)

st.title("📈 股票AI模擬器")

# =========================
# 初始化（只做一次）
# =========================
if "started" not in st.session_state:

    st.session_state.started = False

    st.session_state.market = Market()

    st.session_state.accounts = [
        Account("AI"),
        Account("Random")
    ]

    st.session_state.strategies = [
        AITrader(),
        RandomTrader()
    ]


# =========================
# 開始按鈕
# =========================
if st.button("開始模擬"):
    st.session_state.started = True


# =========================
# 主流程
# =========================
if st.session_state.started:

    market = st.session_state.market.next_day()

    st.subheader("📊 今日價格")
    st.write(market)

    st.subheader("🎮 操作")

    col1, col2, col3 = st.columns(3)

    # AI
    with col1:
        if st.button("AI交易"):
            trader = st.session_state.strategies[0]
            acc = st.session_state.accounts[0]

            market = st.session_state.market.next_day()

            trader.trade(
                acc,
                market,
                st.session_state.market.history,
                st.session_state.market.day
            )

            # 🔥 記錄（範例：記第一檔股票）
            stock = list(market.keys())[0]
            log_trade("AI", "buy", stock, market[stock], 100)

    # Random
    with col2:
        if st.button("Random交易"):
            trader = st.session_state.strategies[1]
            acc = st.session_state.accounts[1]

            market = st.session_state.market.next_day()

            trader.trade(
                acc,
                market,
                st.session_state.market.history,
                st.session_state.market.day
            )

            stock = list(market.keys())[0]
            log_trade("Random", "buy", stock, market[stock], 100)

    # 下一天
    with col3:
        if st.button("下一天"):
            st.rerun()


    st.subheader("💰 資產")

    for acc in st.session_state.accounts:
        total = acc.total_asset(market)
        st.write(f"{acc.name}: {total:,.0f}")