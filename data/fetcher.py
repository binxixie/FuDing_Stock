import yfinance as yf
import pandas as pd


class StockDataFetcher:
    def fetch(self, ticker: str, start: str, end: str, interval: str = '1d') -> pd.DataFrame:
        df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=True, progress=False)
        if df.empty:
            raise ValueError(f"No data returned for {ticker}")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.dropna(inplace=True)
        return df

    def fetch_multiple(self, tickers: list, start: str, end: str) -> dict:
        result = {}
        for ticker in tickers:
            try:
                result[ticker] = self.fetch(ticker, start, end)
            except Exception as e:
                print(f"Failed to fetch {ticker}: {e}")
        return result
