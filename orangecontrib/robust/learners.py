import sklearn.linear_model as skl
from Orange.regression import SklLearner


class TheilSenLearner(SklLearner):
    __wraps__ = skl.TheilSenRegressor  # robust to ~29% outliers in 1D
    name = "Theil–Sen"

    def __init__(
        self,
        preprocessors=None,
        fit_intercept=True,
        max_subpopulation=10000,
        n_subsamples=None,
        max_iter=300,
        tol=0.001,
        random_state=None,
        n_jobs=None,
        verbose=False,
    ):
        super().__init__(preprocessors=preprocessors)
        self.params = vars()


class HuberLearner(SklLearner):
    __wraps__ = skl.HuberRegressor     # L2 w/ Huber loss (epsilon controls robustness)
    name = "Huber"

    def __init__(
        self,
        preprocessors=None,
        epsilon=1.35,
        max_iter=100,
        alpha=0.0001,
        warm_start=False,
        fit_intercept=True,
        tol=1e-5,
    ):
        super().__init__(preprocessors=preprocessors)
        self.params = vars()


class RANSACLearner(SklLearner):
    __wraps__ = skl.RANSACRegressor    # random consensus, inlier mask available
    name = "RANSAC"

    def __init__(
        self,
        preprocessors=None,
        estimator=None,
        min_samples=None,
        residual_threshold=None,
        is_data_valid=None,
        is_model_valid=None,
        max_trials=100,
        max_skips=float("inf"),
        stop_n_inliers=float("inf"),
        stop_score=float("inf"),
        stop_probability=0.99,
        loss="absolute_error",
        random_state=None,
    ):
        super().__init__(preprocessors=preprocessors)
        self.params = vars()
