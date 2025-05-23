import os
import pandas as pd
import yfinance as yf

def load_or_download_yf_data(ticker, start, end, folder="../data_cache"):
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{ticker}_{start}_{end}.csv")
    if os.path.exists(file_path):
        print(f"載入本地快取：{file_path}")
        df = pd.read_csv(file_path, parse_dates=['Date'])
        for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"從yfinance下載：{ticker}")
        df = yf.download(ticker, start=start, end=end)
        if df.empty:
            raise ValueError(f"無法取得 {ticker} 的歷史資料")
        df.reset_index(inplace=True)
        df.to_csv(file_path, index=False)
    # 重新命名欄位以符合PyBroker格式
    df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
        "Adj Close": "adj_close"
    }, inplace=True)
    df['symbol'] = ticker
    return df
