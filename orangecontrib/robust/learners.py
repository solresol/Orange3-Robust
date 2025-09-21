import sklearn.linear_model as skl
from Orange.regression import SklLearner

class TheilSenLearner(SklLearner):
    __wraps__ = skl.TheilSenRegressor  # robust to ~29% outliers in 1D
    name = "Theil–Sen"

class HuberLearner(SklLearner):
    __wraps__ = skl.HuberRegressor     # L2 w/ Huber loss (epsilon controls robustness)
    name = "Huber"

class RANSACLearner(SklLearner):
    __wraps__ = skl.RANSACRegressor    # random consensus, inlier mask available
    name = "RANSAC"
