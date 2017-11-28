import numpy as np
import config
import logging

logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')


def band_reject_ideal_filter(params):
    """

    :param params: shape, cutoff, width
    :return:
    """
    shape = params['filter_shape']
    cutoff = params['cutoff']
    width = params['width']

    mask = np.ones(params['filter_shape'])*255
    rows = shape[0]
    cols = shape[1]

    for u in range(rows):
        for v in range(cols):
            duv = ((u - (rows / 2)) ** 2 + (v - (cols / 2)) ** 2) ** (1 / 2)
            if (cutoff - width / 2) <= duv and duv <= (cutoff + width / 2):
                mask[u][v] = 0

    return mask


def band_reject_gaussian_filter(params):
    """

    :param params: shape, cutoff, width
    :return:
    """
    shape = params['filter_shape']
    cutoff = params['cutoff']
    width = params['width']

    mask = np.zeros(params['filter_shape'])
    rows = shape[0]
    cols = shape[1]

    for u in range(rows):
        for v in range(cols):
            duv = ((u - (rows / 2)) ** 2 + (v - (cols / 2)) ** 2) ** (1 / 2)
            if duv != 0:
                mask[u][v] = 1 - np.e ** (-((duv ** 2 - cutoff ** 2) / (duv * width)) ** 2)
            else:
                mask[u][v] = 1 - np.e ** (-((duv ** 2 - cutoff ** 2) / (width)) ** 2)
    return mask


def band_reject_butterworth_filter(params):
    """

    :param params: shape, cutoff, width, order
    :return:
    """
    shape = params['filter_shape']
    cutoff = params['cutoff']
    width = params['width']
    order = params['order']

    mask = np.ones(params['filter_shape']) * 255
    rows = shape[0]
    cols = shape[1]

    for u in range(rows):
        for v in range(cols):
            duv = ((u - (rows / 2)) ** 2 + (v - (cols / 2)) ** 2) ** (1 / 2)
            if (duv ** 2 - cutoff ** 2) != 0:
                mask[u][v] = 1 / (1 + (duv * width / (duv ** 2 - cutoff ** 2)) ** (2 * order))
            else:
                mask[u][v] = 1 / (1 + (duv * width) ** (2 * order))
    return mask


def notch_ideal_filter(params, notch_list):
    """

    :param params: shape, notch_size, cutoff, notch_list
    :return:
    """
    image_shape = params['filter_shape']
    notch_size = 2 #params['notch_size']
    cutoff = 4 #params['cutoff']

    mask = np.ones(params['filter_shape']) * 255
    rows = image_shape[0]
    cols = image_shape[1]
    for notch_center in notch_list:
        x = notch_center[0]
        y = notch_center[1]

        for u in range(int(x - (notch_size / 2)), int(x + (notch_size / 2))):
            for v in range(int(y - (notch_size / 2)), int(y + (notch_size / 2))):
                duv = ((u - x) ** 2 + (v - y) ** 2) ** (1 / 2)
                if duv <= cutoff:
                    if u > -1 and v > -1 and u < rows and v < cols:
                        mask[u][v] = 0
    return mask


def notch_gaussian_filter(params,notch_list):
    """

    :param params:
    :return:
    """
    image_shape = params['filter_shape']
    notch_size = 2 #params['notch_size']
    cutoff = 4 #params['cutoff']

    mask = np.ones(params['filter_shape']) * 255
    rows = image_shape[0]
    cols = image_shape[1]
    for notch_center in notch_list:
        x = notch_center[0]
        y = notch_center[1]

        for u in range(int(x - (notch_size / 2)), int(x + (notch_size / 2))):
            for v in range(int(y - (notch_size / 2)), int(y + (notch_size / 2))):
                duv = ((u - (rows / 2)) ** 2 + (v - (cols / 2)) ** 2) ** (1 / 2)
                if u > -1 and v > -1 and u < rows and v < cols:
                    mask[u][v] = 1 - np.e ** (-duv ** 2 / (2 * cutoff ** 2))
    return mask


def notch_butterworth_ideal_filter(params, notch_list):
    """
    :param params:
    :return:
    """
    image_shape = params['filter_shape']
    notch_size = params['notch_size']
    cutoff = params['cutoff']
    order = params['order']

    mask = np.ones(params['filter_shape']) * 255
    rows = image_shape[0]
    cols = image_shape[1]
    for notch_center in notch_list:
        x = notch_center[0]
        y = notch_center[1]

        for u in range(int(x - (notch_size / 2)), int(x + (notch_size / 2))):
            for v in range(int(y - (notch_size / 2)), int(y + (notch_size / 2))):
                duv = ((u - x) ** 2 + (v - y) ** 2) ** (1 / 2)
                if u > -1 and v > -1 and u < rows and v < cols:
                    if (duv > 0):
                        mask[u][v] = 1 / (1 + (cutoff / duv) ** (2 * order))
                    else:
                        mask[u][v] = 1 / (1 + (cutoff) ** (2 * order))
    return mask

def dft_centerbox(rows, cols, u, v, innerbox=10):
    h = rows / 2
    w = cols / 2
    return h - innerbox < u and u < h + innerbox and w - innerbox < v and v < w + innerbox

def getNotchLocation(binary_image, innerbox):
    shape = binary_image.shape
    rows = shape[0]
    cols = shape[1]
    notchlist = []

    for u in range(rows):
        for v in range(cols):
            if binary_image[u][v] == 0 and not dft_centerbox(rows, cols, u, v, innerbox):
                notchlist.append([u, v])
    print(len(notchlist))
    return notchlist

def find_threshold(dft_img,order):
    mean = int(np.mean(dft_img))
    std = int(np.std(dft_img))
    return mean + std*order

def binarize(image, std):
    threshold = find_threshold(image,std)
    bin_img = image.copy()
    org_height, org_width = bin_img.shape[:2]

    for i in range(org_height):
        for j in range(org_width):
            if (image[i][j] > threshold):
                bin_img[i][j] = 0
            else:
                bin_img[i][j] = 255
    return bin_img

def notch_filter(params):
    """
        :param params: dft of image , type of notch, diviation number,
        :return:
    """
    type = params['type']

    #Generate binary image
    fft_mag = np.log(np.abs(params['image_dft']))
    fft_mag = (255 * (fft_mag / np.max(fft_mag))).astype('uint8')
    binaryimg = binarize(fft_mag, params['std_num'])

    #get notch location
    notch_list = getNotchLocation(binaryimg, params['center_box'])

    if type == 'gaussian':
        return notch_gaussian_filter(params, notch_list)
    elif type == 'butterworth':
        return notch_butterworth_ideal_filter(params, notch_list)
    else:
        return notch_ideal_filter(params, notch_list)

def gen_ring_noise_mask (dft_img, cutoff, width = 1):
    shape = dft_img.shape
    rows = shape[0]
    cols = shape[1]
    noisyimg = np.ones(shape)

    print(cutoff)
    for u in range(rows):
        for v in range(cols):
            duv = ((u - (rows/2))**2 + (v - (cols/2))**2)**(1/2)
            if (cutoff - width/2) <= duv and duv <= (cutoff + width/2) and np.random.randint(50)==1:
                noisyimg[u][v] = 255
    return noisyimg

def generate_noise(params):
    noise_mask = gen_ring_noise_mask(params['image_dft'], np.random.randint(20, 100), 1)
    noisy_dft = params['image_dft'] * noise_mask
    return noisy_dft

def generate_blur(params):
    return params['image_dft'] * degradation_function(params)

def degradation_function(params):
    k = params['k_param']
    shape= params['filter_shape']
    degradation = np.zeros(shape)
    rows = shape[0]
    cols = shape[1]

    for u in range(rows):
        for v in range(cols):
            degradation[u][v] = np.e ** (-k * ((u - rows / 2) ** 2 + (v - cols / 2) ** 2) ** (5 / 6))
    return degradation

def inverse_filter(params):
    filter = params['image_dft'] / degradation_function(params)
    return filter

def inverse_wiener_filter(params):
    """
    :param params:
    :return:
    """
    degradation = degradation_function(params)
    reconstructed = ((1 / degradation) * ((np.conj(degradation) * degradation) / (
    np.conj(degradation) * degradation + params['spectrum_noise_orgimg']))) * params['image_dft']

    return reconstructed
