# FuDing Stock - Quantitative Trading Strategy System

A Python-based quantitative trading system with multiple strategies, a backtesting engine, and performance metrics.

## Project Structure

```
FuDing_Stock/
├── data/
│   └── fetcher.py          # yfinance data fetching
├── strategy/
│   ├── momentum.py         # RSI + MACD momentum strategy
│   ├── mean_reversion.py   # Bollinger Bands mean reversion
│   └── moving_average.py   # MA crossover with trend filter
├── backtest/
│   ├── engine.py           # Backtesting engine
│   └── metrics.py          # Performance metrics
├── results/                # Output charts
├── main.py                 # Entry point
└── requirements.txt
```

## Strategies

- **Momentum**: Buys when RSI < 40 and MACD crosses up; sells when RSI > 70 or MACD crosses down.
- **Mean Reversion**: Buys when price closes below the lower Bollinger Band; sells when price exceeds the upper band or middle band.
- **Moving Average Crossover**: Buys when the 20-day MA crosses above the 50-day MA and price is above the 200-day MA; sells when the 20-day MA crosses below the 50-day MA.

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

Results are printed to the console and equity curves are saved to `results/equity_curves.png`.
