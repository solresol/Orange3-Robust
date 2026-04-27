import numpy as np

from Orange.data import Domain
from Orange.preprocess import Preprocess
from Orange.preprocess.transformation import Normalizer


class RobustScale(Preprocess):
    """Scale continuous features by median and interquartile range."""

    def __init__(
        self,
        with_centering=True,
        with_scaling=True,
        quantile_range=(25.0, 75.0),
        transform_class=False,
    ):
        self.with_centering = with_centering
        self.with_scaling = with_scaling
        self.quantile_range = tuple(quantile_range)
        self.transform_class = transform_class

    def __call__(self, data):
        def transform(var):
            if not var.is_continuous:
                return var

            values = np.asarray(data.get_column(var), dtype=float)
            values = values[np.isfinite(values)]

            center = float(np.median(values)) if self.with_centering and values.size else 0.0

            if self.with_scaling and values.size:
                q_min, q_max = np.percentile(values, self.quantile_range)
                scale = float(q_max - q_min)
                if not np.isfinite(scale) or abs(scale) < 1e-15:
                    scale = 1.0
            else:
                scale = 1.0

            return var.copy(compute_value=Normalizer(var, center, 1.0 / scale))

        attributes = [transform(var) for var in data.domain.attributes]
        if self.transform_class:
            class_vars = [transform(var) for var in data.domain.class_vars]
        else:
            class_vars = data.domain.class_vars

        domain = Domain(attributes, class_vars, data.domain.metas)
        return data.transform(domain)
