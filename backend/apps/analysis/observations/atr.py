from ta.volatility import AverageTrueRange

from .base import Observation


class ATRObservation(Observation):

    name = "atr"

    def calculate(self, df):

        atr = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=14,
        ).average_true_range().iloc[-1]

        return {
            "values": {
                "atr14": round(float(atr), 5),
            },
            "observations": {},
        }