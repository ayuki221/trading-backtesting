import unicodedata

metrics_zh_map = {
    "trade_count": "交易次數",
    "initial_market_value": "初始資金",
    "end_market_value": "結束資產",
    "total_pnl": "總損益",
    "unrealized_pnl": "未實現損益",
    "total_return_pct": "總報酬率 (%)",
    "total_profit": "總獲利",
    "total_loss": "總虧損",
    "total_fees": "手續費總額",
    "max_drawdown": "最大回撤金額",
    "max_drawdown_pct": "最大回撤 (%)",
    "max_drawdown_date": "最大回撤發生日",
    "win_rate": "勝率",
    "loss_rate": "虧損率",
    "winning_trades": "獲利單數",
    "losing_trades": "虧損單數",
    "avg_pnl": "平均單筆損益",
    "avg_return_pct": "平均單筆報酬率 (%)",
    "avg_trade_bars": "平均持有天數",
    "avg_profit": "平均獲利",
    "avg_profit_pct": "平均獲利報酬率 (%)",
    "avg_winning_trade_bars": "平均獲利單持有天數",
    "avg_loss": "平均虧損",
    "avg_loss_pct": "平均虧損報酬率 (%)",
    "avg_losing_trade_bars": "平均虧損單持有天數",
    "largest_win": "單筆最大獲利",
    "largest_win_pct": "單筆最大獲利報酬率 (%)",
    "largest_win_bars": "最大獲利持有天數",
    "largest_loss": "單筆最大虧損",
    "largest_loss_pct": "單筆最大虧損報酬率 (%)",
    "largest_loss_bars": "最大虧損持有天數",
    "max_wins": "連續獲利次數",
    "max_losses": "連續虧損次數",
    "sharpe": "夏普比率",
    "sortino": "Sortino比率",
    "profit_factor": "盈虧比",
    "ulcer_index": "Ulcer指標",
    "upi": "Ulcer績效指標(UPI)",
    "equity_r2": "資產R平方值",
    "std_error": "標準誤差"
}

trades_zh_map = {
    "type": "方向",
    "symbol": "股票",
    "entry_date": "進場日",
    "exit_date": "出場日",
    "entry": "進場價",
    "exit": "出場價",
    "shares": "股數",
    "pnl": "損益",
    "return_pct": "報酬率%",
    "agg_pnl": "累積損益",
    "bars": "持有天數",
    "pnl_per_bar": "單日損益",
    "stop": "停損",
    "mae": "最大不利MAE",
    "mfe": "最大有利MFE"
}

positions_zh_map = {
    "symbol": "股票",
    "long_shares": "多頭股數",
    "short_shares":"空頭股數",
    "avg_entry": "平均成本",
    "market_value": "市值",
    "pnl": "損益",
    "unrealized_pnl": "未實現損益",
    "close":"收盤價",
    "equity":"總權益",
    "margin":"保證金需求",
}

def zhwidth(text):
    width = 0
    for ch in str(text):
        if unicodedata.east_asian_width(ch) in ['F', 'W', 'A']:
            width += 2
        else:
            width += 1
    return width
