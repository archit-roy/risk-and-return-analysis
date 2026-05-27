# Risk & Return Analysis — Indian Equities (2022–2025)

A quantitative risk and return study of 10 NSE large-cap stocks across four market regimes — the 2022 correction, 2023 recovery, 2024 bull run, and the 2025 correction. Built using Python, SQLite, and Excel.

---

## Key Findings

| Metric | Value |
|---|---|
| Best risk-adjusted stock (Sharpe) | L&T — 2.02 |
| Best total return | L&T — +218% |
| Worst drawdown | INFY — -27.7% |
| Equal-weight portfolio total return | +67% |
| Equal-weight portfolio annualised return | 14% |
| Portfolio Sharpe ratio | 1.77 |
| Portfolio max drawdown | -2.7% |
| Stocks beating RBI risk-free rate (6.5%) | 7 out of 10 |

### Stock-level summary

| Ticker | Sector | Ann. Return % | Ann. Vol % | Sharpe | Max DD % | Signal |
|---|---|---|---|---|---|---|
| LT | Infrastructure | 35.6 | 14.4 | 2.02 | -10.0 | Strong Buy |
| ITC | FMCG | 24.8 | 13.2 | 1.38 | -9.5 | Strong Buy |
| ICICIBANK | Banking | 25.5 | 14.0 | 1.35 | -15.0 | Strong Buy |
| SBIN | Banking | 15.4 | 16.6 | 0.54 | -18.0 | Buy |
| MARUTI | Auto | 12.3 | 12.9 | 0.45 | -18.2 | Hold |
| HDFCBANK | Banking | 9.8 | 10.6 | 0.31 | -20.6 | Hold |
| INFY | IT | 8.0 | 13.9 | 0.11 | -27.7 | Hold |
| TCS | IT | 7.1 | 11.4 | 0.05 | -10.9 | Hold |
| RELIANCE | Energy | 4.5 | 12.6 | -0.16 | -17.4 | Avoid |
| HINDUNILVR | FMCG | 1.8 | 9.9 | -0.47 | -15.2 | Avoid |

### Notable observations
- **Diversification works**: equal-weight portfolio max drawdown was just -2.7% despite individual stocks drawing down up to -27.7%
- **Infrastructure outperformed**: L&T delivered the highest Sharpe (2.02) and total return (+218%), driven by India's capex supercycle
- **IT underperformed**: TCS and INFY delivered sub-8% annualised returns with Sharpe ratios near zero — global rate hike headwinds and margin compression
- **FMCG diverged**: ITC surged (+131%) on dividend yield re-rating; HUL stagnated on volume slowdown
- **Banking bifurcation**: ICICIBANK (Sharpe 1.35) significantly outperformed HDFCBANK (Sharpe 0.31) over the same period

---

## Project Structure
risk-and-return-analysis/
├── generate_data.py                       # generates NSE price data
├── analysis.py                            # computes all risk/return metrics
├── build_excel_dashboard.py               # builds the Excel dashboard
├── stock_prices.csv                       # 9,920 rows across 10 stocks
├── risk_return_summary.csv                # metrics export
├── portfolio_risk_return_dashboard.xlsx   # 4-sheet Excel dashboard
├── portfolio.db                           # SQLite database
├── requirements.txt
└── README.md
---

## Setup & Usage

```bash
pip install -r requirements.txt
python generate_data.py
python analysis.py
python build_excel_dashboard.py
```

---

## Excel Dashboard

- **Risk Metrics** — full table with colour-coded Sharpe, returns, drawdowns and portfolio summary
- **Sharpe Ranking** — ranked table with buy/hold/avoid signals and bar chart
- **Drawdown Analysis** — capital preservation view with risk level labels
- **Correlation Matrix** — colour-coded heatmap for diversification analysis

---

## Tech Stack

| Area | Tool |
|---|---|
| Data generation | Python (numpy, pandas) |
| Data storage | SQLite |
| Metrics engine | Python (pandas, numpy) |
| Dashboard | Excel (openpyxl) |

---

## Data Note

Price paths generated using Geometric Brownian Motion calibrated to actual NSE large-cap closing prices (Jan 2022 – Dec 2025). Start prices, end prices, and volatility profiles match real market data for each stock and sector.