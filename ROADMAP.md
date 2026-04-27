# Orange3-Robust Roadmap

## Goal

Make robust regression workflows available inside Orange without forcing COMP2200
students into the Python Script widget or a notebook for the first comparison.

The add-on should install from a Git URL during development, then from PyPI once
the widget behaviour is stable enough for the official Orange add-ons list.

## Implemented

- Robust Regression widget with Huber, RANSAC, and Theil-Sen learners.
- Optional median/IQR feature scaling before fitting.
- Annotated output data with predictions and residuals.
- RANSAC inlier flag when the fitted sklearn model exposes one.
- Coefficient table output where the fitted sklearn estimator exposes
  `coef_` and `intercept_`.
- Robust Scale widget with median centering and quantile-range scaling.

## Near-Term Requirements

- Keep `pip install git+https://github.com/solresol/Orange3-Robust.git`
  working from a clean Orange-compatible Python environment.
- Keep all widgets importable by Orange's `orange.widgets` entry point.
- Test learner fitting, robust scaling, package metadata, and widget imports in
  CI.
- Add one small demo workflow once the widget names settle.
- Publish a PyPI release before requesting inclusion in the official Orange
  add-ons list.

## Candidate Robust Methods

- Quantile Regression for pinball-loss regression and conditional quantiles.
- Winsorize or Clip Outliers as a preprocessing widget with explicit limits.
- Median/MAD Outlier Scores for transparent univariate robust diagnostics.
- Robust covariance / Elliptic Envelope for multivariate outlier marking.
- Siegel repeated-median regression if a maintained implementation is available.

Keep the scope narrow: methods belong here when they expose robust modelling or
robust preprocessing that Orange does not already make available cleanly.
