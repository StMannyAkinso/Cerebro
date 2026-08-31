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

        direction = trend["direction"]

        bullish_pullback = trend.get(
            "bullish_pullback",
            False,
        )

        bearish_pullback = trend.get(
            "bearish_pullback",
            False,
        )

        bullish_close = price_action.get(
            "bullish_close",
            False,
        )

        bearish_close = price_action.get(
            "bearish_close",
            False,
        )

        bullish_reversal = price_action.get(
            "bullish_reversal",
            False,
        )

        bearish_reversal = price_action.get(
            "bearish_reversal",
            False,
        )

        bullish_candle = price_action.get(
            "bullish_candle",
            False,
        )

        bearish_candle = price_action.get(
            "bearish_candle",
            False,
        )

        # --------------------------------------------------
        # BULLISH SETUP
        # --------------------------------------------------

        if direction == "Bullish" and bullish_pullback:

            confidence += 40
            reasons.append("Bullish trend pullback")

            if bullish_close:
                confidence += 20
                reasons.append("Strong bullish close")

            elif bullish_candle:
                confidence += 10
                reasons.append("Bullish candle")

            if bullish_reversal:
                confidence += 15
                reasons.append("Bullish reversal pattern")

            if 55 <= rsi <= 70:
                confidence += 20
                reasons.append("RSI confirms bullish momentum")

            elif 50 <= rsi < 55:
                confidence += 10
                reasons.append("RSI supports bullish momentum")

            if confidence >= 70:
                signal = "BUY"

            else:
                signal = "HOLD"

        # --------------------------------------------------
        # BEARISH SETUP
        # --------------------------------------------------

        elif direction == "Bearish" and bearish_pullback:

            confidence += 40
            reasons.append("Bearish trend pullback")

            if bearish_close:
                confidence += 20
                reasons.append("Strong bearish close")

            elif bearish_candle:
                confidence += 10
                reasons.append("Bearish candle")

            if bearish_reversal:
                confidence += 15
                reasons.append("Bearish reversal pattern")

            if 30 <= rsi <= 45:
                confidence += 20
                reasons.append("RSI confirms bearish momentum")

            elif 45 < rsi <= 50:
                confidence += 10
                reasons.append("RSI supports bearish momentum")

            if confidence >= 70:
                signal = "SELL"

            else:
                signal = "HOLD"

        # --------------------------------------------------
        # NO SETUP
        # --------------------------------------------------

        else:

            signal = "HOLD"
            confidence = 0
            reasons.append("No complete trading setup")

        # --------------------------------------------------
        # RISK MANAGEMENT
        # --------------------------------------------------

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