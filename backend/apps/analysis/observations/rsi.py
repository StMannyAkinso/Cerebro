from ta.momentum import RSIIndicator

from .base import Observation


class RSIObservation(Observation):

    name = "rsi"

    def __init__(self, window=14):

        self.window = window

    def calculate(self, df):

        close = df["close"]

        rsi = RSIIndicator(
            close,
            window=self.window,
        ).rsi().iloc[-1]

        return {
            "values": {
                "rsi": round(float(rsi), 5),
            },

            "observations": {
                "overbought": bool(rsi >= 70),
                "oversold": bool(rsi <= 30),
            },
        }