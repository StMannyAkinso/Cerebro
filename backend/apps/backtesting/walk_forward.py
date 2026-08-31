from collections import Counter

from apps.backtesting.engine import BacktestEngine
from apps.backtesting.evaluation import ResearchEvaluator
from apps.markets.models import Market, MarketPrice


class WalkForwardResearchRunner:

    def __init__(
        self,
        experiment_class=None,
        experiment_classes=None,
        parameter_space=None,
    ):

        self.experiment_class = experiment_class
        self.experiment_classes = experiment_classes
        self.parameter_space = parameter_space

        self.engine = BacktestEngine()
        self.evaluator = ResearchEvaluator()

    # ---------------------------------------------------------
    # EXPERIMENT GENERATION
    # ---------------------------------------------------------

    def _generator(self, experiment_class):

        from apps.analysis.experiments.generator import (
            ExperimentGenerator
        )

        return ExperimentGenerator(
            experiment_class=experiment_class,
            parameter_space=self.parameter_space,
        )

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

        if self.experiment_class is None:

            raise ValueError(
                "No experiment_class or experiment_classes provided."
            )

        generator = self._generator(
            self.experiment_class
        )

        return list(generator.generate())

    # ---------------------------------------------------------
    # EVALUATION
    # ---------------------------------------------------------

    def _evaluate_experiment(
        self,
        symbol,
        experiment,
        end_date,
    ):

        backtest = self.engine.run(
            symbol,
            experiment,
            end_date=end_date,
        )

        evaluation = self.evaluator.evaluate(
            backtest
        )

        return {
            "experiment": experiment.name,
            "experiment_family": (
                experiment.__class__.__name__
            ),
            "parameters": experiment.parameters,
            "evaluation": evaluation,
        }

    # ---------------------------------------------------------
    # PARAMETER STABILITY
    # ---------------------------------------------------------

    def _parameter_stability(
        self,
        fold_results,
    ):

        print()
        print("=== PARAMETER STABILITY ===")

        if not fold_results:

            print("No fold results available.")
            return {}

        parameter_counts = {}

        for fold in fold_results:

            parameters = (
                fold["best_train"]["parameters"]
            )

            for parameter, value in parameters.items():

                if parameter not in parameter_counts:
                    parameter_counts[parameter] = Counter()

                parameter_counts[parameter][
                    str(value)
                ] += 1

        stability = {}

        for parameter, counts in parameter_counts.items():

            print()
            print(parameter)

            stability[parameter] = {}

            for value, count in counts.most_common():

                print(
                    f"  {value} -> selected "
                    f"{count}/{len(fold_results)} folds"
                )

                stability[parameter][value] = count

        return stability

    # ---------------------------------------------------------
    # WALK FORWARD
    # ---------------------------------------------------------

    def walk_forward(
        self,
        symbol,
        folds=4,
        initial_train_ratio=0.5,
    ):

        market = Market.objects.get(
            symbol=symbol
        )

        candles = list(
            MarketPrice.objects
            .filter(market=market)
            .order_by("datetime")
        )

        if len(candles) < 400:

            raise ValueError(
                "Not enough candles for walk-forward research."
            )

        if folds < 1:

            raise ValueError(
                "folds must be at least 1."
            )

        if not 0 < initial_train_ratio < 1:

            raise ValueError(
                "initial_train_ratio must be between 0 and 1."
            )

        experiments = self._build_experiments()

        if not experiments:

            raise ValueError(
                "No experiments were generated."
            )

        total_candles = len(candles)

        initial_train_size = int(
            total_candles * initial_train_ratio
        )

        remaining_candles = (
            total_candles - initial_train_size
        )

        test_size = remaining_candles // folds

        if test_size < 1:

            raise ValueError(
                "Not enough candles for the requested "
                "number of folds."
            )

        print()
        print("=== WALK-FORWARD RESEARCH ===")
        print(f"Symbol: {symbol}")
        print(f"Experiments: {len(experiments)}")
        print(f"Folds: {folds}")
        print()

        fold_results = []

        # -----------------------------------------------------
        # FOLDS
        # -----------------------------------------------------

        for fold in range(folds):

            train_end_index = (
                initial_train_size
                + (fold * test_size)
                - 1
            )

            test_start_index = (
                train_end_index + 1
            )

            if fold == folds - 1:

                test_end_index = (
                    total_candles - 1
                )

            else:

                test_end_index = (
                    test_start_index
                    + test_size
                    - 1
                )

            train_end = candles[
                train_end_index
            ].datetime

            test_start = candles[
                test_start_index
            ].datetime

            test_end = candles[
                test_end_index
            ].datetime

            print(
                f"Fold {fold + 1}/{folds}: "
                f"training {len(experiments)} experiments..."
            )

            # -------------------------------------------------
            # TRAINING
            # -------------------------------------------------

            train_results = []

            for index, experiment in enumerate(
                experiments,
                start=1,
            ):

                if (
                    index == 1
                    or index % 10 == 0
                    or index == len(experiments)
                ):

                    print(
                        f"  Training experiment "
                        f"{index}/{len(experiments)}..."
                    )

                result = self._evaluate_experiment(
                    symbol=symbol,
                    experiment=experiment,
                    end_date=train_end,
                )

                train_results.append(result)

            # -------------------------------------------------
            # SELECT BEST TRAINING EXPERIMENT
            # -------------------------------------------------

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

            print(
                f"  Best training experiment: "
                f"{best_experiment.name}"
            )

            # -------------------------------------------------
            # TEST
            # -------------------------------------------------

            print(
                "  Testing best experiment..."
            )

            test_backtest = self.engine.run(
                symbol,
                best_experiment,
                start_date=test_start,
                end_date=test_end,
            )

            test_evaluation = (
                self.evaluator.evaluate(
                    test_backtest
                )
            )

            # -------------------------------------------------
            # TEST DIAGNOSTICS
            # -------------------------------------------------

            test_results = test_backtest.get(
                "results",
                []
            )

            buy_signals = 0
            sell_signals = 0
            hold_signals = 0
            trades_taken = 0
            open_trades = 0

            for result in test_results:

                analysis = result.get(
                    "analysis"
                )

                simulation = result.get(
                    "simulation"
                )

                if analysis is not None:

                    strategy = analysis.get(
                        "strategy",
                        {}
                    )

                    signal = strategy.get(
                        "signal"
                    )

                    if signal == "BUY":
                        buy_signals += 1

                    elif signal == "SELL":
                        sell_signals += 1

                    else:
                        hold_signals += 1

                if simulation is not None:

                    trades_taken += 1

                    if simulation.exit_date is None:
                        open_trades += 1

            print(
                f"  Test complete: "
                f"{test_evaluation['trades']} trades, "
                f"{test_evaluation['total_r']} R"
            )

            print(
                f"    Results returned: "
                f"{len(test_results)}"
            )

            print(
                f"    BUY signals: "
                f"{buy_signals}"
            )

            print(
                f"    SELL signals: "
                f"{sell_signals}"
            )

            print(
                f"    HOLD candles: "
                f"{hold_signals}"
            )

            print(
                f"    Trades taken: "
                f"{trades_taken}"
            )

            print(
                f"    Open trades: "
                f"{open_trades}"
            )

            fold_results.append({
                "fold": fold + 1,
                "train_end": train_end,
                "test_start": test_start,
                "test_end": test_end,
                "best_train": best,
                "test_result": {
                    "experiment": (
                        best_experiment.name
                    ),
                    "parameters": (
                        best_experiment.parameters
                    ),
                    "evaluation": test_evaluation,
                    "diagnostics": {
                        "results_returned": (
                            len(test_results)
                        ),
                        "buy_signals": buy_signals,
                        "sell_signals": sell_signals,
                        "hold_signals": hold_signals,
                        "trades_taken": trades_taken,
                        "open_trades": open_trades,
                    },
                },
            })

        # -----------------------------------------------------
        # PARAMETER STABILITY
        # -----------------------------------------------------

        parameter_stability = (
            self._parameter_stability(
                fold_results
            )
        )

        # -----------------------------------------------------
        # SUMMARY
        # -----------------------------------------------------

        total_test_r = sum(
            fold["test_result"]["evaluation"]["total_r"]
            for fold in fold_results
        )

        total_test_trades = sum(
            fold["test_result"]["evaluation"]["trades"]
            for fold in fold_results
        )

        total_wins = sum(
            fold["test_result"]["evaluation"]["wins"]
            for fold in fold_results
        )

        total_losses = sum(
            fold["test_result"]["evaluation"]["losses"]
            for fold in fold_results
        )

        total_open = sum(
            fold["test_result"]["evaluation"]["open"]
            for fold in fold_results
        )

        average_test_r = (
            total_test_r / total_test_trades
            if total_test_trades
            else 0
        )

        # -----------------------------------------------------
        # COMPLETE
        # -----------------------------------------------------

        print()
        print("=== WALK-FORWARD COMPLETE ===")
        print(
            f"Total test trades: "
            f"{total_test_trades}"
        )
        print(
            f"Total test R: "
            f"{total_test_r}"
        )
        print(
            f"Average test R: "
            f"{average_test_r}"
        )

        return {
            "symbol": symbol,
            "folds": folds,
            "initial_train_ratio": (
                initial_train_ratio
            ),
            "experiments_tested": len(
                experiments
            ),
            "fold_results": fold_results,
            "parameter_stability": (
                parameter_stability
            ),
            "summary": {
                "total_test_trades": (
                    total_test_trades
                ),
                "total_wins": total_wins,
                "total_losses": total_losses,
                "total_open": total_open,
                "total_test_r": total_test_r,
                "average_test_r": average_test_r,
            },
        }