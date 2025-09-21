from orangewidget.widget import OWBaseWidget, Input, Output
from orangewidget import gui
from Orange.data import Table
from Orange.regression import Learner, Model
from orangecontrib.robust.learners import TheilSenLearner, HuberLearner, RANSACLearner

class OWRobustRegression(OWBaseWidget):
    name = "Robust Regression"
    description = "Theil–Sen, RANSAC, and Huber"
    icon = "icons/robust.svg"
    priority = 50  # lives in the Model pane

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        learner = Output("Learner", Learner)
        model = Output("Model", Model)

    want_main_area = False

    LEARNERS = {
        "Theil–Sen": (TheilSenLearner, {"fit_intercept": True, "max_iter": 300, "tol": 1e-3}),
        "RANSAC":    (RANSACLearner,    {"max_trials": 100, "stop_probability": 0.99}),
        "Huber":     (HuberLearner,     {"epsilon": 1.35, "alpha": 1e-4, "fit_intercept": True}),
    }

    def __init__(self):
        super().__init__()
        self.learner_name = "Huber"
        self.params = dict(self.LEARNERS[self.learner_name][1])

        box = gui.widgetBox(self.controlArea, "Model")
        gui.comboBox(box, self, "learner_name",
                     items=list(self.LEARNERS),
                     callback=self._on_change)

        # TODO: add per-learner parameter editors (gui.spin, gui.doubleSpin, gui.checkBox)
        # and keep self.params in sync. For RANSAC consider exposing residual_threshold,
        # min_samples, max_trials; for Theil–Sen: n_subsamples, max_subpopulation; for Huber: epsilon, alpha.

        self.data = None
        self._send_learner()

    def _build_learner(self):
        L, defaults = self.LEARNERS[self.learner_name]
        return L(**self.params)

    def _send_learner(self):
        self.Outputs.learner.send(self._build_learner())

    @Inputs.data
    def set_data(self, data):
        self.data = data
        self._maybe_fit()

    def _maybe_fit(self):
        if self.data is not None:
            model = self._build_learner()(self.data)
            self.Outputs.model.send(model)
        else:
            self.Outputs.model.send(None)

    def _on_change(self):
        # reset params when algorithm changes and re-emit learner/model
        self.params = dict(self.LEARNERS[self.learner_name][1])
        self._send_learner()
        self._maybe_fit()

if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWRobustRegression).run(Table("housing"))

# Nice extras (worth doing):
#	•	RANSAC inlier mask output: add a third output that appends inlier as a meta/flag column to the input table (so users can visualise inliers vs outliers).
#	•	Standardise features toggle (wrap the learner in a StandardScaler pipeline) — Huber is sensitive to feature scaling.  ￼
#	•	Coefficients output: for Theil–Sen/Huber, output a small table of coef_/intercept_ for Explain and Data Table workflows.
