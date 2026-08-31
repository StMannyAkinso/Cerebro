from apps.analysis.services import AnalysisService
from apps.backtesting.simulator import TradeSimulator
from apps.backtesting.history import TradeHistory


class BacktestExecutor:

    def __init__(self):
        self.analysis = AnalysisService()
        self.simulator = TradeSimulator()

    def execute(
        self,
        symbol,
        experiment,
        candles,
        start_date=None,
    ):
        history = TradeHistory()
        results = []
        trades = []
        trade_diagnostics = []

        if len(candles) <= 200:
            return {
                "results": results,
                "trades": trades,
                "trade_diagnostics": trade_diagnostics,
                "history": history,
            }

        index = 200

        while index < len(candles) - 1:

            candle = candles[index]

            # Historical warmup period.
            #
            # Indicators need historical candles,
            # but trades must not be generated before
            # start_date.
            if (
                start_date is not None
                and candle.datetime < start_date
            ):
                index += 1
                continue

            analysis = self.analysis.analyse(
                symbol,
                experiment,
                end_date=candle.datetime,
            )

            strategy = analysis["strategy"]

            simulation = None

            if (
                strategy["signal"] in ("BUY", "SELL")
                and strategy["entry"] is not None
                and strategy["stop_loss"] is not None
                and strategy["take_profit"] is not None
            ):

                simulation = self.simulator.simulate(
                    signal=strategy["signal"],
                    entry=strategy["entry"],
                    stop_loss=strategy["stop_loss"],
                    take_profit=strategy["take_profit"],
                    future_candles=candles[index + 1:],
                )

                history.add(simulation)
                trades.append(simulation)

                # -------------------------------------------------
                # TRADE DIAGNOSTICS
                #
                # Preserve the decision that created the trade.
                # This is what we eventually want to show to a
                # human trader.
                # -------------------------------------------------

                decision = analysis.get("decision", {})

                trade_diagnostics.append({
                    "signal": simulation.signal,
                    "entry_date": simulation.entry_date,
                    "exit_date": simulation.exit_date,
                    "entry_price": simulation.entry_price,
                    "exit_price": simulation.exit_price,
                    "stop_loss": simulation.stop_loss,
                    "take_profit": simulation.take_profit,
                    "result": simulation.result,
                    "exit_reason": simulation.exit_reason,
                    "candles_held": simulation.candles_held,
                    "r_multiple": simulation.r_multiple,

                    # Decision information.
                    "decision": decision,

                    # Useful flattened fields.
                    "confidence": decision.get("confidence"),
                    "reasons": decision.get("reasons", []),
                })

                results.append({
                    "date": candle.datetime,
                    "experiment": experiment.name,
                    "analysis": analysis,
                    "simulation": simulation,
                })

                # -------------------------------------------------
                # POSITION MANAGEMENT
                #
                # Do not search for another trade while this
                # position is still active.
                # -------------------------------------------------

                if simulation.exit_date is None:

                    # Trade remained open until the end of
                    # available data.
                    break

                exit_index = None

                for future_index in range(
                    index + 1,
                    len(candles),
                ):
                    if (
                        candles[future_index].datetime
                        == simulation.exit_date
                    ):
                        exit_index = future_index
                        break

                if exit_index is None:

                    # Safety fallback.
                    index += 1

                else:

                    # Resume searching after the previous
                    # position has closed.
                    index = exit_index + 1

                continue

            # -----------------------------------------------------
            # NO TRADE ON THIS CANDLE
            # -----------------------------------------------------

            results.append({
                "date": candle.datetime,
                "experiment": experiment.name,
                "analysis": analysis,
                "simulation": None,
            })

            index += 1

        return {
            "results": results,
            "trades": trades,
            "trade_diagnostics": trade_diagnostics,
            "history": history,
        }