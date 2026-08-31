from apps.analysis.strategies.base import Strategy


class TrendFollowingStrategy(Strategy):

    name = "trend_following"

    def __init__(
        self,
        stop_loss_atr=1.0,
        take_profit_atr=2.0,
    ):
        self.stop_loss_atr = stop_loss_atr
        self.take_profit_atr = take_profit_atr

    def evaluate(self, observations):

        reasons = []
        confidence = 0

        trend = observations["trend"]["observations"]

        rsi = observations["rsi"]["values"]["rsi"]
        atr = observations["atr"]["values"]["atr"]

        price_action = observations["price_action"]["observations"]

        price = observations["ema"]["values"]["price"]

        bullish_setup = (
            trend["direction"] == "Bullish"
            and trend["bullish_pullback"]
            and price_action["bullish_close"]
            and 55 <= rsi <= 70
        )

        bearish_setup = (
            trend["direction"] == "Bearish"
            and trend["bearish_pullback"]
            and price_action["bearish_close"]
            and 30 <= rsi <= 45
        )

        if bullish_setup:

            signal = "BUY"
            confidence = 80

            reasons.extend([
                "Bullish trend pullback",
                "Strong bullish price action",
                "RSI confirms bullish momentum",
            ])

            if price_action["bullish_reversal"]:
                confidence += 10
                reasons.append("Bullish reversal pattern")

        elif bearish_setup:

            signal = "SELL"
            confidence = 80

            reasons.extend([
                "Bearish trend pullback",
                "Strong bearish price action",
                "RSI confirms bearish momentum",
            ])

            if price_action["bearish_reversal"]:
                confidence += 10
                reasons.append("Bearish reversal pattern")

        else:

            signal = "HOLD"
            confidence = 0
            reasons.append("No complete trading setup")

        entry = None
        stop_loss = None
        take_profit = None

        if signal == "BUY":

            entry = price

            stop_loss = (
                entry
                - atr * self.stop_loss_atr
            )

            take_profit = (
                entry
                + atr * self.take_profit_atr
            )

        elif signal == "SELL":

            entry = price

            stop_loss = (
                entry
                + atr * self.stop_loss_atr
            )

            take_profit = (
                entry
                - atr * self.take_profit_atr
            )

        return {
            "signal": signal,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence,
            "reasons": reasons,
        }