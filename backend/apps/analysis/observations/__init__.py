from .registry import registry

from .ema import EMAObservation
from .rsi import RSIObservation
from .atr import ATRObservation
from .momentum import MomentumObservation


registry.register(EMAObservation)
registry.register(RSIObservation)
registry.register(ATRObservation)
registry.register(MomentumObservation)