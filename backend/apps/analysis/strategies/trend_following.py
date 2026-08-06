from .base import Strategy


class TrendFollowingStrategy(Strategy):

    name = "trend_following"

    def evaluate(self, observations):

        reasons = []
        confidence = 0

        ema_values = observations["ema"]["values"]
        ema = observations["ema"]["observations"]

        rsi = observations["rsi"]["values"]["rsi14"]
        atr = observations["atr"]["values"]["atr14"]

        trend = observations["trend"]["observations"]["direction"]

        price = ema_values["price"]

        if trend == "Bullish":
            confidence += 40
            reasons.append("Bullish trend")

        if ema["price_above_ema20"]:
            confidence += 10
            reasons.append("Price above EMA20")

        if ema["price_above_ema50"]:
            confidence += 10
            reasons.append("Price above EMA50")

        if ema["price_above_ema200"]:
            confidence += 20
            reasons.append("Price above EMA200")

        if 55 <= rsi <= 70:
            confidence += 20
            reasons.append("Healthy RSI")

        if confidence >= 70:
            signal = "BUY"
        elif confidence <= 30:
            signal = "SELL"
        else:
            signal = "HOLD"

        entry = None
        stop_loss = None
        take_profit = None

        if signal == "BUY":

            entry = round(price, 5)

            stop_loss = round(price - (atr * 1.5), 5)

            risk = entry - stop_loss

            take_profit = round(entry + (risk * 2), 5)

        elif signal == "SELL":

            entry = round(price, 5)

            stop_loss = round(price + (atr * 1.5), 5)

            risk = stop_loss - entry

            take_profit = round(entry - (risk * 2), 5)

        return {
            "signal": signal,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "confidence": confidence,
            "reasons": reasons,
        }