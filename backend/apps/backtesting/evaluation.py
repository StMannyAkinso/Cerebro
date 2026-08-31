class ResearchEvaluator:

    def evaluate(self, backtest):

        statistics = backtest["statistics"]
        results = backtest["results"]

        trades = [
            result["simulation"]
            for result in results
            if result["simulation"] is not None
        ]

        closed_trades = [
            trade
            for trade in trades
            if trade.result != "OPEN"
        ]

        total_r = round(
            sum(
                trade.r_multiple
                for trade in closed_trades
            ),
            2,
        )

        profit_factor = self._profit_factor(
            closed_trades
        )

        max_drawdown = self._max_drawdown(
            closed_trades
        )

        return {
            "trades": statistics["trades"],
            "wins": statistics["wins"],
            "losses": statistics["losses"],
            "open": statistics["open"],
            "win_rate": statistics["win_rate"],
            "average_r": statistics["average_r"],
            "total_r": total_r,
            "profit_factor": profit_factor,
            "max_drawdown_r": max_drawdown,
            "average_candles": statistics["average_candles"],
        }

    def _profit_factor(self, trades):

        gross_profit = sum(
            trade.r_multiple
            for trade in trades
            if trade.r_multiple > 0
        )

        gross_loss = abs(
            sum(
                trade.r_multiple
                for trade in trades
                if trade.r_multiple < 0
            )
        )

        if gross_loss == 0:

            if gross_profit > 0:
                return float("inf")

            return 0

        return round(
            gross_profit / gross_loss,
            2,
        )

    def _max_drawdown(self, trades):

        equity = 0
        peak = 0
        max_drawdown = 0

        for trade in trades:

            equity += trade.r_multiple

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return round(max_drawdown, 2)