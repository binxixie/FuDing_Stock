import pandas as pd


def moving_average_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    df['ma_fast'] = df['Close'].rolling(20).mean()
    df['ma_slow'] = df['Close'].rolling(50).mean()
    df['ma_200'] = df['Close'].rolling(200).mean()

    fast_cross_up = (df['ma_fast'] > df['ma_slow']) & (df['ma_fast'].shift(1) <= df['ma_slow'].shift(1))
    fast_cross_down = (df['ma_fast'] < df['ma_slow']) & (df['ma_fast'].shift(1) >= df['ma_slow'].shift(1))

    df['signal'] = 0
    df.loc[fast_cross_up & (df['Close'] > df['ma_200']), 'signal'] = 1
    df.loc[fast_cross_down, 'signal'] = -1

    return df
