import numpy as np

from Orange.data import ContinuousVariable, Domain, StringVariable, Table
from Orange.regression import Learner, Model
from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Msg, OWBaseWidget, Output

from orangecontrib.robust.learners import (
    HuberLearner,
    RANSACLearner,
    TheilSenLearner,
)
from orangecontrib.robust.preprocess import RobustScale


class OWRobustRegression(OWBaseWidget):
    name = "Robust Regression"
    description = "Theil-Sen, RANSAC, and Huber regression."
    icon = "icons/robust.svg"
    priority = 50

    class Inputs:
        data = Input("Data", Table, auto_summary=False)

    class Outputs:
        learner = Output("Learner", Learner, auto_summary=False)
        model = Output("Model", Model, auto_summary=False)
        annotated_data = Output("Annotated Data", Table, auto_summary=False)
        coefficients = Output("Coefficients", Table, auto_summary=False)

    class Error(OWBaseWidget.Error):
        fit_failed = Msg("{}")
        bad_target = Msg("Data must have a continuous target variable.")

    want_main_area = False
    replaces = []

    learner_name = Setting("Huber")
    robust_scale = Setting(False)

    theilsen_fit_intercept = Setting(True)
    theilsen_n_subsamples = Setting(0)
    theilsen_max_subpopulation = Setting(10000)
    theilsen_max_iter = Setting(300)
    theilsen_tol = Setting(0.001)
    theilsen_random_state = Setting(42)

    ransac_min_samples = Setting(0)
    ransac_residual_threshold = Setting(0.0)
    ransac_max_trials = Setting(100)
    ransac_stop_probability = Setting(0.99)
    ransac_random_state = Setting(42)

    huber_epsilon = Setting(1.35)
    huber_alpha = Setting(0.0001)
    huber_max_iter = Setting(200)
    huber_fit_intercept = Setting(True)

    LEARNERS = {
        "Huber": HuberLearner,
        "RANSAC": RANSACLearner,
        "Theil-Sen": TheilSenLearner,
    }
    LEARNER_NAMES = tuple(LEARNERS)

    def __init__(self):
        super().__init__()
        self.data = None

        model_box = gui.widgetBox(self.controlArea, "Model")
        self.learner_combo = gui.comboBox(
            model_box,
            self,
            "learner_name",
            items=self.LEARNER_NAMES,
            sendSelectedValue=True,
            callback=self._on_change,
        )
        gui.checkBox(
            model_box,
            self,
            "robust_scale",
            "Scale features by median and IQR before fitting",
            callback=self._on_change,
        )

        self._parameter_boxes = {
            "Huber": self._make_huber_box(),
            "RANSAC": self._make_ransac_box(),
            "Theil-Sen": self._make_theilsen_box(),
        }
        self._update_visible_parameters()
        self._send_learner()

    def _make_huber_box(self):
        box = gui.widgetBox(self.controlArea, "Huber")
        gui.doubleSpin(
            box,
            self,
            "huber_epsilon",
            minv=1.0,
            maxv=10.0,
            step=0.05,
            label="epsilon",
            callback=self._on_change,
        )
        gui.doubleSpin(
            box,
            self,
            "huber_alpha",
            minv=0.0,
            maxv=1.0,
            step=0.0001,
            label="alpha",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "huber_max_iter",
            minv=10,
            maxv=10000,
            label="max iterations",
            callback=self._on_change,
        )
        gui.checkBox(
            box,
            self,
            "huber_fit_intercept",
            "Fit intercept",
            callback=self._on_change,
        )
        return box

    def _make_ransac_box(self):
        box = gui.widgetBox(self.controlArea, "RANSAC")
        gui.spin(
            box,
            self,
            "ransac_min_samples",
            minv=0,
            maxv=10000,
            label="min samples (0 = auto)",
            callback=self._on_change,
        )
        gui.doubleSpin(
            box,
            self,
            "ransac_residual_threshold",
            minv=0.0,
            maxv=1.0e9,
            step=0.1,
            label="residual threshold (0 = auto)",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "ransac_max_trials",
            minv=1,
            maxv=100000,
            label="max trials",
            callback=self._on_change,
        )
        gui.doubleSpin(
            box,
            self,
            "ransac_stop_probability",
            minv=0.01,
            maxv=0.999999,
            step=0.01,
            label="stop probability",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "ransac_random_state",
            minv=-1,
            maxv=2 ** 31 - 1,
            label="random state (-1 = none)",
            callback=self._on_change,
        )
        return box

    def _make_theilsen_box(self):
        box = gui.widgetBox(self.controlArea, "Theil-Sen")
        gui.spin(
            box,
            self,
            "theilsen_n_subsamples",
            minv=0,
            maxv=10000,
            label="subsamples (0 = auto)",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "theilsen_max_subpopulation",
            minv=1,
            maxv=1000000,
            label="max subpopulation",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "theilsen_max_iter",
            minv=1,
            maxv=10000,
            label="max iterations",
            callback=self._on_change,
        )
        gui.doubleSpin(
            box,
            self,
            "theilsen_tol",
            minv=0.0,
            maxv=1.0,
            step=0.0001,
            label="tolerance",
            callback=self._on_change,
        )
        gui.spin(
            box,
            self,
            "theilsen_random_state",
            minv=-1,
            maxv=2 ** 31 - 1,
            label="random state (-1 = none)",
            callback=self._on_change,
        )
        gui.checkBox(
            box,
            self,
            "theilsen_fit_intercept",
            "Fit intercept",
            callback=self._on_change,
        )
        return box

    def _update_visible_parameters(self):
        for name, box in self._parameter_boxes.items():
            box.setVisible(name == self.learner_name)

    def _params(self):
        if self.learner_name == "Huber":
            return {
                "epsilon": self.huber_epsilon,
                "alpha": self.huber_alpha,
                "max_iter": self.huber_max_iter,
                "fit_intercept": self.huber_fit_intercept,
            }
        if self.learner_name == "RANSAC":
            params = {
                "max_trials": self.ransac_max_trials,
                "stop_probability": self.ransac_stop_probability,
            }
            if self.ransac_min_samples:
                params["min_samples"] = self.ransac_min_samples
            if self.ransac_residual_threshold > 0:
                params["residual_threshold"] = self.ransac_residual_threshold
            if self.ransac_random_state >= 0:
                params["random_state"] = self.ransac_random_state
            return params

        params = {
            "fit_intercept": self.theilsen_fit_intercept,
            "max_subpopulation": self.theilsen_max_subpopulation,
            "max_iter": self.theilsen_max_iter,
            "tol": self.theilsen_tol,
        }
        if self.theilsen_n_subsamples:
            params["n_subsamples"] = self.theilsen_n_subsamples
        if self.theilsen_random_state >= 0:
            params["random_state"] = self.theilsen_random_state
        return params

    def _build_learner(self):
        learner_cls = self.LEARNERS[self.learner_name]
        kwargs = self._params()
        if self.robust_scale:
            kwargs["preprocessors"] = [RobustScale()]
        learner = learner_cls(**kwargs)
        if self.robust_scale:
            learner.use_default_preprocessors = True
        return learner

    def _send_learner(self):
        self.Outputs.learner.send(self._build_learner())

    @Inputs.data
    def set_data(self, data):
        self.data = data
        self._maybe_fit()

    def _maybe_fit(self):
        self.Error.clear()
        self.Outputs.model.send(None)
        self.Outputs.annotated_data.send(None)
        self.Outputs.coefficients.send(None)

        if self.data is None:
            return
        if not self.data.domain.class_var or not self.data.domain.class_var.is_continuous:
            self.Error.bad_target()
            return

        learner = self._build_learner()
        try:
            model = learner(self.data)
        except Exception as exc:  # pragma: no cover - exercised manually in Orange
            self.Error.fit_failed(str(exc))
            return

        self.Outputs.model.send(model)
        self.Outputs.annotated_data.send(self._annotated_data(model))
        self.Outputs.coefficients.send(self._coefficients_table(model))

    def _on_change(self):
        self._update_visible_parameters()
        self._send_learner()
        self._maybe_fit()

    def _sklearn_model(self, model):
        skl_model = getattr(model, "skl_model", None)
        if skl_model is None:
            skl_model = getattr(model, "model", None)
        return skl_model

    def _annotated_data(self, model):
        predictions = np.asarray(model(self.data), dtype=float).reshape(-1, 1)
        residuals = np.asarray(self.data.Y, dtype=float).reshape(-1, 1) - predictions

        metas = self.data.metas
        if metas.size == 0:
            metas = np.empty((len(self.data), 0), dtype=object)

        meta_vars = list(self.data.domain.metas)
        meta_columns = [
            predictions,
            residuals,
        ]
        meta_vars.extend(
            [
                ContinuousVariable(f"{self.learner_name} Prediction"),
                ContinuousVariable(f"{self.learner_name} Residual"),
            ]
        )

        skl_model = self._sklearn_model(model)
        inlier_mask = getattr(skl_model, "inlier_mask_", None)
        if inlier_mask is not None:
            meta_vars.append(ContinuousVariable("RANSAC Inlier"))
            meta_columns.append(np.asarray(inlier_mask, dtype=float).reshape(-1, 1))

        new_domain = Domain(
            self.data.domain.attributes,
            self.data.domain.class_vars,
            meta_vars,
        )
        new_metas = np.hstack([metas] + meta_columns)
        return Table(new_domain, self.data.X, self.data.Y, metas=new_metas)

    def _coefficients_table(self, model):
        skl_model = self._sklearn_model(model)
        if skl_model is None:
            return None

        coef_source = getattr(skl_model, "estimator_", skl_model)
        coefs = getattr(coef_source, "coef_", None)
        intercept = getattr(coef_source, "intercept_", None)
        if coefs is None:
            return None

        names = [var.name for var in model.domain.attributes]
        values = np.asarray(coefs, dtype=float).ravel()

        if intercept is not None:
            names = ["intercept"] + names
            values = np.concatenate([[float(np.asarray(intercept).ravel()[0])], values])

        domain = Domain([ContinuousVariable("coefficient")], metas=[StringVariable("term")])
        return Table(
            domain,
            values.reshape(-1, 1),
            metas=np.asarray(names, dtype=object).reshape(-1, 1),
        )


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWRobustRegression).run(Table("housing"))
