from apps.analysis.decision import TradingDecision
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

        results = execution["results"]

        for result in results:

            strategy_result = (
                result["analysis"]["strategy"]
            )

            result["analysis"]["decision"] = (
                TradingDecision(
                    strategy_result
                ).build()
            )

        history = execution.get("history")

        if history is None:

            return {
                "experiment": experiment.name,
                "parameters": experiment.parameters,
                "results": results,
                "trades": execution["trades"],
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

        return {
            "experiment": experiment.name,
            "parameters": experiment.parameters,
            "results": results,
            "trades": execution["trades"],
            "statistics": statistics,
        }