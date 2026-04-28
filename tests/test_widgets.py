import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from AnyQt.QtWidgets import QApplication

from orangecontrib.robust.learners import RANSACLearner, TheilSenLearner
from orangecontrib.robust.widgets.owrobustregression import OWRobustRegression


def test_robust_regression_migrates_old_combo_box_indices():
    app = QApplication.instance() or QApplication([])
    widget = OWRobustRegression()
    try:
        widget.learner_name = 1
        assert isinstance(widget._build_learner(), RANSACLearner)
        assert widget.learner_name == "RANSAC"

        widget.learner_name = 2
        assert isinstance(widget._build_learner(), TheilSenLearner)
        assert widget.learner_name == "Theil-Sen"
    finally:
        widget.onDeleteWidget()
        app.processEvents()
