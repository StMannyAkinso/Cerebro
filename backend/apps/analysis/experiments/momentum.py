from apps.analysis.experiments.base import Experiment
from apps.analysis.observations.momentum import MomentumObservation
from apps.analysis.observations.atr import ATRObservation
from apps.analysis.strategies.momentum import MomentumStrategy


class MomentumExperiment(Experiment):

    default_parameters = {
        "momentum_window": 14,
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
            "momentum"
            f"_window{self.parameters['momentum_window']}"
            f"_atr{self.parameters['atr_window']}"
            f"_sl{self.parameters['stop_loss_atr']}"
            f"_tp{self.parameters['take_profit_atr']}"
        )

    def build_observations(self):

        return [
            MomentumObservation(
                window=self.parameters["momentum_window"],
            ),

            ATRObservation(
                window=self.parameters["atr_window"],
            ),
        ]

    def build_derived_observations(self):

        return []

    def build_strategy(self):

        return MomentumStrategy(
            stop_loss_atr=self.parameters["stop_loss_atr"],
            take_profit_atr=self.parameters["take_profit_atr"],
        )