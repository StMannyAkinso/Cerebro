from apps.analysis.observations.base import Observation


class MomentumObservation(Observation):

    name = "momentum"

    def __init__(self, window=14):
        self.window = window

    def calculate(self, df):

        current_price = float(df["close"].iloc[-1])

        if len(df) <= self.window:
            return {
                "values": {
                    "price": current_price,
                    "momentum": None,
                },
                "observations": {
                    "positive": False,
                    "negative": False,
                },
            }

        previous_price = float(
            df["close"].iloc[-1 - self.window]
        )

        momentum = (
            (current_price / previous_price) - 1
        )

        return {
            "values": {
                "price": current_price,
                "momentum": round(momentum, 5),
            },
            "observations": {
                "positive": momentum > 0,
                "negative": momentum < 0,
            },
        }