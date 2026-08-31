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

        if len(candles) <= 200:
            return {
                "results": results,
                "trades": trades,
                "statistics": None,
            }

        index = 200

        while index < len(candles) - 1:

            candle = candles[index]

            # Historical warmup period.
            #
            # Indicators need historical candles, but trades
            # must not be generated before start_date.
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
                    # the available data.
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

            # No trade on this candle.

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
            "history": history,
        }