from abc import ABC, abstractmethod


class Strategy(ABC):

    name = ""

    @abstractmethod
    def evaluate(self, observations):
        pass