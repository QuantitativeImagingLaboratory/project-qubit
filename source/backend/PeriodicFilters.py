import numpy as np
import config
import logging

logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')


def band_reject_ideal_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def band_reject_gaussian_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def band_reject_butterworth_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def notch_ideal_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def notch_gaussian_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def notch_butterworth_ideal_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter


def inverse_wiener_filter(params):
    """

    :param params:
    :return:
    """
    filter = np.zeros(params['filter_shape'])

    if params['high_pass']:
        return 1 - filter
    return filter
