import numpy as np

from Orange.data import ContinuousVariable, Domain, Table

from orangecontrib.robust.preprocess import RobustScale


def test_robust_scale_centers_by_median_and_scales_by_iqr():
    x = np.array([[0.0], [1.0], [2.0], [3.0], [100.0]])
    y = np.arange(len(x), dtype=float)
    data = Table(Domain([ContinuousVariable("x")], ContinuousVariable("y")), x, y)

    scaled = RobustScale()(data)
    values = scaled.X[:, 0]

    assert np.median(values) == 0.0
    assert np.percentile(values, 75) - np.percentile(values, 25) == 1.0
    np.testing.assert_array_equal(scaled.Y, y)


def test_robust_scale_leaves_constant_columns_finite():
    x = np.ones((4, 1))
    data = Table(Domain([ContinuousVariable("x")]), x)

    scaled = RobustScale()(data)

    assert np.all(np.isfinite(scaled.X))
    np.testing.assert_array_equal(scaled.X, np.zeros((4, 1)))
