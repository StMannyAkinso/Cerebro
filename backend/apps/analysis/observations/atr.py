from ta.volatility import AverageTrueRange

from .base import Observation


class ATRObservation(Observation):

    name = "atr"

    def __init__(self, window=14):

        self.window = window

    def calculate(self, df):

        atr = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=self.window,
        ).average_true_range().iloc[-1]

        return {
            "values": {
                "atr": round(float(atr), 5),
            },

            "observations": {},
        }