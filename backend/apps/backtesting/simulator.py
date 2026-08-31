from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeResult:

    signal: str

    entry_date: datetime

    exit_date: datetime | None

    entry_price: float

    exit_price: float | None

    stop_loss: float

    take_profit: float

    result: str

    exit_reason: str | None

    candles_held: int

    r_multiple: float


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

        # Calculate the actual amount risked per trade.
        risk = abs(entry - stop_loss)

        if risk == 0:
            raise ValueError(
                "Stop loss cannot be equal to entry price."
            )

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

                    reward = take_profit - entry
                    r_multiple = reward / risk

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
                        r_multiple=r_multiple,
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

                    reward = entry - take_profit
                    r_multiple = reward / risk

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
                        r_multiple=r_multiple,
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