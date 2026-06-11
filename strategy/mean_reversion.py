import pandas as pd


def mean_reversion_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    df['bb_middle'] = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    df['bb_upper'] = df['bb_middle'] + 2 * std
    df['bb_lower'] = df['bb_middle'] - 2 * std

    df['signal'] = 0
    df.loc[df['Close'] < df['bb_lower'], 'signal'] = 1
    df.loc[(df['Close'] > df['bb_upper']) | (df['Close'] > df['bb_middle']), 'signal'] = -1

    return df
