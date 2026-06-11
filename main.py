import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 尝试使用系统中文字体
_CN_FONTS = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'SimHei', 'Arial Unicode MS']
for _f in _CN_FONTS:
    if any(_f.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams['font.sans-serif'] = [_f] + plt.rcParams['font.sans-serif']
        break
plt.rcParams['axes.unicode_minus'] = False

from data.fetcher import StockDataFetcher
from backtest.engine import Backtest
from strategy.momentum import momentum_strategy
from strategy.mean_reversion import mean_reversion_strategy
from strategy.moving_average import moving_average_strategy

# A股CPO板块核心标的
# 天孚通信300394 中际旭创300308 新易盛300502 光迅科技002281 华工科技000988 太辰光300570
TICKERS = ['300394.SZ', '300308.SZ', '300502.SZ', '002281.SZ', '000988.SZ', '300570.SZ']
TICKER_NAMES = {
    '300394.SZ': '天孚通信',
    '300308.SZ': '中际旭创',
    '300502.SZ': '新易盛',
    '002281.SZ': '光迅科技',
    '000988.SZ': '华工科技',
    '300570.SZ': '太辰光',
}
START = '2023-01-01'
END = '2024-12-31'

STRATEGIES = {
    'Momentum': momentum_strategy,
    'MeanReversion': mean_reversion_strategy,
    'MovingAverage': moving_average_strategy,
}


def main():
    os.makedirs('results', exist_ok=True)

    fetcher = StockDataFetcher()
    print("获取A股CPO板块数据...")
    data = fetcher.fetch_multiple(TICKERS, START, END)

    rows = []
    equity_curves = {s: {} for s in STRATEGIES}

    for ticker in TICKERS:
        if ticker not in data:
            continue
        name = TICKER_NAMES.get(ticker, ticker)
        df = data[ticker]
        for strat_name, strat_fn in STRATEGIES.items():
            bt = Backtest(df, strat_fn)
            res = bt.run()
            equity_curves[strat_name][ticker] = res['equity_curve']
            rows.append({
                '代码': ticker,
                '名称': name,
                '策略': strat_name,
                '总收益': f"{res['total_return']:.2%}",
                '年化收益': f"{res['annualized_return']:.2%}",
                '最大回撤': f"{res['max_drawdown']:.2%}",
                'Sharpe': f"{res['sharpe_ratio']:.2f}",
                '胜率': f"{res['win_rate']:.2%}",
                '交易次数': res['total_trades'],
            })

    table = pd.DataFrame(rows)
    print("\n=== A股CPO板块策略回测 ===")
    print(table.to_string(index=False))

    fig, axes = plt.subplots(3, 1, figsize=(14, 18))
    labels = [f"{TICKER_NAMES.get(t, t)}({t})" for t in TICKERS]
    for ax, strat_name in zip(axes, STRATEGIES.keys()):
        for ticker, label in zip(TICKERS, labels):
            if ticker in equity_curves[strat_name]:
                ec = equity_curves[strat_name][ticker]
                normalized = ec / ec.iloc[0] * 100
                ax.plot(normalized.index, normalized.values, label=label)
        ax.set_title(f'{strat_name} 策略 — A股CPO板块净值曲线', fontsize=13)
        ax.set_ylabel('净值（基准=100）')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/cpo_equity_curves.png', dpi=150, bbox_inches='tight')
    print("\n净值曲线已保存至 results/cpo_equity_curves.png")


if __name__ == '__main__':
    main()
