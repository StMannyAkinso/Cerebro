from apps.backtesting.execution import BacktestExecutor
from apps.backtesting.statistics import Statistics
from apps.markets.models import Market, MarketPrice


class BacktestEngine:

    def __init__(self):

        self.executor = BacktestExecutor()
        self.statistics = Statistics()

    def run(
        self,
        symbol,
        experiment,
        start_date=None,
        end_date=None,
    ):

        market = Market.objects.get(
            symbol=symbol
        )

        queryset = (
            MarketPrice.objects
            .filter(market=market)
            .order_by("datetime")
        )

        if end_date is not None:
            queryset = queryset.filter(
                datetime__lte=end_date
            )

        candles = list(queryset)

        execution = self.executor.execute(
            symbol=symbol,
            experiment=experiment,
            candles=candles,
            start_date=start_date,
        )

        history = execution.get("history")

        if history is None:

            return {
                "experiment": experiment.name,
                "parameters": experiment.parameters,
                "results": execution["results"],
                "trades": execution["trades"],
                "trade_diagnostics": [],
                "statistics": {
                    "trades": 0,
                    "wins": 0,
                    "losses": 0,
                    "open": 0,
                    "win_rate": 0,
                    "average_r": 0,
                    "average_candles": 0,
                },
            }

        statistics = self.statistics.calculate(
            history
        )

        trade_diagnostics = self._build_trade_diagnostics(
            execution["trades"],
            execution["results"],
            candles,
        )

        return {
            "experiment": experiment.name,
            "parameters": experiment.parameters,
            "results": execution["results"],
            "trades": execution["trades"],
            "trade_diagnostics": trade_diagnostics,
            "statistics": statistics,
        }

    # ==========================================================
    # TRADE DIAGNOSTICS
    # ==========================================================

    def _build_trade_diagnostics(
        self,
        trades,
        results,
        candles,
    ):

        diagnostics = []

        for trade in trades:

            entry_date = trade.entry_date
            exit_date = trade.exit_date

            entry_price = float(trade.entry_price)

            stop_loss = float(trade.stop_loss)

            signal = trade.signal

            risk = abs(
                entry_price - stop_loss
            )

            if risk == 0:
                risk = None

            trade_candles = [
                candle
                for candle in candles
                if entry_date <= candle.datetime <= exit_date
            ]

            mfe_price = 0.0
            mae_price = 0.0

            if trade_candles:

                if signal == "BUY":

                    highest_price = max(
                        float(candle.high)
                        for candle in trade_candles
                    )

                    lowest_price = min(
                        float(candle.low)
                        for candle in trade_candles
                    )

                    mfe_price = (
                        highest_price - entry_price
                    )

                    mae_price = (
                        entry_price - lowest_price
                    )

                elif signal == "SELL":

                    lowest_price = min(
                        float(candle.low)
                        for candle in trade_candles
                    )

                    highest_price = max(
                        float(candle.high)
                        for candle in trade_candles
                    )

                    mfe_price = (
                        entry_price - lowest_price
                    )

                    mae_price = (
                        highest_price - entry_price
                    )

            if risk is not None:

                mfe_r = mfe_price / risk
                mae_r = mae_price / risk

            else:

                mfe_r = 0
                mae_r = 0

            setup = self._find_trade_setup(
                entry_date,
                results,
            )

            diagnostics.append({
                "signal": signal,

                "entry_date": entry_date,
                "exit_date": exit_date,

                "entry_price": entry_price,

                "stop_loss": stop_loss,
                "take_profit": float(
                    trade.take_profit
                ),

                "result": trade.result,
                "exit_reason": trade.exit_reason,

                "candles_held": trade.candles_held,
                "r_multiple": trade.r_multiple,

                "mfe_price": round(
                    mfe_price,
                    5,
                ),

                "mae_price": round(
                    mae_price,
                    5,
                ),

                "mfe_r": round(
                    mfe_r,
                    3,
                ),

                "mae_r": round(
                    mae_r,
                    3,
                ),

                "decision": setup,
            })

        return diagnostics

    # ==========================================================
    # FIND THE DECISION THAT CREATED THE TRADE
    # ==========================================================

    def _find_trade_setup(
        self,
        entry_date,
        results,
    ):

        for result in results:

            result_date = (
                result.get("datetime")
                or result.get("date")
                or result.get("timestamp")
            )

            if result_date != entry_date:
                continue

            analysis = result.get(
                "analysis",
                {},
            )

            decision = analysis.get(
                "decision",
                {},
            )

            return {
                "signal": decision.get(
                    "signal"
                ),

                "confidence": decision.get(
                    "confidence"
                ),

                "reasons": decision.get(
                    "reasons",
                    [],
                ),
            }

        return {
            "signal": None,
            "confidence": None,
            "reasons": [],
        }