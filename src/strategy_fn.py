def exec_fn(ctx):
    """
    交易決策函數：
    - 若目前沒有持有該股票，且模型對該股票預測未來1日報酬率為正，則產生買入信號。
    - 若目前持有該股票，且模型預測未來1日報酬率轉為負，則產生賣出信號。
    - ctx.score 設定用於在多檔買入信號時進行排序，只執行預測分數最高的股票（基於 max_long_positions 限制）。
    """
    # 取得模型對該股票的預測結果數列（ctx.preds('ml_model') 返回該模型對此股票歷史每一bar的預測值陣列）
    preds = ctx.preds('ml_model')
    # 取得最新一筆（當前 bar）的預測值
    latest_pred = preds[-1] if len(preds) > 0 else None
    if latest_pred is None:
        return  # 尚無預測值（可能在 warmup 初期），不進行任何交易動作
    if not ctx.long_pos():
        # 沒有持倉的情況下，如果預測未來報酬率為正，則準備買入
        if latest_pred > 0:
            # 設定購買股數（此處先設為滿倉，實際將透過排名機制與倉位上限確定最終執行）
            ctx.buy_shares = ctx.calc_target_shares(1.0)
            # 設定該買入信號的排序分數為預測的報酬率，PyBroker 將依此分數在允許的持倉數內挑選最高者執行
            ctx.score = float(latest_pred)
    else:
        # 如果目前已持有該股票，且模型最新預測的未來報酬率為負值，則賣出清倉
        if latest_pred < 0:
            ctx.sell_all_shares()