import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from AnyQt.QtWidgets import QApplication
import numpy as np
from Orange.data import ContinuousVariable, DiscreteVariable, Domain, Table

from orangecontrib.robust.learners import RANSACLearner
from orangecontrib.robust.widgets.owrobustregression import OWRobustRegression


def _mixed_regression_data():
    zone = DiscreteVariable("zone", values=("A", "B", "C"))
    size = ContinuousVariable("size")
    price = ContinuousVariable("price")
    x = np.array(
        [
            [0, 80],
            [1, 90],
            [2, 100],
            [0, 110],
            [1, 120],
            [2, 130],
            [0, 140],
            [1, 150],
            [2, 160],
        ],
        dtype=float,
    )
    y = np.array([100, 120, 155, 135, 150, 190, 170, 185, 225], dtype=float)
    return Table(Domain([zone, size], price), x, y)


def test_robust_regression_combo_box_stores_selected_value():
    app = QApplication.instance() or QApplication([])
    widget = OWRobustRegression()
    try:
        widget.learner_combo.setCurrentIndex(1)
        widget.learner_combo.textActivated.emit("RANSAC")
        assert widget.learner_name == "RANSAC"
        assert isinstance(widget._build_learner(), RANSACLearner)
    finally:
        widget.onDeleteWidget()
        app.processEvents()


def test_robust_regression_scaling_keeps_default_sklearn_preprocessors():
    app = QApplication.instance() or QApplication([])
    widget = OWRobustRegression()
    try:
        widget.robust_scale = True
        data = _mixed_regression_data()

        for learner_name in widget.LEARNER_NAMES:
            widget.learner_name = learner_name
            learner = widget._build_learner()

            preprocessor_names = [
                type(preprocessor).__name__
                for preprocessor in learner.active_preprocessors
            ]
            assert preprocessor_names[:3] == [
                "RobustScale",
                "HasClass",
                "Continuize",
            ]

            model = learner(data)
            widget.data = data
            coefficients = widget._coefficients_table(model)
            assert len(coefficients) == len(model.domain.attributes) + 1
    finally:
        widget.onDeleteWidget()
        app.processEvents()
