import numpy as np
import pandas as pd
import sqlite3
import os

np.random.seed(42)

STOCKS = {
    "TCS":        (3820,  4190,  0.22, "IT"),
    "INFY":       (1880,  1820,  0.28, "IT"),
    "HDFCBANK":   (1680,  1760,  0.20, "Banking"),
    "RELIANCE":   (2460,  2910,  0.24, "Energy"),
    "ITC":        (222,   480,   0.26, "FMCG"),
    "HINDUNILVR": (2510,  2320,  0.19, "FMCG"),
    "SBIN":       (472,   790,   0.32, "Banking"),
    "ICICIBANK":  (790,   1280,  0.27, "Banking"),
    "LT":         (1920,  3650,  0.28, "Infrastructure"),
    "MARUTI":     (8600,  12400, 0.25, "Auto"),
}

def get_market_factor(dates):
    factors = []
    for d in dates:
        yr = d.year; mo = d.month
        if yr == 2022:
            factors.append(-0.0004 if mo <= 6 else 0.0001)
        elif yr == 2023: factors.append(0.0003)
        elif yr == 2024: factors.append(0.0004)
        else:            factors.append(-0.0001)
    return np.array(factors)

def generate_prices(ticker, start_price, end_price, ann_vol, dates):
    n = len(dates)
    dt = 1/252
    years = n / 252
    mu = np.log(end_price / start_price) / years + 0.5 * ann_vol**2
    market_factor = get_market_factor(dates)
    daily_vol = ann_vol * np.sqrt(dt)
    market_shocks = np.random.standard_normal(n) * 0.0015
    idio_shocks   = np.random.standard_normal(n) * daily_vol * 0.85
    log_returns = (mu * dt) + market_factor + 0.4*market_shocks + 0.6*idio_shocks
    prices = np.exp(np.log(start_price) + np.cumsum(log_returns))
    return np.round(prices * (end_price / prices[-1]), 2)

def generate_all():
    all_dates = pd.bdate_range("2022-01-03", "2025-12-26", freq="B")
    np.random.seed(0)
    all_dates = all_dates.delete(sorted(np.random.choice(len(all_dates), size=48, replace=False)))

    rows = []
    for ticker, (start, end, vol, sector) in STOCKS.items():
        for date, price in zip(all_dates, generate_prices(ticker, start, end, vol, all_dates)):
            rows.append({"date": date.date(), "ticker": ticker, "close_price": price, "sector": sector})

    df = pd.DataFrame(rows).sort_values(["ticker", "date"])
    df.to_csv("stock_prices.csv", index=False)
    conn = sqlite3.connect("portfolio.db")
    df.to_sql("stock_prices", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Done — {len(df)} rows generated")
    return df

if __name__ == "__main__":
    generate_all()