from zh_maps import metrics_zh_map, trades_zh_map, positions_zh_map, zhwidth
import os
import pandas as pd

def print_metrics_report(metrics_df, model_cls=None, model_params=None):
    csv_path = f"metrics_report_{getattr(model_cls, '__name__', str(model_cls))}.csv"
    metrics_df_zh = metrics_df.copy()
    metrics_df_zh['name'] = metrics_df_zh['name'].map(lambda x: metrics_zh_map.get(x, x))
    col1 = metrics_df_zh['name'].astype(str)
    col2 = metrics_df_zh['value'].astype(str)
    maxlen1 = max(zhwidth(x) for x in col1)
    maxlen2 = max(zhwidth(x) for x in col2)
    print("回測績效指標：")
    for n, v in zip(col1, col2):
        pad1 = maxlen1 - zhwidth(n)
        pad2 = maxlen2 - zhwidth(v)
        print(f"{n}{' '*pad1}  {v}{' '*pad2}")
     # == 準備這次要加入的模型名、參數字串 ==
    param_str = str(model_params) if model_params is not None else ""
    col_title = f"{param_str}"

    # == 把結果準備成dict（指標名: value） ==
    def to_float4(x):
        try:
            f = float(x)
            return f"{f:.4f}"
        except Exception:
            return x
    result_dict = {n: to_float4(v) for n, v in zip(col1, col2)}
    #result_dict = dict(zip(col1, col2))

    # == 處理CSV append (欄位橫向新增) ==
    if os.path.exists(csv_path):
        # 檔案存在，讀舊檔，用pandas合併
        old_df = pd.read_csv(csv_path, index_col=0)
        new_colname = col_title
        # 若同模型參數已存在則自動加序號避免覆蓋
        base_name = new_colname
        idx = 1
        while new_colname in old_df.columns:
            idx += 1
            new_colname = f"{base_name} ({idx})"
        # append 新欄
        merged_df = old_df.copy()
        merged_df[new_colname] = pd.Series(result_dict)
    else:
        # 第一次寫，建立新表
        merged_df = pd.DataFrame({col_title: result_dict})

    # 儲存
    merged_df.to_csv(csv_path, encoding="utf-8-sig")

def print_trades_report(trades_df, head=None):
    trades = trades_df.copy()
    trades_zh = trades.rename(columns=trades_zh_map)
    if head is not None:
        trades_zh = trades_zh.head(head)
    print("\n交易紀錄：")
    col_widths = [
        max([zhwidth(col)] + [zhwidth(val) for val in trades_zh[col]])
        for col in trades_zh.columns
    ]
    header = "  ".join([f"{col}{' ' * (w - zhwidth(col))}" for col, w in zip(trades_zh.columns, col_widths)])
    print(header)
    for idx, row in trades_zh.iterrows():
        print("  ".join([f"{str(row[col])}{' ' * (w - zhwidth(str(row[col])))}" for col, w in zip(trades_zh.columns, col_widths)]))

def print_positions_report(positions_df):
    positions_zh = positions_df.rename(columns=positions_zh_map)
    if not positions_zh.empty:
        print("\n回測結束時現有持股部位：")
        col_widths = [max(zhwidth(col), *(zhwidth(val) for val in positions_zh[col])) for col in positions_zh.columns]
        header = "  ".join([f"{col}{' ' * (w - zhwidth(col))}" for col, w in zip(positions_zh.columns, col_widths)])
        print(header)
        for idx, row in positions_zh.iterrows():
            print("  ".join([f"{str(row[col])}{' ' * (w - zhwidth(str(row[col])))}" for col, w in zip(positions_zh.columns, col_widths)]))
    else:
        print("\n現有持股部位：無持倉")
