import pandas as pd


def _rsi(close, window=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)


def _ema(close, span):
    return close.ewm(span=span, adjust=False).mean()


def _roc(close, window=10):
    return (close - close.shift(window)) / close.shift(window) * 100


def momentum_strategy(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    df['rsi'] = _rsi(df['Close'])

    ema_fast = _ema(df['Close'], 12)
    ema_slow = _ema(df['Close'], 26)
    df['macd'] = ema_fast - ema_slow
    df['macd_signal'] = _ema(df['macd'], 9)

    df['roc'] = _roc(df['Close'])

    macd_cross_up = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
    macd_cross_down = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))

    df['signal'] = 0
    df.loc[(df['rsi'] < 40) & macd_cross_up, 'signal'] = 1
    df.loc[(df['rsi'] > 70) | macd_cross_down, 'signal'] = -1

    return df
