def pos_size_handler(ctx):
    signals = list(ctx.signals())
    max_frac = 1 / 3  # 單檔最多佔總資金1/3
    for signal in signals:
        price = signal.bar_data.close[-1]
        shares = ctx.calc_target_shares(max_frac, price)
        ctx.set_shares(signal, shares)
