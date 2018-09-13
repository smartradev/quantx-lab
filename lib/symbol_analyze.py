import pandas as pd

def calc(trade_history):
    """
    各種指標値計算処理
    """
    positions = []
    winCount = 0 # 勝数
    sellCount = 0 # 売り回数
    profit = 0 # 利益
    totalProfit = 0 # 累積益
    totalLoss = 0 # 累積損
    maxProfit = 0 # 最大利益
    maxLoss = 0 # 最大損失
    
    if trade_history is None:
        return winCount, sellCount, profit, totalProfit, totalLoss, maxProfit, maxLoss

    for i, row in trade_history.iterrows():
        if row.amount > 0:
            # 買い
            # ポジションに追加して、購入価格順にソートする
            positions.append({
                "amount": row.amount,
                "price": row.price,
            })
            positions = sorted(positions, key=lambda x: x["price"])
        else:
            # 売り
            amount = -row.amount
            while amount > 0:
                # ポジションと相殺する
                p = None
                try:
                    p = positions.pop()
                except:
                    # マイナスになる場合は、株式分割のため。
                    # 現状、株式分割情報が取れないので、
                    # マイナスになった場合、無視して次のデータを処理する。
                    break

                currentAmount = p["amount"]
                amount -= p["amount"]

                if amount < 0:
                    # 引き過ぎた場合、
                    currentAmount -= amount
                    p["amount"] = -amount
                    positions.append(p)

                sellCount += 1
                # 勝数と損益を記録する。
                if p["price"] < row.price:
                    winCount += 1
                    p = p["amount"] * (row.price - p["price"])
                    profit += p
                    totalProfit += p
                    if p > maxProfit:
                        maxProfit = p
                else:
                    l = p["amount"] * (p["price"] - row.price)
                    if l > maxLoss:
                        maxLoss = l
                    profit -= l
                    totalLoss += l

    return winCount, sellCount, profit, totalProfit, totalLoss, maxProfit, maxLoss

def symbol_analyze(backtestResult):
    """
        銘柄毎の各種指標値の計算・DataFrameに加工
    """
    symbols = backtestResult.symbol_summary()
    summary = []
    for symbol in symbols.symbol:
        th = backtestResult.trade_history_by_symbol(symbol)
        winCount, sellCount, profit, totalProfit, totalLoss, maxProfit, maxLoss = calc(th)
        winRatio = 0
        if sellCount != 0:
            winRatio = winCount / sellCount
        profitFactor = 0
        if totalLoss != 0:
            profitFactor = totalProfit / totalLoss
        summary.append([
            symbol, winCount, sellCount, winRatio,
            profit, totalProfit, totalLoss, profitFactor,
            maxProfit, maxLoss])

    summary_df = pd.DataFrame(summary, columns=[
        "symbol", "win_count", "sell_count", "win_ratio", "profit", "total_profit", "total_loss", "profit_factor", "max_profit", "max_loss"])
    summary_df = summary_df.set_index(["symbol"])
    return summary_df
