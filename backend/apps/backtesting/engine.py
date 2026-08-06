from apps.analysis.services import AnalysisService
from apps.markets.models import Market, MarketPrice

from .history import TradeHistory
from .simulator import TradeSimulator
from .statistics import Statistics


class BacktestEngine:

    def __init__(self):

        self.analysis = AnalysisService()
        self.simulator = TradeSimulator()
        self.statistics = Statistics()

    def run(self, symbol):

        market = Market.objects.get(symbol=symbol)

        candles = list(
            MarketPrice.objects
            .filter(market=market)
            .order_by("datetime")
        )

        history = TradeHistory()

        for index in range(200, len(candles) - 1):

            candle = candles[index]

            analysis = self.analysis.analyse(
                symbol,
                end_date=candle.datetime,
            )

            strategy = analysis["strategy"]

            trade = self.simulator.simulate(
                signal=strategy["signal"],
                entry=strategy["entry"],
                stop_loss=strategy["stop_loss"],
                take_profit=strategy["take_profit"],
                future_candles=candles[index + 1:],
            )

            history.add(trade)

        statistics = self.statistics.calculate(history)

        return {
            "statistics": statistics,
            "history": history,
        }