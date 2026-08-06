import pandas as pd

from apps.markets.models import Market, MarketPrice

from .observations.ema import EMAObservation
from .observations.rsi import RSIObservation
from .observations.atr import ATRObservation
from .observations.trend import TrendObservation

from .strategies.trend_following import TrendFollowingStrategy


class AnalysisService:

    def __init__(self):

        self.observations = [
            EMAObservation(),
            RSIObservation(),
            ATRObservation(),
        ]

        self.trend = TrendObservation()

        self.strategy = TrendFollowingStrategy()

    def analyse(self, symbol, end_date=None):

        market = Market.objects.get(symbol=symbol)

        prices = MarketPrice.objects.filter(
            market=market
        )

        if end_date:
            prices = prices.filter(
                datetime__lte=end_date
            )

        prices = (
            prices
            .order_by("datetime")
            .values(
                "datetime",
                "open",
                "high",
                "low",
                "close",
                "volume",
            )
        )

        df = pd.DataFrame(prices)

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        df[numeric_columns] = df[numeric_columns].astype(float)

        observations = {}

        # Primitive observations
        for observation in self.observations:
            observations[observation.name] = observation.calculate(df)

        # Derived observation
        observations[self.trend.name] = self.trend.calculate(observations)

        # Strategy
        strategy = self.strategy.evaluate(observations)

        return {
            "observations": observations,
            "strategy": strategy,
        }