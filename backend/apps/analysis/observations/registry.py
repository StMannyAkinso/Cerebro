class HypothesisRegistry:

    def __init__(self):
        self._hypotheses = []

    def register(self, hypothesis):
        self._hypotheses.append(hypothesis)

    def all(self):
        return self._hypotheses


registry.register(
    EMAHypothesis()
)