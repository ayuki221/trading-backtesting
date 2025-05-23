import pandas as pd
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor

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

model_cls = RandomForestRegressor

model_params = MODEL_PARAM_TABLE[model_cls]

def train_ml_model(symbol: str, train_data: pd.DataFrame, test_data: pd.DataFrame):
    # 計算未來X日的累積報酬率作為預測目標
    train_data['future_1d_return'] = train_data['close'].shift(-1) / train_data['close'] - 1.0
    train_data = train_data.dropna()

    features = ['sma_10', 'sma_20', 'rsi_14', 'percent_b', 'ret_1', 'ret_5']
    X_train = train_data[features].values
    y_train = train_data['future_1d_return'].values

    model = model_cls(**model_params)
    model.fit(X_train, y_train)
    return model
