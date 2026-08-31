from apps.analysis.strategies.base import Strategy


class MomentumStrategy(Strategy):

    name = "momentum"

    def __init__(
        self,
        stop_loss_atr=1.0,
        take_profit_atr=2.0,
    ):

        self.stop_loss_atr = stop_loss_atr
        self.take_profit_atr = take_profit_atr

    def evaluate(self, observations):

        momentum = observations["momentum"]["observations"]
        price = observations["momentum"]["values"]["price"]
        atr = observations["atr"]["values"]["atr"]

        reasons = []
        confidence = 0

        if momentum["positive"]:
            signal = "BUY"
            confidence = 70
            reasons.append("Positive momentum")

        elif momentum["negative"]:
            signal = "SELL"
            confidence = 70
            reasons.append("Negative momentum")

        else:
            signal = "HOLD"
            confidence = 0
            reasons.append("No clear momentum")

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