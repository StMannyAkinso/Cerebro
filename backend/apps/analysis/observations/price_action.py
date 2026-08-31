from .base import Observation


class PriceActionObservation(Observation):

    name = "price_action"

    def calculate(self, df):

        previous = df.iloc[-2]
        current = df.iloc[-1]

        previous_open = float(previous["open"])
        previous_close = float(previous["close"])

        current_open = float(current["open"])
        current_high = float(current["high"])
        current_low = float(current["low"])
        current_close = float(current["close"])

        current_range = current_high - current_low

        if current_range > 0:
            close_position = (
                current_close - current_low
            ) / current_range
        else:
            close_position = 0.5

        bullish_candle = current_close > current_open
        bearish_candle = current_close < current_open

        bullish_reversal = (
            previous_close < previous_open
            and current_close > current_open
            and current_close > previous_open
        )

        bearish_reversal = (
            previous_close > previous_open
            and current_close < current_open
            and current_close < previous_open
        )

        bullish_close = close_position >= 0.65
        bearish_close = close_position <= 0.35

        return {
            "values": {
                "previous_open": round(previous_open, 5),
                "previous_close": round(previous_close, 5),
                "current_open": round(current_open, 5),
                "current_high": round(current_high, 5),
                "current_low": round(current_low, 5),
                "current_close": round(current_close, 5),
                "close_position": round(close_position, 5),
            },

            "observations": {
                "bullish_reversal": bullish_reversal,
                "bearish_reversal": bearish_reversal,
                "bullish_candle": bullish_candle,
                "bearish_candle": bearish_candle,
                "bullish_close": bullish_close,
                "bearish_close": bearish_close,
            },
        }