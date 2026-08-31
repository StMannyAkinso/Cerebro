class TradingDecision:

    def __init__(self, strategy_result):
        self.strategy_result = strategy_result

    def build(self):
        result = self.strategy_result

        signal = result["signal"]
        confidence = result["confidence"]
        entry = result["entry"]
        stop_loss = result["stop_loss"]
        take_profit = result["take_profit"]
        reasons = result["reasons"]

        if signal == "BUY":
            action = "LONG"

        elif signal == "SELL":
            action = "SHORT"

        else:
            action = "WAIT"

        return {
            "signal": signal,
            "action": action,
            "confidence": confidence,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "reasons": reasons,
        }