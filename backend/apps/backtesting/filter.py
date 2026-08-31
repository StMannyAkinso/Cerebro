class ResearchFilter:

    def __init__(
        self,
        minimum_trades=100,
        minimum_average_r=0,
        minimum_profit_factor=1,
    ):

        self.minimum_trades = minimum_trades
        self.minimum_average_r = minimum_average_r
        self.minimum_profit_factor = minimum_profit_factor

    def evaluate(self, evaluation):

        reasons = []

        if evaluation["trades"] < self.minimum_trades:

            reasons.append(
                f"Too few trades: "
                f"{evaluation['trades']} "
                f"< {self.minimum_trades}"
            )

        if evaluation["average_r"] <= self.minimum_average_r:

            reasons.append(
                f"Average R too low: "
                f"{evaluation['average_r']} "
                f"<= {self.minimum_average_r}"
            )

        if evaluation["profit_factor"] <= self.minimum_profit_factor:

            reasons.append(
                f"Profit factor too low: "
                f"{evaluation['profit_factor']} "
                f"<= {self.minimum_profit_factor}"
            )

        return {
            "passes": len(reasons) == 0,
            "reasons": reasons,
        }