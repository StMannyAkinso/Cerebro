from .parameters import ParameterSpace


class ExperimentGenerator:

    def __init__(self, experiment_class, parameter_space):

        self.experiment_class = experiment_class
        self.parameter_space = parameter_space

    def generate(self):

        for parameters in self.parameter_space.generate():

            yield self.experiment_class(
                parameters=parameters
            )

    def count(self):

        return self.parameter_space.count()