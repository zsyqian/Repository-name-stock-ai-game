import yfinance as yf
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

FEE_RATE = 0.001425
LOT_SIZE = 100
SEASON_LENGTH = 30
TOTAL_DAYS = 60


TICKERS = {
    "2330 台積電": "2330.TW",
    "2454 聯發科": "2454.TW",
    "2317 鴻海": "2317.TW",
    "2308 台達電": "2308.TW",
    "1301 台塑": "1301.TW",
    "1303 南亞": "1303.TW",
    "2881 富邦金": "2881.TW",
    "2882 國泰金": "2882.TW",
    "2002 中鋼": "2002.TW",
    "1216 統一": "1216.TW"
}


# =========================
# 市場
# =========================
class Market:
    def __init__(self):
        self.history = {}

        for name, code in TICKERS.items():
            data = yf.download(code, period="2y")

            if data.empty:
                continue

            close = data["Close"].dropna().values
            self.history[name] = [
                float(x.item()) if hasattr(x, "item") else float(x)
                for x in close
            ]

        self.day = 0
        self.prices = {s: self.history[s][0] for s in self.history}

    def next_day(self):
        self.day += 1
        for s in self.history:
            if self.day < len(self.history[s]):
                self.prices[s] = self.history[s][self.day]
        return self.prices


# =========================
# 帳戶
# =========================
class Account:
    def __init__(self, name):
        self.name = name
        self.cash = 10000000
        self.positions = {}
        self.asset_history = []

    def total_asset(self, market):
        stock_value = sum(qty * market[s] for s, qty in self.positions.items())
        return self.cash + stock_value


# =========================
# AI Trader
# =========================
class AITrader:
    def trade(self, account, market, history, day):

        scores = {}

        for stock in market:
            prices = history[stock][:day+1]
            if len(prices) < 4:
                continue

            r1 = (prices[-1] - prices[-2]) / prices[-2]
            r2 = (prices[-2] - prices[-3]) / prices[-3]

            score = r1 + r2
            scores[stock] = score

        top = sorted(scores, key=scores.get, reverse=True)[:3]

        for stock in top:
            price = market[stock]

            if account.cash > price * LOT_SIZE:
                cost = price * LOT_SIZE
                fee = cost * FEE_RATE

                account.cash -= (cost + fee)
                account.positions[stock] = account.positions.get(stock, 0) + LOT_SIZE


# =========================
# Random Trader
# =========================
class RandomTrader:
    def trade(self, account, market, history, day):
        stock = random.choice(list(market.keys()))
        price = market[stock]

        if account.cash > price * LOT_SIZE:
            cost = price * LOT_SIZE
            fee = cost * FEE_RATE

            account.cash -= (cost + fee)
            account.positions[stock] = account.positions.get(stock, 0) + LOT_SIZE


# =========================
# 主程式（給 Streamlit 用）
# =========================
def main():

    market = Market()

    traders = [
        {"account": Account("AI"), "strategy": AITrader()},
        {"account": Account("Random"), "strategy": RandomTrader()},
    ]

    for day in range(TOTAL_DAYS):

        prices = market.next_day()

        for t in traders:
            t["strategy"].trade(
                t["account"],
                prices,
                market.history,
                market.day
            )

        for t in traders:
            acc = t["account"]
            acc.asset_history.append(acc.total_asset(prices))

    return traders