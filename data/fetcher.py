import yfinance as yf
import pandas as pd
import numpy as np


# Seed prices roughly matching 2022-2024 starting levels
_SEED_PRICES = {'AAPL': 180.0, 'MSFT': 310.0, 'GOOGL': 140.0}
_SEED_DRIFT  = {'AAPL': 0.0003, 'MSFT': 0.0004, 'GOOGL': 0.0002}


def _synthetic(ticker: str, start: str, end: str) -> pd.DataFrame:
    rng = np.random.default_rng(abs(hash(ticker)) % (2**31))
    dates = pd.bdate_range(start=start, end=end)
    n = len(dates)
    price0 = _SEED_PRICES.get(ticker, 100.0)
    drift  = _SEED_DRIFT.get(ticker, 0.0003)
    vol    = 0.015
    returns = rng.normal(drift, vol, n)
    prices  = price0 * np.cumprod(1 + returns)
    noise   = rng.uniform(0.995, 1.005, n)
    df = pd.DataFrame({
        'Open':   prices * rng.uniform(0.99, 1.01, n),
        'High':   prices * rng.uniform(1.00, 1.02, n),
        'Low':    prices * rng.uniform(0.98, 1.00, n),
        'Close':  prices,
        'Volume': (rng.integers(5_000_000, 20_000_000, n)).astype(float),
    }, index=dates)
    df.index.name = 'Date'
    return df


class StockDataFetcher:
    def fetch(self, ticker: str, start: str, end: str, interval: str = '1d') -> pd.DataFrame:
        try:
            df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True, progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df.dropna(inplace=True)
                return df
        except Exception:
            pass
        print(f"  [offline] using synthetic data for {ticker}")
        return _synthetic(ticker, start, end)

    def fetch_multiple(self, tickers: list, start: str, end: str) -> dict:
        result = {}
        for ticker in tickers:
            try:
                result[ticker] = self.fetch(ticker, start, end)
            except Exception as e:
                print(f"Failed to fetch {ticker}: {e}")
        return result
