from abc import ABC, abstractmethod


class Observation(ABC):

    name = ""

    @abstractmethod
    def calculate(self, df):
        pass