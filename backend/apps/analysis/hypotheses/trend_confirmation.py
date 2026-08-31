from .base import Hypothesis


class TrendConfirmationHypothesis(Hypothesis):

    name = "trend_confirmation"

    def __init__(
        self,
        bullish_rsi_min=55,
        bullish_rsi_max=70,
        bearish_rsi_min=30,
        bearish_rsi_max=45,
    ):

        self.bullish_rsi_min = bullish_rsi_min
        self.bullish_rsi_max = bullish_rsi_max

        self.bearish_rsi_min = bearish_rsi_min
        self.bearish_rsi_max = bearish_rsi_max

    def evaluate(self, observations):

        trend = observations["trend"]["observations"]["direction"]
        rsi = observations["rsi"]["values"]["rsi"]

        reasons = []

        if trend == "Bullish":

            reasons.append("Bullish trend structure")

            if self.bullish_rsi_min <= rsi <= self.bullish_rsi_max:

                return {
                    "direction": "Bullish",
                    "confirmed": True,
                    "confidence": 80,
                    "reasons": reasons + [
                        "RSI confirms bullish momentum"
                    ],
                }

            return {
                "direction": "Bullish",
                "confirmed": False,
                "confidence": 0,
                "reasons": [
                    "Bullish trend without RSI confirmation"
                ],
            }

        if trend == "Bearish":

            reasons.append("Bearish trend structure")

            if self.bearish_rsi_min <= rsi <= self.bearish_rsi_max:

                return {
                    "direction": "Bearish",
                    "confirmed": True,
                    "confidence": 80,
                    "reasons": reasons + [
                        "RSI confirms bearish momentum"
                    ],
                }

            return {
                "direction": "Bearish",
                "confirmed": False,
                "confidence": 0,
                "reasons": [
                    "Bearish trend without RSI confirmation"
                ],
            }

        return {
            "direction": "Neutral",
            "confirmed": False,
            "confidence": 0,
            "reasons": [
                "No confirmed trend"
            ],
        }