import numpy as np

from Orange.data import ContinuousVariable, Domain, Table

from orangecontrib.robust.learners import HuberLearner, RANSACLearner, TheilSenLearner
from orangecontrib.robust.preprocess import RobustScale


def regression_table():
    x = np.linspace(-2, 2, 20).reshape(-1, 1)
    y = 3 * x[:, 0] + 1
    return Table(Domain([ContinuousVariable("x")], ContinuousVariable("y")), x, y)


def test_robust_learners_fit_and_predict():
    data = regression_table()

    learners = [
        HuberLearner(max_iter=200),
        RANSACLearner(random_state=0),
        TheilSenLearner(random_state=0, max_subpopulation=10000),
    ]

    for learner in learners:
        model = learner(data)
        predictions = np.asarray(model(data), dtype=float)
        assert predictions.shape == (len(data),)
        assert np.all(np.isfinite(predictions))


def test_learners_accept_robust_scale_preprocessor():
    data = regression_table()
    learner = HuberLearner(max_iter=200, preprocessors=[RobustScale()])

    model = learner(data)

    assert np.all(np.isfinite(model(data)))
