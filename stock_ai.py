import yfinance as yf
import pandas as pd
import numpy as np
import random
from sklearn.linear_model import LogisticRegression

# =========================
# 記錄交易（AI學習資料）
# =========================
def log_trade(player, stock, price, action, qty):
    file = "trade_log.csv"

    data = {
        "player": player,
        "stock": stock,
        "price": price,
        "action": action,
        "qty": qty
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv(file)
        df = pd.concat([old, df])
    except:
        pass

    df.to_csv(file, index=False)

# =========================
# 市場
# =========================
class Market:
    def __init__(self):
        self.history = {}
        self.day = 0

        tickers = ["2330.TW", "2454.TW", "2317.TW"]

        for t in tickers:
            data = yf.download(t, period="1y")
            self.history[t] = data["Close"].dropna().tolist()

    def next_day(self):
        self.day += 1
        prices = {}

        for t in self.history:
            if self.day < len(self.history[t]):
                prices[t] = float(self.history[t][self.day])
            else:
                prices[t] = float(self.history[t][-1])

        return prices

# =========================
# 帳戶
# =========================
class Account:
    def __init__(self, name):
        self.name = name
        self.cash = 1000000
        self.positions = {}

    def total_asset(self, market):
        return self.cash

# =========================
# AI Trader（會學習）
# =========================
class AITrader:
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def learn_from_log(self):
        try:
            df = pd.read_csv("trade_log.csv")
        except:
            return

        if len(df) < 10:
            return

        X = df[["price", "qty"]]
        y = (df["action"] == "buy").astype(int)

        self.model.fit(X, y)
        self.trained = True

    def trade(self, account, market, history, day):

        self.learn_from_log()

        stock = list(market.keys())[0]
        price = market[stock]

        if self.trained:
            prob = self.model.predict_proba([[price, 100]])[0][1]
        else:
            prob = random.random()

        if prob > 0.5:
            account.cash -= price * 100
            account.positions[stock] = account.positions.get(stock, 0) + 100

# =========================
# Random Trader
# =========================
class RandomTrader:
    def trade(self, account, market, history, day):
        stock = list(market.keys())[0]
        price = market[stock]

        account.cash -= price * 100
        account.positions[stock] = account.positions.get(stock, 0) + 100