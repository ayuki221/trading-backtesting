import pandas as pd
import talib
import pybroker

# 布林通道%B計算輔助函式
def percent_b_func(data):
    # 保證 close 欄位為 float array 並補空值
    close = pd.Series(data.close).ffill().astype(float).to_numpy()
    upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
    return (close - lower) / (upper - lower)

# 技術指標定義
sma_10 = pybroker.indicator('sma_10',lambda data: pd.Series(data.close).astype(float).rolling(window=10).mean().to_numpy())
sma_20 = pybroker.indicator('sma_20',lambda data: pd.Series(data.close).astype(float).rolling(window=50).mean().to_numpy())

# 這裡直接使用 talib 的 RSI
rsi_14 = pybroker.indicator('rsi_14',lambda data: talib.RSI(data.close, timeperiod=14))

# 布林通道 %B 指標
percent_b = pybroker.indicator('percent_b', percent_b_func)

ret_1 = pybroker.indicator('ret_1',lambda data: pd.Series(data.close).astype(float).pct_change(periods=1).to_numpy())
ret_5 = pybroker.indicator('ret_5',lambda data: pd.Series(data.close).astype(float).pct_change(periods=5).to_numpy())
