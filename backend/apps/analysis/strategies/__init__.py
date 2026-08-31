from .registry import registry

from .momentum import MomentumStrategy
from .trend_following import TrendFollowingStrategy


registry.register(MomentumStrategy)
registry.register(TrendFollowingStrategy)