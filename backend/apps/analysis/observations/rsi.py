from ta.momentum import RSIIndicator

from .base import Observation


class RSIObservation(Observation):

    name = "rsi"

    def calculate(self, df):

        rsi = RSIIndicator(
            close=df["close"],
            window=14,
        ).rsi().iloc[-1]

        return {
            "values": {
                "rsi14": round(float(rsi), 5),
            },
            "observations": {
                "overbought": bool(rsi > 70),
                "oversold": bool(rsi < 30),
            },
        }