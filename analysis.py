import pandas as pd
import numpy as np
import sqlite3

RISK_FREE_RATE = 0.065

def load_data():
    conn = sqlite3.connect("portfolio.db")
    df = pd.read_sql("SELECT * FROM stock_prices ORDER BY ticker, date", conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

def compute_returns(df):
    df = df.copy().sort_values(["ticker", "date"])
    df["daily_return"] = df.groupby("ticker")["close_price"].pct_change()
    df["cumulative_return"] = df.groupby("ticker")["daily_return"].transform(
        lambda x: (1 + x.fillna(0)).cumprod() - 1
    )
    return df

def compute_metrics(df):
    results = []
    for ticker, grp in df.groupby("ticker"):
        grp = grp.dropna(subset=["daily_return"])
        daily_ret = grp["daily_return"]
        n_days = len(daily_ret)
        ann_return = (1 + daily_ret.mean()) ** 252 - 1
        ann_vol = daily_ret.std() * np.sqrt(252)
        sharpe = (ann_return - RISK_FREE_RATE) / ann_vol if ann_vol > 0 else 0
        cum = (1 + daily_ret).cumprod()
        max_drawdown = ((cum - cum.cummax()) / cum.cummax()).min()
        total_return = cum.iloc[-1] - 1
        win_rate = (daily_ret > 0).sum() / n_days
        results.append({
            "ticker": ticker,
            "start_price": round(grp["close_price"].iloc[0], 2),
            "end_price": round(grp["close_price"].iloc[-1], 2),
            "total_return_pct": round(total_return * 100, 2),
            "ann_return_pct": round(ann_return * 100, 2),
            "ann_volatility_pct": round(ann_vol * 100, 2),
            "sharpe_ratio": round(sharpe, 3),
            "max_drawdown_pct": round(max_drawdown * 100, 2),
            "win_rate_pct": round(win_rate * 100, 2),
            "trading_days": n_days,
        })
    return pd.DataFrame(results).sort_values("sharpe_ratio", ascending=False)

def compute_correlation(df):
    pivot = df.pivot_table(index="date", columns="ticker", values="daily_return")
    return pivot.corr().round(3)

def compute_portfolio(df):
    tickers = df["ticker"].unique()
    weights = {t: 1/len(tickers) for t in tickers}
    pivot = df.pivot_table(index="date", columns="ticker", values="daily_return").dropna()
    port_ret = sum(pivot[t] * w for t, w in weights.items() if t in pivot.columns)
    ann_return = (1 + port_ret.mean()) ** 252 - 1
    ann_vol = port_ret.std() * np.sqrt(252)
    cum = (1 + port_ret).cumprod()
    return {
        "portfolio": "Equal-Weight (10 stocks)",
        "total_return_pct": round((cum.iloc[-1] - 1) * 100, 2),
        "ann_return_pct": round(ann_return * 100, 2),
        "ann_volatility_pct": round(ann_vol * 100, 2),
        "sharpe_ratio": round((ann_return - RISK_FREE_RATE) / ann_vol, 3),
        "max_drawdown_pct": round(((cum - cum.cummax()) / cum.cummax()).min() * 100, 2),
    }

if __name__ == "__main__":
    df = load_data()
    df_ret = compute_returns(df)
    metrics = compute_metrics(df_ret)
    corr = compute_correlation(df_ret)
    port = compute_portfolio(df_ret)

    conn = sqlite3.connect("portfolio.db")
    df_ret.to_sql("stock_returns", conn, if_exists="replace", index=False)
    metrics.to_sql("risk_metrics", conn, if_exists="replace", index=False)
    corr.reset_index().to_sql("correlation_matrix", conn, if_exists="replace", index=False)
    conn.close()

    metrics.to_csv("risk_return_summary.csv", index=False)

    print("\n=== RISK & RETURN METRICS ===")
    print(metrics[["ticker","ann_return_pct","ann_volatility_pct","sharpe_ratio","max_drawdown_pct"]].to_string(index=False))
    print("\n=== EQUAL-WEIGHT PORTFOLIO ===")
    for k, v in port.items():
        print(f"  {k}: {v}")