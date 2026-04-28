# Orange3-Robust

Robust regression and robust preprocessing widgets for Orange.

## Install From Git

During development, install the add-on from the GitHub repository:

```bash
pip install git+https://github.com/solresol/Orange3-Robust.git
```

Then open Orange. The widgets should appear in the **Robust** category:

- **Robust Scale**: median centering and quantile-range scaling.
- **Robust Regression**: Huber, RANSAC, and Theil-Sen regression learners.

If you are using the standalone Orange app, use the Python environment that
belongs to that Orange installation. If the Add-ons dialog supports URL/package
installation in that build, use the same Git URL.

For the macOS standalone app this command installs into Orange's bundled Python:

```bash
/Applications/Orange.app/Contents/MacOS/python -m pip install \
  git+https://github.com/solresol/Orange3-Robust.git
```

Restart Orange after installing so the widget registry is refreshed.

## Using in Orange

For a new workflow:

1. Add **Datasets**, **File**, or **Paint Data**.
2. Add **Select Columns** and set a continuous target variable.
3. Add **Robust Regression** and choose **Huber**, **RANSAC**, or **Theil-Sen**.
4. Turn on **Scale features by median and IQR before fitting** if you want
   robust scaling inside that learner.
5. Connect **Robust Regression** to **Predictions**, **Test & Score**, or
   **Data Table** outputs as needed.

The checked demo workflow in `docs/examples/robust-regression-demo.ows` shows
the recommended wiring:

![Orange workflow using Robust Regression](docs/images/orange-robust-demo-workflow.png)

The **Robust Regression** widget exposes the model choice, optional median/IQR
scaling, and per-method parameters:

![Robust Regression widget settings](docs/images/orange-robust-regression-widget.png)

## Local Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
pytest
QT_QPA_PLATFORM=offscreen python -m Orange.canvas
```

## Current Behaviour

The **Robust Regression** widget outputs:

- an Orange learner, suitable for **Test & Score** and **Predictions**;
- a fitted model when data with a continuous target is connected;
- annotated data containing predictions, residuals, and RANSAC inlier flags
  when available;
- a coefficient table when the fitted estimator exposes coefficients.

The **Robust Scale** widget outputs both a preprocessor and a transformed table,
so it can be placed before other Orange learners or used to inspect/export a
median/IQR-scaled table. Do not put **Robust Scale** before **Robust
Regression** if the regression widget's internal scaling checkbox is also on,
because that will scale continuous features twice.

## Why This Exists

The COMP2200 robust-regression material uses Orange for the ordinary linear
regression workflow, but Theil-Sen and RANSAC currently have to move into
Python for a clean comparison. This add-on fills that gap.

## Release Checklist

- Keep tests passing in a clean virtual environment.
- Verify `pip install git+https://github.com/solresol/Orange3-Robust.git`.
- Open Orange and confirm the **Robust** category loads.
- Wire `File -> Select Columns -> Robust Regression -> Test & Score`.
- Publish to PyPI as `Orange3-Robust`.
- Request inclusion in `biolab/orange3-addons` once PyPI install is stable.
