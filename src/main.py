import pandas as pd
from yf_utils import load_or_download_yf_data
from indicators import sma_10, sma_20, rsi_14, percent_b, ret_1, ret_5
from ml_model import train_ml_model,model_cls,model_params
from strategy_fn import exec_fn
from position_size import pos_size_handler
from report_utils import print_metrics_report, print_trades_report, print_positions_report
import pybroker
from pybroker import Strategy, StrategyConfig
from pybroker.common import PositionMode 

# 註冊模型到 PyBroker
model_ml = pybroker.model('ml_model', train_ml_model, indicators=[sma_10, sma_20, rsi_14, percent_b, ret_1, ret_5])

# 最多同時持有3檔股票，禁做空
config = StrategyConfig(max_long_positions=3,position_mode=PositionMode.LONG_ONLY)

start_date = "2015-01-01"
end_date = "2025-05-16"
tickers = ['AAPL', 'MSFT', 'AMZN']
# 合併所有股票的歷史資料，先從本地讀取
all_data = pd.concat(
    [load_or_download_yf_data(ticker, start_date, end_date) for ticker in tickers],
    axis=0,
    ignore_index=True
)

strategy = Strategy(all_data, start_date=start_date, end_date=end_date, config=config)
strategy.add_execution(exec_fn, tickers, models=model_ml)

strategy.set_pos_size_handler(pos_size_handler)

# 執行回測（使用 walkforward 多窗口訓練/測試）
result = strategy.walkforward(
    warmup=20,      # 前20天數據用於技術指標計算暖身，不參與交易
    windows=40,      # 將回測區間分成3段進行走勢前推分析（Walkforward）
    train_size=0.5, # 每個窗口用一半資料訓練，後一半資料測試
    lookahead=1     # 預測未來1天，訓練/測試分割時跳過1天以避免未來資料洩漏
)

# 輸出績效指標
print_metrics_report(result.metrics_df, model_cls=model_cls, model_params=model_params)

# 輸出交易紀錄
print_trades_report(result.trades)

# 輸出現有持倉
if not result.positions.empty:
    latest_date = result.positions.index.get_level_values('date').max()
    if pd.notnull(latest_date):
        positions = result.positions.xs(latest_date, level='date').reset_index()
        print_positions_report(positions)
    else:
        print("\n現有持股部位：無持倉 (查無持倉日期)")
else:
    print("\n現有持股部位：無持倉 (回測全程無持倉)")
