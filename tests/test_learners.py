import numpy as np

from Orange.data import ContinuousVariable, Domain, StringVariable, Table, TimeVariable
from Orange.regression.linear import LinearRegressionLearner

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


def _learner_variants():
    return [
        HuberLearner(max_iter=500),
        RANSACLearner(random_state=0, max_trials=25),
        TheilSenLearner(random_state=0, max_subpopulation=100, max_iter=10),
    ]


def _scaled(learner):
    learner.preprocessors = (RobustScale(),)
    learner.use_default_preprocessors = True
    return learner


def _assert_same_preprocessed_domain_as_ols(data):
    ols_model = LinearRegressionLearner()(data)
    expected = [var.name for var in ols_model.domain.attributes]

    for learner in _learner_variants() + [_scaled(learner) for learner in _learner_variants()]:
        model = learner(data)

        assert [var.name for var in model.domain.attributes] == expected
        assert np.all(np.isfinite(model(data)))


def test_robust_learners_handle_datetime_attributes_like_ols():
    x = ContinuousVariable("x")
    when = TimeVariable("when")
    y = ContinuousVariable("y")
    domain = Domain([when, x], y)
    x_values = np.arange(12, dtype=float)
    time_values = 1_700_000_000 + np.array(
        [0, 2, 3, 7, 11, 12, 15, 19, 21, 28, 30, 34], dtype=float
    ) * 86_400
    data = Table(
        domain,
        np.column_stack([time_values, x_values]),
        4 * x_values + 1,
    )

    _assert_same_preprocessed_domain_as_ols(data)


def test_robust_learners_ignore_text_metas_like_ols():
    x = ContinuousVariable("x")
    y = ContinuousVariable("y")
    note = StringVariable("note")
    domain = Domain([x], y, metas=[note])
    x_values = np.arange(12, dtype=float)
    metas = np.array([[f"row {i}"] for i in range(12)], dtype=object)
    data = Table(domain, x_values.reshape(-1, 1), 4 * x_values + 1, metas=metas)

    _assert_same_preprocessed_domain_as_ols(data)
