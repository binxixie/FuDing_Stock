import pandas as pd
import ta


def momentum_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    df['rsi'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    macd = ta.trend.MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    df['roc'] = ta.momentum.ROCIndicator(close=df['Close'], window=10).roc()

    df['macd_cross_up'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
    df['macd_cross_down'] = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))

    df['signal'] = 0
    df.loc[(df['rsi'] < 40) & df['macd_cross_up'], 'signal'] = 1
    df.loc[(df['rsi'] > 70) | df['macd_cross_down'], 'signal'] = -1

    df.drop(columns=['macd_cross_up', 'macd_cross_down'], inplace=True)

    return df
