from Orange.data import Table
from Orange.preprocess import Preprocess
from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Msg, OWBaseWidget, Output

from orangecontrib.robust.preprocess import RobustScale


class OWRobustScale(OWBaseWidget):
    name = "Robust Scale"
    description = "Center continuous features by median and scale by IQR."
    icon = "icons/RobustScale.svg"
    priority = 40

    class Inputs:
        data = Input("Data", Table, auto_summary=False)

    class Outputs:
        preprocessor = Output("Preprocessor", Preprocess, auto_summary=False)
        preprocessed_data = Output("Preprocessed Data", Table, auto_summary=False)

    class Error(OWBaseWidget.Error):
        transform_failed = Msg("{}")

    want_main_area = False
    replaces = []

    with_centering = Setting(True)
    with_scaling = Setting(True)
    lower_quantile = Setting(25.0)
    upper_quantile = Setting(75.0)

    def __init__(self):
        super().__init__()
        self.data = None

        box = gui.widgetBox(self.controlArea, "Robust scaling")
        gui.checkBox(
            box,
            self,
            "with_centering",
            "Center by median",
            callback=self.commit,
        )
        gui.checkBox(
            box,
            self,
            "with_scaling",
            "Scale by quantile range",
            callback=self.commit,
        )
        gui.doubleSpin(
            box,
            self,
            "lower_quantile",
            minv=0.0,
            maxv=100.0,
            step=1.0,
            label="lower quantile",
            callback=self.commit,
        )
        gui.doubleSpin(
            box,
            self,
            "upper_quantile",
            minv=0.0,
            maxv=100.0,
            step=1.0,
            label="upper quantile",
            callback=self.commit,
        )
        gui.rubber(self.controlArea)
        self.commit()

    @Inputs.data
    def set_data(self, data):
        self.data = data
        self.commit()

    def _preprocessor(self):
        lower = min(self.lower_quantile, self.upper_quantile)
        upper = max(self.lower_quantile, self.upper_quantile)
        if lower == upper:
            lower, upper = 25.0, 75.0
        return RobustScale(
            with_centering=self.with_centering,
            with_scaling=self.with_scaling,
            quantile_range=(lower, upper),
        )

    def commit(self):
        self.Error.clear()
        preprocessor = self._preprocessor()
        self.Outputs.preprocessor.send(preprocessor)

        if self.data is None:
            self.Outputs.preprocessed_data.send(None)
            return

        try:
            self.Outputs.preprocessed_data.send(preprocessor(self.data))
        except Exception as exc:  # pragma: no cover - exercised manually in Orange
            self.Error.transform_failed(str(exc))
            self.Outputs.preprocessed_data.send(None)


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWRobustScale).run(Table("housing"))
