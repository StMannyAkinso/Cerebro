from ta.trend import EMAIndicator

from .base import Observation


class EMAObservation(Observation):

    name = "ema"

    def __init__(
        self,
        fast_window=20,
        mid_window=50,
        slow_window=200,
    ):

        self.fast_window = fast_window
        self.mid_window = mid_window
        self.slow_window = slow_window

    def calculate(self, df):

        close = df["close"]

        ema_fast = EMAIndicator(
            close,
            window=self.fast_window,
        ).ema_indicator().iloc[-1]

        ema_mid = EMAIndicator(
            close,
            window=self.mid_window,
        ).ema_indicator().iloc[-1]

        ema_slow = EMAIndicator(
            close,
            window=self.slow_window,
        ).ema_indicator().iloc[-1]

        price = close.iloc[-1]

        return {
            "values": {
                "price": round(float(price), 5),
                "ema_fast": round(float(ema_fast), 5),
                "ema_mid": round(float(ema_mid), 5),
                "ema_slow": round(float(ema_slow), 5),
            },

            "observations": {
                "price_above_ema_fast": bool(price > ema_fast),
                "price_above_ema_mid": bool(price > ema_mid),
                "price_above_ema_slow": bool(price > ema_slow),
            },
        }