# Orange3-Robust Development

## Install From Git

During development, install the add-on from the GitHub repository:

```bash
pip install git+https://github.com/solresol/Orange3-Robust.git
```

Then open Orange. The widgets should appear in the **Robust** category:

- **Robust Scale**: median centering and quantile-range scaling.
- **Robust Regression**: Huber, Least Absolute Deviation, RANSAC, and Theil-Sen
  regression learners.

If you are using the standalone Orange app, use the Python environment that
belongs to that Orange installation. If the Add-ons dialog supports URL/package
installation in that build, use the same Git URL.

For the macOS standalone app this command installs into Orange's bundled Python:

```bash
/Applications/Orange.app/Contents/MacOS/python -m pip install \
  git+https://github.com/solresol/Orange3-Robust.git
```

Restart Orange after installing so the widget registry is refreshed.

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

- an Orange learner, suitable for **Test and Score** and **Predictions**;
- a fitted model when data with a continuous target is connected;
- annotated data containing predictions, residuals, and RANSAC inlier flags
  when available;
- a coefficient table when the fitted estimator exposes coefficients.

The **Robust Scale** widget outputs both a preprocessor and a transformed table,
so it can be placed before other Orange learners or used to inspect/export a
median/IQR-scaled table.

## Release Checklist

- Keep tests passing in a clean virtual environment.
- Verify `pip install git+https://github.com/solresol/Orange3-Robust.git`.
- Open Orange and confirm the **Robust** category loads.
- Wire `File -> Select Columns -> Robust Regression -> Test & Score`.
- Publish to PyPI as `Orange3-Robust`.
- Request inclusion in `biolab/orange3-addons` once PyPI install is stable.

## PyPI Publishing

The repository has a `.github/workflows/publish.yml` workflow for PyPI Trusted
Publishing. In PyPI, configure a trusted publisher for:

- repository: `solresol/Orange3-Robust`
- workflow: `publish.yml`
- environment: `pypi`

Then create a GitHub release for the version being published. The workflow
builds the source distribution and wheel, runs `twine check`, and publishes with
PyPI's OpenID Connect flow, so no long-lived PyPI token is needed in GitHub
Secrets.
