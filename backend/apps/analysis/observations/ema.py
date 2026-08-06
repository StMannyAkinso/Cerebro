from ta.trend import EMAIndicator

from .base import Observation


class EMAObservation(Observation):

    name = "ema"

    def calculate(self, df):

        close = df["close"]

        ema20 = EMAIndicator(close, window=20).ema_indicator().iloc[-1]
        ema50 = EMAIndicator(close, window=50).ema_indicator().iloc[-1]
        ema200 = EMAIndicator(close, window=200).ema_indicator().iloc[-1]

        price = close.iloc[-1]

        return {
            "values": {
                "price": round(float(price), 5),
                "ema20": round(float(ema20), 5),
                "ema50": round(float(ema50), 5),
                "ema200": round(float(ema200), 5),
            },
            "observations": {
                "price_above_ema20": bool(price > ema20),
                "price_above_ema50": bool(price > ema50),
                "price_above_ema200": bool(price > ema200),
            },
        }