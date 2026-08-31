class StrategyRegistry:

    def __init__(self):
        self._strategies = {}

    def register(self, strategy_class):
        name = strategy_class.name

        if not name:
            raise ValueError(
                "Strategy class must define a name."
            )

        if name in self._strategies:
            raise ValueError(
                f"Strategy '{name}' is already registered."
            )

        self._strategies[name] = strategy_class

    def get(self, name):
        return self._strategies[name]

    def all(self):
        return self._strategies.copy()


registry = StrategyRegistry()