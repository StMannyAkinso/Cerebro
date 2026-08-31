from .base import Observation


class TrendObservation(Observation):

    name = "trend"

    def calculate(self, observations):

        ema = observations["ema"]

        values = ema["values"]
        ema_observations = ema["observations"]

        price = values["price"]
        ema_fast = values["ema_fast"]
        ema_mid = values["ema_mid"]
        ema_slow = values["ema_slow"]

        above_fast = ema_observations["price_above_ema_fast"]
        above_mid = ema_observations["price_above_ema_mid"]
        above_slow = ema_observations["price_above_ema_slow"]

        bullish_structure = (
            ema_fast > ema_mid > ema_slow
        )

        bearish_structure = (
            ema_fast < ema_mid < ema_slow
        )

        if bullish_structure:
            direction = "Bullish"

        elif bearish_structure:
            direction = "Bearish"

        else:
            direction = "Neutral"

        bullish_pullback = (
            bullish_structure
            and not above_fast
            and above_mid
            and above_slow
        )

        bearish_pullback = (
            bearish_structure
            and above_fast
            and not above_mid
            and not above_slow
        )

        pullback = (
            bullish_pullback
            or bearish_pullback
        )

        return {
            "metrics": {
                "price": round(float(price), 5),
                "ema_fast": round(float(ema_fast), 5),
                "ema_mid": round(float(ema_mid), 5),
                "ema_slow": round(float(ema_slow), 5),
            },

            "observations": {
                "direction": direction,
                "structure_aligned": (
                    bullish_structure
                    or bearish_structure
                ),
                "pullback": pullback,
                "bullish_pullback": bullish_pullback,
                "bearish_pullback": bearish_pullback,
            },
        }