import pandas as pd
import ta


def mean_reversion_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_middle'] = bb.bollinger_mavg()
    df['bb_lower'] = bb.bollinger_lband()

    df['signal'] = 0
    df.loc[df['Close'] < df['bb_lower'], 'signal'] = 1
    df.loc[(df['Close'] > df['bb_upper']) | (df['Close'] > df['bb_middle']), 'signal'] = -1

    return df
