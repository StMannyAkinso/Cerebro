class TradeHistory:

    def __init__(self):

        self.trades = []

    def add(self, trade):

        if trade is not None:
            self.trades.append(trade)

    def all(self):

        return self.trades

    def closed(self):

        return [
            trade
            for trade in self.trades
            if trade.result != "OPEN"
        ]

    def open(self):

        return [
            trade
            for trade in self.trades
            if trade.result == "OPEN"
        ]

    def wins(self):

        return [
            trade
            for trade in self.trades
            if trade.result == "WIN"
        ]

    def losses(self):

        return [
            trade
            for trade in self.trades
            if trade.result == "LOSS"
        ]
