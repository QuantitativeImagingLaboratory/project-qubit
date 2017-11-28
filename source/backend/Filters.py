from enum import Enum
import config
from backend import StatisticalFilters, PeriodicFilters
import logging
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

# __all__ = ['Filters']


## Statistical Noise Filters

# Mean Filters
MEAN_ARITHMETIC_FILTER = StatisticalFilters.mean_arithmetic_filter
MEAN_GEOMETRIC_FILTER = StatisticalFilters.mean_geometric_filter
MEAN_HARMONIC_FILTER = StatisticalFilters.mean_harmonic_filter
MEAN_CONTRAHARMONIC_FILTER = StatisticalFilters.mean_contraharmonic_filter

# Order Statistic Filters
OS_MEDIAN_FILTER = StatisticalFilters.order_statistic_median_filter
OS_MAX_FILTER = StatisticalFilters.order_statistic_max_filter
OS_MIN_FILTER = StatisticalFilters.order_statistic_min_filter
OS_MIDPOINT_FILTER = StatisticalFilters.order_statistic_midpoint_filter
OS_ALPHA_TRIMMED_FILTER = StatisticalFilters.order_statistic_alpha_trimmed_filter

# Adaptive Filters
ADAPTIVE_FILTER = StatisticalFilters.adaptive_filter

## Periodic Noise Filters

# Band Reject Filters
BR_IDEAL_FILTER = PeriodicFilters.band_reject_ideal_filter
BR_GAUSSIAN_FILTER = PeriodicFilters.band_reject_gaussian_filter
BR_BUTTERWORTH_FILTER = PeriodicFilters.band_reject_butterworth_filter

# Notch Filters
# NOTCH_IDEAL_FILTER = PeriodicFilters.notch_ideal_filter
# NOTCH_GAUSSIAN_FILTER = PeriodicFilters.notch_gaussian_filter
# NOTCH_BUTTERWORTH_FILTER = PeriodicFilters.notch_butterworth_ideal_filter
NOTCH_IDEAL_FILTER = PeriodicFilters.notch_filter
NOTCH_GAUSSIAN_FILTER = PeriodicFilters.notch_filter
NOTCH_BUTTERWORTH_FILTER = PeriodicFilters.notch_filter


# Inverse Filters
INVERSE_FILTER      = PeriodicFilters.inverse_filter
WIENER_FILTER       = PeriodicFilters.inverse_wiener_filter
