import config
import cv2
import numpy as np
from matplotlib import pyplot as plt


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def estimate_params(image_matrix):
    """
    Takes the 30% of the image from the center as strip
    calculates mean and variance to return.
    :param image_matrix:
    :return:
    """
    width, height = np.shape(image_matrix)
    strip = image_matrix[ int(width*0.35):int(width*0.65), int(height*0.35):int(height*0.65)]

    hist, bins = np.histogram(strip.ravel(), 256, [0, 256])
    # plt.bar(bins[:-1], hist)
    # plt.show()

    # print(hist)

    return np.mean(hist), np.var(hist)


# img2 = cv2.imread('data/board_gaussian.tif', 0)
# mean, variance = estimate_params(img2)
# print(mean, variance)
#
# img2 = cv2.imread('data/board_pepper.tifgit', 0)
# mean, variance = estimate_params(img2)
# print(mean, variance)

