from abc import ABC, abstractmethod


class Experiment(ABC):

    name = None

    @abstractmethod
    def build_observations(self):
        pass

    def build_derived_observations(self):
        return []

    @abstractmethod
    def build_strategy(self):
        pass