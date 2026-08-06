class Statistics:

    def calculate(self, history):

        total = len(history.all())

        wins = len(history.wins())

        losses = len(history.losses())

        open_trades = len(history.open())

        closed = len(history.closed())

        win_rate = 0

        if closed:
            win_rate = round(
                (wins / closed) * 100,
                2,
            )

        average_r = 0

        if closed:
            average_r = round(
                sum(
                    trade.r_multiple
                    for trade in history.closed()
                ) / closed,
                2,
            )

        average_candles = 0

        if total:
            average_candles = round(
                sum(
                    trade.candles_held
                    for trade in history.all()
                ) / total,
                2,
            )

        return {
            "trades": total,
            "wins": wins,
            "losses": losses,
            "open": open_trades,
            "win_rate": win_rate,
            "average_r": average_r,
            "average_candles": average_candles,
        }