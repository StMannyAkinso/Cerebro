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