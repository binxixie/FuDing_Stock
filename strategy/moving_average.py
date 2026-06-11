import pandas as pd
import ta


def moving_average_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    df['ma_fast'] = ta.trend.SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['ma_slow'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['ma_200'] = ta.trend.SMAIndicator(close=df['Close'], window=200).sma_indicator()

    fast_cross_up = (df['ma_fast'] > df['ma_slow']) & (df['ma_fast'].shift(1) <= df['ma_slow'].shift(1))
    fast_cross_down = (df['ma_fast'] < df['ma_slow']) & (df['ma_fast'].shift(1) >= df['ma_slow'].shift(1))

    df['signal'] = 0
    df.loc[fast_cross_up & (df['Close'] > df['ma_200']), 'signal'] = 1
    df.loc[fast_cross_down, 'signal'] = -1

    return df
