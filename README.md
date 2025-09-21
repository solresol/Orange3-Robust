# Orange3-Robust
Robust regressors plug-in for Orange

# Testing locally

pip install -e .
orange-canvas

# To-do 


orangecontrib/robust/widgets/__init__.py should define the category ICON, BACKGROUND, and WIDGET_HELP_PATH; Orange uses these when it registers your orange.widgets entry point and when users press F1. 

There are some notes at the end of orangecontrib/robust/widgets/owrobustregression.py

# Getting on to the official add-ons list

Orange’s Add‑ons dialog is curated. The list the Canvas shows comes from a file generated in biolab/orange3-addons (they fetch PyPI metadata and serve a compiled list at https://orange.biolab.si/addons/list). To be included:
	•	Ensure your package is on PyPI and installs cleanly.
	•	Open a PR adding your package name to OFFICIAL_ADDONS.txt in that repo. The maintainers review and regenerate the list.  ￼


# Behavioural notes & defaults (avoid foot‑guns)

	•	Theil–Sen can be slow on large n_samples unless you set n_subsamples or keep max_subpopulation modest. Consider exposing both and defaulting max_subpopulation=10_000.  ￼
	•	Huber: expose epsilon and alpha; explain that smaller epsilon ⇒ more aggressive outlier handling. Encourage scaling (toggle).  ￼
	•	RANSAC: leave residual_threshold=None by default so it uses MAD(y); surface min_samples, max_trials, and stop_probability. Consider a small note/warning in the GUI when too few inliers are found.  ￼

# How to

	•	Base your code on the Example Add‑on docs/tutorial (entry points, help, and the widget boilerplate are exactly as described there).  ￼
                  -> https://orange3-example-addon.readthedocs.io/en/latest/
	•	For the widget framework, the Orange Widget Base tutorial shows how to define inputs/outputs and create the left‑hand controls.  ￼
                  -> https://orange-widget-base.readthedocs.io/en/stable/tutorial.html

