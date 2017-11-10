import numpy as np
import config
import logging
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')


def mean_arithmetic_filter(params):
    """
    Creates and returns a mean arithmetic filter
    :param params:
    :return:
    """

    filter = np.zeros(params['filter_shape'])

    logging.info(filter)

    if params['high_pass']:
        return 1 - filter
    return filter


def mean_geometric_filter(params):
    """
    Creates and returns a mean geometric filter
    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def mean_harmonic_filter(params):
    """
    Creates and returns a mean harmonic filter
    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def mean_contraharmonic_filter(params):
    """
    Creates and returns a mean contraharmonic filter
    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def order_statistic_median_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def order_statistic_max_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def order_statistic_min_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def order_statistic_midpoint_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def order_statistic_alpha_trimmed_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def adaptive_filter(params):
    """

    :param params:
    :return:
    """

    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter
