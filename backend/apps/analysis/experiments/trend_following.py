from apps.analysis.experiments.base import Experiment

from apps.analysis.observations.ema import EMAObservation
from apps.analysis.observations.rsi import RSIObservation
from apps.analysis.observations.atr import ATRObservation
from apps.analysis.observations.trend import TrendObservation

from apps.analysis.strategies.trend_following import TrendFollowingStrategy

from apps.analysis.observations.price_action import PriceActionObservation

class TrendFollowingExperiment(Experiment):

    default_parameters = {
        "ema_fast": 20,
        "ema_mid": 50,
        "ema_slow": 200,
        "rsi_window": 14,
        "atr_window": 14,
        "stop_loss_atr": 1.0,
        "take_profit_atr": 2.0,
    }

    def __init__(self, parameters=None):

        parameters = parameters or {}

        self.parameters = {
            **self.default_parameters,
            **parameters,
        }

        self.name = self._build_name()

    def _build_name(self):

        return (
            "trend_following"
            f"_ema{self.parameters['ema_fast']}"
            f"-{self.parameters['ema_mid']}"
            f"-{self.parameters['ema_slow']}"
            f"_rsi{self.parameters['rsi_window']}"
            f"_atr{self.parameters['atr_window']}"
            f"_sl{self.parameters['stop_loss_atr']}"
            f"_tp{self.parameters['take_profit_atr']}"
        )

    def build_observations(self):

        return [
            EMAObservation(
                fast_window=self.parameters["ema_fast"],
                mid_window=self.parameters["ema_mid"],
                slow_window=self.parameters["ema_slow"],
            ),
            RSIObservation(
                window=self.parameters["rsi_window"],
            ),
            ATRObservation(
                window=self.parameters["atr_window"],
            ),
            PriceActionObservation(),
        ]

    def build_derived_observations(self):

        return [
            TrendObservation(),
        ]

    def build_strategy(self):

        return TrendFollowingStrategy(
            stop_loss_atr=self.parameters["stop_loss_atr"],
            take_profit_atr=self.parameters["take_profit_atr"],
        )