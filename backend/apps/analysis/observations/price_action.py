from .base import Observation


class PriceActionObservation(Observation):

    name = "price_action"

    def calculate(self, df):

        if len(df) < 2:
            return {
                "values": {},
                "observations": {
                    "bullish_reversal": False,
                    "bearish_reversal": False,
                    "bullish_close": False,
                    "bearish_close": False,
                },
            }

        previous = df.iloc[-2]
        current = df.iloc[-1]

        previous_bearish = previous["close"] < previous["open"]
        previous_bullish = previous["close"] > previous["open"]

        current_bullish = current["close"] > current["open"]
        current_bearish = current["close"] < current["open"]

        bullish_engulfing = (
            previous_bearish
            and current_bullish
            and current["open"] <= previous["close"]
            and current["close"] >= previous["open"]
        )

        bearish_engulfing = (
            previous_bullish
            and current_bearish
            and current["open"] >= previous["close"]
            and current["close"] <= previous["open"]
        )

        current_range = current["high"] - current["low"]

        if current_range > 0:

            close_position = (
                current["close"] - current["low"]
            ) / current_range

        else:
            close_position = 0.5

        bullish_close = close_position >= 0.70
        bearish_close = close_position <= 0.30

        return {
            "values": {
                "previous_open": round(float(previous["open"]), 5),
                "previous_close": round(float(previous["close"]), 5),
                "current_open": round(float(current["open"]), 5),
                "current_high": round(float(current["high"]), 5),
                "current_low": round(float(current["low"]), 5),
                "current_close": round(float(current["close"]), 5),
                "close_position": round(float(close_position), 3),
            },
            "observations": {
                "bullish_reversal": bool(bullish_engulfing),
                "bearish_reversal": bool(bearish_engulfing),
                "bullish_close": bool(bullish_close),
                "bearish_close": bool(bearish_close),
            },
        }