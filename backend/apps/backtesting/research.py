from apps.backtesting.engine import BacktestEngine
from apps.backtesting.evaluation import ResearchEvaluator
from apps.markets.models import Market, MarketPrice


class ResearchRunner:

    def __init__(
        self,
        experiment_class=None,
        experiment_classes=None,
        parameter_space=None,
        train_ratio=0.7,
    ):

        self.experiment_class = experiment_class
        self.experiment_classes = experiment_classes
        self.parameter_space = parameter_space
        self.train_ratio = train_ratio

        self.engine = BacktestEngine()
        self.evaluator = ResearchEvaluator()

    def _build_experiments(self):

        if self.experiment_classes is not None:

            experiments = []

            for experiment_class in self.experiment_classes:

                generator = self._generator(
                    experiment_class
                )

                experiments.extend(
                    list(generator.generate())
                )

            return experiments

        generator = self._generator(
            self.experiment_class
        )

        return list(generator.generate())

    def _generator(self, experiment_class):

        from apps.analysis.experiments.generator import (
            ExperimentGenerator
        )

        return ExperimentGenerator(
            experiment_class=experiment_class,
            parameter_space=self.parameter_space,
        )

    def run(self, symbol):

        market = Market.objects.get(symbol=symbol)

        candles = list(
            MarketPrice.objects
            .filter(market=market)
            .order_by("datetime")
        )

        if len(candles) < 400:

            raise ValueError(
                "Not enough candles for train/test research."
            )

        split_index = int(
            len(candles) * self.train_ratio
        )

        train_end = candles[
            split_index - 1
        ].datetime

        test_start = candles[
            split_index
        ].datetime

        experiments = self._build_experiments()

        train_results = []

        total_experiments = len(experiments)

        print()
        print("=== TRAIN / TEST RESEARCH ===")
        print(f"Symbol: {symbol}")
        print(f"Experiments: {total_experiments}")
        print()

        for index, experiment in enumerate(
            experiments,
            start=1,
        ):

            if (
                index == 1
                or index % 10 == 0
                or index == total_experiments
            ):

                print(
                    f"Training experiment "
                    f"{index}/{total_experiments}..."
                )

            backtest = self.engine.run(
                symbol,
                experiment,
                end_date=train_end,
            )

            evaluation = self.evaluator.evaluate(
                backtest
            )

            train_results.append({
                "experiment": experiment.name,
                "experiment_family": (
                    experiment.__class__.__name__
                ),
                "parameters": experiment.parameters,
                "evaluation": evaluation,
            })

        train_results.sort(
            key=lambda result: (
                result["evaluation"]["average_r"]
            ),
            reverse=True,
        )

        best = train_results[0]

        best_experiment = next(
            experiment
            for experiment in experiments
            if experiment.name == best["experiment"]
        )

        print()
        print(
            "Best training experiment:",
            best_experiment.name,
        )

        print("Testing best experiment...")

        test_backtest = self.engine.run(
            symbol,
            best_experiment,
            start_date=test_start,
        )

        test_evaluation = self.evaluator.evaluate(
            test_backtest
        )

        print(
            "Test complete:",
            test_evaluation["trades"],
            "trades,",
            test_evaluation["total_r"],
            "R",
        )

        return {
            "symbol": symbol,
            "train_ratio": self.train_ratio,
            "train_end": train_end,
            "test_start": test_start,
            "experiments_tested": len(experiments),
            "train_results": train_results,
            "best_train": best,
            "test_result": {
                "experiment": best_experiment.name,
                "parameters": best_experiment.parameters,
                "evaluation": test_evaluation,
            },
        }