from .trend_following import TrendFollowingExperiment
from .momentum import MomentumExperiment


EXPERIMENT_REGISTRY = {
    "trend_following": TrendFollowingExperiment,
    "momentum": MomentumExperiment,
}


def get_experiment(name):

    try:
        return EXPERIMENT_REGISTRY[name]

    except KeyError:
        raise ValueError(
            f"Unknown experiment: {name}"
        )


def get_all_experiments():

    return EXPERIMENT_REGISTRY.copy()