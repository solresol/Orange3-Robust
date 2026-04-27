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
so it can be placed before other Orange learners as well as the robust learners.

## Why This Exists

The COMP2200 robust-regression material uses Orange for the ordinary linear
regression workflow, but Theil-Sen and RANSAC currently have to move into
Python for a clean comparison. This add-on fills that gap.

## Release Checklist

- Keep tests passing in a clean virtual environment.
- Verify `pip install git+https://github.com/solresol/Orange3-Robust.git`.
- Open Orange and confirm the **Robust** category loads.
- Wire `File -> Select Columns -> Robust Regression -> Predictions`.
- Publish to PyPI as `Orange3-Robust`.
- Request inclusion in `biolab/orange3-addons` once PyPI install is stable.
