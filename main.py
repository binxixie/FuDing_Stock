import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from data.fetcher import StockDataFetcher
from backtest.engine import Backtest
from strategy.momentum import momentum_strategy
from strategy.mean_reversion import mean_reversion_strategy
from strategy.moving_average import moving_average_strategy

TICKERS = ['AAPL', 'MSFT', 'GOOGL']
START = '2022-01-01'
END = '2024-12-31'

STRATEGIES = {
    'Momentum': momentum_strategy,
    'MeanReversion': mean_reversion_strategy,
    'MovingAverage': moving_average_strategy,
}


def main():
    os.makedirs('results', exist_ok=True)

    fetcher = StockDataFetcher()
    print("Fetching data...")
    data = fetcher.fetch_multiple(TICKERS, START, END)

    rows = []
    equity_curves = {s: {} for s in STRATEGIES}

    for ticker in TICKERS:
        if ticker not in data:
            continue
        df = data[ticker]
        for strat_name, strat_fn in STRATEGIES.items():
            bt = Backtest(df, strat_fn)
            res = bt.run()
            equity_curves[strat_name][ticker] = res['equity_curve']
            rows.append({
                'Ticker': ticker,
                'Strategy': strat_name,
                'Total Return': f"{res['total_return']:.2%}",
                'Ann. Return': f"{res['annualized_return']:.2%}",
                'Max Drawdown': f"{res['max_drawdown']:.2%}",
                'Sharpe': f"{res['sharpe_ratio']:.2f}",
                'Win Rate': f"{res['win_rate']:.2%}",
                'Trades': res['total_trades'],
            })

    table = pd.DataFrame(rows)
    print("\n=== Strategy Comparison ===")
    print(table.to_string(index=False))

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    for ax, strat_name in zip(axes, STRATEGIES.keys()):
        for ticker in TICKERS:
            if ticker in equity_curves[strat_name]:
                ec = equity_curves[strat_name][ticker]
                normalized = ec / ec.iloc[0] * 100
                ax.plot(normalized.index, normalized.values, label=ticker)
        ax.set_title(f'{strat_name} Strategy - Equity Curves (AAPL, MSFT, GOOGL)')
        ax.set_ylabel('Portfolio Value (indexed to 100)')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/equity_curves.png', dpi=150)
    print("\nEquity curves saved to results/equity_curves.png")


if __name__ == '__main__':
    main()
