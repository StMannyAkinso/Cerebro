from itertools import product


class ParameterSpace:

    def __init__(self, parameters):

        if not parameters:
            raise ValueError(
                "ParameterSpace requires at least one parameter"
            )

        for name, values in parameters.items():

            if not values:
                raise ValueError(
                    f"Parameter '{name}' must contain at least one value"
                )

        self.parameters = parameters

    def generate(self):

        names = list(self.parameters.keys())
        value_sets = [
            self.parameters[name]
            for name in names
        ]

        for combination in product(*value_sets):

            yield dict(
                zip(names, combination)
            )

    def count(self):

        total = 1

        for values in self.parameters.values():
            total *= len(values)

        return total