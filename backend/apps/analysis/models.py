from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Trade:

    symbol: str

    signal: str

    entry: Decimal

    stop_loss: Decimal

    take_profit: Decimal

    confidence: int

    reasons: list[str]