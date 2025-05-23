import pandas as pd
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor

# 支援的模型參數字典（依模型class指向其參數）
MODEL_PARAM_TABLE = {
    XGBRegressor: {
        "n_estimators": 200,
        "max_depth": 20,
        "random_state": 8,
    },
    LGBMRegressor: {
        "n_estimators": 500,
        "max_depth": 10,
        "random_state": 8,
        "verbosity": -1,
    },
    RandomForestRegressor: {
        "n_estimators": 600,
        "max_depth": 20,
        "random_state": 42,
    },
}

# 只需改這個名稱，參數自動選正確的
model_cls = RandomForestRegressor  # ← 換成 LGBMRegressor 或 RandomForestRegressor 即可

# 自動選對應參數
model_params = MODEL_PARAM_TABLE[model_cls]

def train_ml_model(symbol: str, train_data: pd.DataFrame, test_data: pd.DataFrame):
    """
    給定單一股票的歷史資料，訓練機器學習模型來預測未來1日的報酬率。
    `train_data` 和 `test_data` 為 pandas DataFrame，包含 OHLCV 及上面定義的技術指標欄位。
    """
    # 計算未來X日的累積報酬率作為預測目標
    train_data['future_1d_return'] = train_data['close'].shift(-1) / train_data['close'] - 1.0
    # 刪除有缺失值的列
    train_data = train_data.dropna()
    # 特徵欄位列表
    features = ['sma_10', 'sma_20', 'rsi_14', 'percent_b', 'ret_1', 'ret_5']
    X_train = train_data[features].values
    y_train = train_data['future_1d_return'].values
    # 初始化並訓練模型
    model = model_cls(**model_params)
    model.fit(X_train, y_train)
    return model
