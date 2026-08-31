class ObservationRegistry:

    def __init__(self):
        self._observations = {}

    def register(self, observation_class):
        name = observation_class.name

        if not name:
            raise ValueError(
                "Observation class must define a name."
            )

        if name in self._observations:
            raise ValueError(
                f"Observation '{name}' is already registered."
            )

        self._observations[name] = observation_class

    def get(self, name):
        return self._observations[name]

    def all(self):
        return self._observations.copy()


registry = ObservationRegistry()