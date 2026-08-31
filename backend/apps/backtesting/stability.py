from collections import Counter


class ParameterStabilityAnalyzer:

    def analyze(self, fold_results):

        if not fold_results:
            return {}

        parameter_values = {}

        for fold in fold_results:

            parameters = (
                fold["test_result"]["parameters"]
            )

            for parameter, value in parameters.items():

                if parameter not in parameter_values:
                    parameter_values[parameter] = []

                parameter_values[parameter].append(value)

        stability = {}

        for parameter, values in parameter_values.items():

            counts = Counter(values)

            stability[parameter] = dict(
                counts.most_common()
            )

        return stability

    def print_report(self, stability, folds):

        print()
        print("=== PARAMETER STABILITY ===")
        print()

        for parameter, values in stability.items():

            print(parameter)

            for value, count in values.items():

                print(
                    f"  {value} -> "
                    f"selected {count}/{folds} folds"
                )

            print()