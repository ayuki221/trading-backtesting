import pandas as pd
from yf_utils import load_or_download_yf_data
from indicators import sma_10, sma_20, rsi_14, percent_b, ret_1, ret_5
from ml_model import train_ml_model, model_cls, model_params
from strategy_fn import exec_fn
from position_size import pos_size_handler
from report_utils import print_metrics_report, print_trades_report, print_positions_report
import pybroker
from pybroker import Strategy, StrategyConfig
from pybroker.common import PositionMode

# 設定參數
start_date = "2015-01-01"
end_date = "2025-05-16"
tickers = ['AAPL', 'MSFT', 'AMZN']
warmup = 20
window_size = 30
step = 20

# 讀取資料
all_data = pd.concat(
    [load_or_download_yf_data(ticker, start_date, end_date) for ticker in tickers],
    axis=0,
    ignore_index=True
)
all_data["date"] = pd.to_datetime(all_data["date"])
all_data = all_data.set_index("date")
all_data["date"] = all_data.index

# 建立模型
model_ml = pybroker.model('ml_model', train_ml_model, indicators=[sma_10, sma_20, rsi_14, percent_b, ret_1, ret_5])
config = StrategyConfig(max_long_positions=3, position_mode=PositionMode.LONG_ONLY)

# 產生 splits
date_index = all_data.index.unique().sort_values()
all_results = []
previous_window_data = None

for window_start in range(0, len(date_index) - window_size, step):
    warmup_start = max(0, window_start - warmup)
    window_end = window_start + window_size
    if window_end > len(date_index):  # 避免超出
        break
    window_dates = date_index[warmup_start:window_end]
    window_data = all_data.loc[window_dates].copy()
    
    # warmup 資料不足就借前一段
    current_days = len(window_data)
    if current_days < warmup and previous_window_data is not None:
        needed = warmup - current_days
        extra_dates = previous_window_data.index[-needed:]
        extra_data = previous_window_data.loc[extra_dates]
        window_data = pd.concat([extra_data, window_data])
        window_data = window_data[~window_data.index.duplicated(keep='last')]

    # 回測績效起訖日
    perf_start_idx = min(warmup, len(window_data) - 1)
    perf_start = window_data.index[perf_start_idx]
    perf_end = window_data.index[-1]

    # 初始化策略與回測
    strategy = Strategy(
        window_data,
        start_date=perf_start,
        end_date=perf_end,
        config=config
    )
    strategy.add_execution(exec_fn, tickers, models=model_ml)
    strategy.set_pos_size_handler(pos_size_handler)
    
    result = strategy.backtest(
        warmup=20,
        lookahead=1,
        train_size=0.5,
    )
    all_results.append(result)
    previous_window_data = window_data.copy()

# 合併所有 window 的績效
metrics_dfs = [res.metrics_df for res in all_results]
all_metrics = pd.concat(metrics_dfs, ignore_index=True)
print_metrics_report(all_metrics, model_cls=model_cls, model_params=model_params)

# 合併所有 window 的交易紀錄
trades_dfs = [res.trades for res in all_results]
all_trades = pd.concat(trades_dfs, ignore_index=True)
print_trades_report(all_trades)

# 輸出現有持倉（只看最後一個 window）
result = all_results[-1]
if not result.positions.empty:
    latest_date = result.positions.index.get_level_values('date').max()
    if pd.notnull(latest_date):
        positions = result.positions.xs(latest_date, level='date').reset_index()
        print_positions_report(positions)
    else:
        print("\n現有持股部位：無持倉 (查無持倉日期)")
else:
    print("\n現有持股部位：無持倉 (回測全程無持倉)")
