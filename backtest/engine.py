import pandas as pd
import numpy as np
from backtest.metrics import sharpe_ratio, max_drawdown, win_rate, annualized_return


class Backtest:
    def __init__(self, data: pd.DataFrame, strategy_fn, initial_capital: float = 100000, commission: float = 0.001):
        self.data = data.copy()
        self.strategy_fn = strategy_fn
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self) -> dict:
        df = self.strategy_fn(self.data)

        cash = self.initial_capital
        position = 0
        portfolio_values = []
        trades = []
        entry_price = None

        for i, row in df.iterrows():
            price = row['Close']
            signal = row.get('signal', 0)

            if signal == 1 and position == 0:
                shares = int(cash / (price * (1 + self.commission)))
                if shares > 0:
                    cost = shares * price * (1 + self.commission)
                    cash -= cost
                    position = shares
                    entry_price = price

            elif signal == -1 and position > 0:
                proceeds = position * price * (1 - self.commission)
                cash += proceeds
                trade_return = (price - entry_price) / entry_price
                trades.append(trade_return)
                position = 0
                entry_price = None

            portfolio_values.append(cash + position * price)

        if position > 0:
            proceeds = position * df['Close'].iloc[-1] * (1 - self.commission)
            cash += proceeds
            trade_return = (df['Close'].iloc[-1] - entry_price) / entry_price
            trades.append(trade_return)
            portfolio_values[-1] = cash

        equity_curve = pd.Series(portfolio_values, index=df.index)
        returns = equity_curve.pct_change().dropna()

        total_ret = (equity_curve.iloc[-1] / self.initial_capital) - 1
        years = len(df) / 252

        results = {
            'equity_curve': equity_curve,
            'total_return': total_ret,
            'annualized_return': annualized_return(total_ret, years),
            'max_drawdown': max_drawdown(equity_curve),
            'sharpe_ratio': sharpe_ratio(returns),
            'win_rate': win_rate(trades),
            'total_trades': len(trades),
        }

        return results
