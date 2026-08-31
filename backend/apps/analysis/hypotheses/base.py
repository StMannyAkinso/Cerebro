from abc import ABC, abstractmethod


class Hypothesis(ABC):

    name = ""

    @abstractmethod
    def evaluate(self, observations):
        pass