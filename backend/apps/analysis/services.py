import pandas as pd

from apps.markets.models import Market, MarketPrice

from .experiments.base import Experiment


class AnalysisService:

    def analyse(self, symbol, experiment, end_date=None):

        if not isinstance(experiment, Experiment):
            raise TypeError(
                "experiment must be an instance of Experiment"
            )

        market = Market.objects.get(symbol=symbol)

        price_query = (
            MarketPrice.objects
            .filter(market=market)
        )

        if end_date is not None:
            price_query = price_query.filter(
                datetime__lte=end_date
            )

        prices = (
            price_query
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

        if df.empty:
            raise ValueError(
                f"No market data available for {symbol}"
                f"{f' at or before {end_date}' if end_date else ''}"
            )

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        df[numeric_columns] = df[numeric_columns].astype(float)

        observations = {}

        # First pass:
        # Calculate observations directly from market data.
        for observation in experiment.build_observations():

            observations[observation.name] = observation.calculate(df)

        # Second pass:
        # Calculate observations that depend on other observations.
        for observation in experiment.build_derived_observations():

            observations[observation.name] = observation.calculate(
                observations
            )

        # Strategy
        strategy = experiment.build_strategy()

        strategy_result = strategy.evaluate(observations)

        return {
            "experiment": experiment.name,
            "observations": observations,
            "strategy": strategy_result,
        }