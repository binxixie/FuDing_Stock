import numpy as np
import pandas as pd


def sharpe_ratio(returns: pd.Series, risk_free: float = 0.02) -> float:
    excess = returns - risk_free / 252
    std = excess.std()
    if len(excess) < 2 or not np.isfinite(std) or std < 1e-10:
        return 0.0
    return float(np.sqrt(252) * excess.mean() / std)


def max_drawdown(equity_curve: pd.Series) -> float:
    roll_max = equity_curve.cummax()
    drawdown = (equity_curve - roll_max) / roll_max
    return float(drawdown.min())


def calmar_ratio(returns: pd.Series, equity_curve: pd.Series) -> float:
    ann_ret = annualized_return(float((equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1),
                                len(returns) / 252)
    mdd = abs(max_drawdown(equity_curve))
    if mdd == 0:
        return 0.0
    return ann_ret / mdd


def win_rate(trades: list) -> float:
    if not trades:
        return 0.0
    wins = sum(1 for t in trades if t > 0)
    return wins / len(trades)


def annualized_return(total_return: float, years: float) -> float:
    if years <= 0:
        return 0.0
    return float((1 + total_return) ** (1 / years) - 1)
