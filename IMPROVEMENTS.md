# Orange3-Robust — Improvements

*Analysis date: 2026-07-11.*

Orange3-Robust is a small, well-shaped Orange add-on (~860 lines of Python) providing two widgets — **Robust Regression** (Huber, LAD/quantile, RANSAC, Theil-Sen, in `orangecontrib/robust/learners.py` and `widgets/owrobustregression.py`) and **Robust Scale** (`preprocess.py`, `widgets/owrobustscale.py`) — aimed at COMP2200 students. It is at v0.1.0, packaged with pyproject.toml, has CI (`tests.yml`) and a publish workflow, tests, docs with screenshots, and a clear ROADMAP.md. The working tree is clean. It is close to release-quality; the remaining work is mostly polish, roadmap follow-through, and release logistics.

## Bugs & Fixes

- **Learner-name key mismatch risk**: `OWRobustRegression.LEARNERS` uses the key `"Theil-Sen"` while `TheilSenLearner.name` is `"Theil–Sen"` (en dash), and pyproject's description also uses the en dash. The `learner_name` Setting stores the string; any future rename of either side silently breaks saved workflows. Normalize on one spelling and add a settings-migration hook (`settings_version` + `migrate_settings`) now, while there are no released users to break.
- **Sentinel-zero settings**: `theilsen_n_subsamples = Setting(0)` and `ransac_residual_threshold = Setting(0.0)` / `ransac_min_samples = Setting(0)` presumably mean "auto/None". Verify the mapping code converts 0 → `None` before passing to sklearn (a literal `n_subsamples=0` or `residual_threshold=0.0` produces errors or degenerate fits). Add unit tests in `tests/test_learners.py` for the zero/auto path.
- **`max_skips=float("inf")` etc. in `RANSACLearner.__init__`**: these are stored via `self.params = vars()` and passed to sklearn; confirm current sklearn (>=1.2 through latest) still accepts `inf` for `max_skips`/`stop_n_inliers` — pin a CI job against the newest sklearn to catch API drift (RANSAC's `estimator` kwarg already changed names once in sklearn history).
- **Huber `max_iter` mismatch**: learner default is 100, widget Setting is 200 — harmless but confusing; align them.

## Improvements

- **Roadmap items worth doing next** (from ROADMAP.md "Candidate Robust Methods"): a Winsorize/Clip Outliers preprocessing widget and Median/MAD outlier scores are cheap, teach well, and fit the add-on's scope. Siegel repeated-median likely isn't worth it (no maintained sklearn implementation).
- **Expose the RANSAC inlier mask more prominently**: it's already in the annotated output when available; consider a dedicated "Inliers"/"Outliers" data output pair so students can wire it straight into a Scatter Plot.
- **`OWBaseWidget` vs `OWWidget`**: the widget subclasses `OWBaseWidget` directly; Orange's `OWWidget` gives report support ("Send Report") and summary bars for free. Worth switching unless there was a deliberate reason (dependency slimming).
- **Coefficient table**: add a standardized-coefficient column when robust scaling is on, so magnitudes are comparable — a common student confusion.

## Testing

- Tests exist for learners, preprocess, package metadata, and widget imports — good. Gaps:
  - No test of the widget's parameter plumbing (e.g. that changing `huber_epsilon` in the GUI actually changes the fitted model). Use `orangewidget.tests.base.WidgetTest`.
  - No test of the `bad_target` error path (discrete/no target).
  - Add a matrix cell in `tests.yml` against sklearn latest and Orange3 latest, plus the oldest supported pins (`Orange3>=3.39`, `scikit-learn>=1.2`), to catch drift in both directions.

## Documentation

- README and `docs/installing-in-orange.md` are in good shape with screenshots. Add:
  - A short "Which method should I choose?" table (breakdown point, speed, when Huber vs RANSAC vs Theil-Sen) — this is the pedagogical core for COMP2200.
  - The demo workflow files (`.ows`) referenced by commit 5be9d48 should be linked from the README so students can download them directly.
- DEVELOPMENT.md's venv/pip instructions work, but see Housekeeping below re: uv.

## Security

- No secrets or credentials found in the repo. `publish.yml` exists — verify it uses PyPI **Trusted Publishing** (OIDC) rather than a long-lived `PYPI_API_TOKEN` secret; migrate if not.

## Housekeeping / Modernization

- **Adopt uv for development**: replace the venv/pip instructions in DEVELOPMENT.md with `uv sync` / `uv run pytest` / `uv run -m Orange.canvas`, and manage dev deps via `uv add --dev` (checking in `uv.lock`). No requirements.txt exists — keep it that way; pyproject.toml stays the single source of truth.
- **Ship the release**: ROADMAP's "Publish a PyPI release before requesting inclusion in the official Orange add-ons list" appears imminent (recent commits: "Prepare robust add-on for PyPI release"). Tag v0.1.0, publish, then submit to the Orange add-ons list — that's the highest-value single action remaining.
- Update ROADMAP.md "Implemented" section: LAD/Quantile Regression is implemented but still listed under "Candidate Robust Methods" (Quantile Regression) and missing from the Implemented widget list, which says only "Huber, RANSAC, and Theil-Sen".
- Add a `CHANGELOG.md` before the first PyPI release.
- Consider adding `ruff` (lint + format) to CI; the codebase is small enough to adopt it painlessly now.

## Quick Wins

1. Fix the Theil-Sen hyphen/en-dash inconsistency and add settings migration.
2. Align Huber `max_iter` default (100 vs 200).
3. Update ROADMAP.md to reflect LAD being implemented.
4. Link demo `.ows` workflows from README.
5. `uv`-ify DEVELOPMENT.md instructions.
