from .base import Observation


class TrendObservation(Observation):

    name = "trend"

    def calculate(self, observations):

        ema = observations["ema"]
        rsi = observations["rsi"]

        ema_obs = ema["observations"]
        rsi_value = rsi["values"]["rsi14"]

        if (
            ema_obs["price_above_ema20"]
            and ema_obs["price_above_ema50"]
            and ema_obs["price_above_ema200"]
            and rsi_value > 55
        ):
            direction = "Bullish"

        elif (
            not ema_obs["price_above_ema20"]
            and not ema_obs["price_above_ema50"]
            and not ema_obs["price_above_ema200"]
            and rsi_value < 45
        ):
            direction = "Bearish"

        else:
            direction = "Neutral"

        return {
            "metrics": {},
            "observations": {
                "direction": direction,
            },
        }