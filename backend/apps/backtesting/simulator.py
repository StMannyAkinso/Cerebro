from .trade import TradeResult


class TradeSimulator:

    def simulate(
        self,
        signal,
        entry,
        stop_loss,
        take_profit,
        future_candles,
    ):

        if signal == "HOLD":
            return None

        for index, candle in enumerate(future_candles):

            high = float(candle.high)
            low = float(candle.low)

            if signal == "BUY":

                # Conservative: if both are hit in the same candle,
                # assume Stop Loss was hit first.
                if low <= stop_loss:
                    return TradeResult(
                        signal=signal,
                        entry_date=future_candles[0].datetime,
                        exit_date=candle.datetime,
                        entry_price=entry,
                        exit_price=stop_loss,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        result="LOSS",
                        exit_reason="STOP_LOSS",
                        candles_held=index + 1,
                        r_multiple=-1.0,
                    )

                if high >= take_profit:
                    return TradeResult(
                        signal=signal,
                        entry_date=future_candles[0].datetime,
                        exit_date=candle.datetime,
                        entry_price=entry,
                        exit_price=take_profit,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        result="WIN",
                        exit_reason="TAKE_PROFIT",
                        candles_held=index + 1,
                        r_multiple=2.0,
                    )

            elif signal == "SELL":

                # Conservative: if both are hit in the same candle,
                # assume Stop Loss was hit first.
                if high >= stop_loss:
                    return TradeResult(
                        signal=signal,
                        entry_date=future_candles[0].datetime,
                        exit_date=candle.datetime,
                        entry_price=entry,
                        exit_price=stop_loss,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        result="LOSS",
                        exit_reason="STOP_LOSS",
                        candles_held=index + 1,
                        r_multiple=-1.0,
                    )

                if low <= take_profit:
                    return TradeResult(
                        signal=signal,
                        entry_date=future_candles[0].datetime,
                        exit_date=candle.datetime,
                        entry_price=entry,
                        exit_price=take_profit,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        result="WIN",
                        exit_reason="TAKE_PROFIT",
                        candles_held=index + 1,
                        r_multiple=2.0,
                    )

        return TradeResult(
            signal=signal,
            entry_date=future_candles[0].datetime,
            exit_date=None,
            entry_price=entry,
            exit_price=None,
            stop_loss=stop_loss,
            take_profit=take_profit,
            result="OPEN",
            exit_reason=None,
            candles_held=len(future_candles),
            r_multiple=0.0,
        )