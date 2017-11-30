import config
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
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


def add_noise_to_image(image, noise_type, gauss_mean=50, gauss_sigma = 20, sp_amount=0.04, salt_pepper_ratio=0.5):
    """
    Followed code from
    https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
    :param image:
    :param noise_type:

    1: gaussian
    2: poisson
    3: salt and pepper
    4: speckle
    :return:
    """
    noisy_image = image.copy()
    if noise_type == 1:
        noise_vals = np.random.randn(image.shape[0], image.shape[1]) * gauss_sigma
        for i in range(2):
            noisy_image[:, :, i] =  noisy_image[:, :, i] + noise_vals

    elif noise_type == 2:
        noisy_image = image.copy()

        # Add salt
        salt_vals = np.ceil(sp_amount * image.size * salt_pepper_ratio)
        placing_points = [np.random.randint(0, i-1, int(salt_vals)) for i in image.shape]
        noisy_image[placing_points] =  1

        # Add pepper
        pepper_vals = np.ceil(sp_amount * image.size * (1.0 - salt_pepper_ratio))
        placing_points = [np.random.randint(0, i - 1, int(pepper_vals)) for i in image.shape]
        noisy_image[placing_points] = 0
        noisy_image = noisy_image

    elif noise_type == 3:
        unique_vals = len(np.unique(image))
        unique_vals = 2 ** np.ceil(np.log2(unique_vals))
        noisy_image = np.random.poisson(image * unique_vals) / float(unique_vals)

    else:
        h, w, ch = image.shape
        noise_vals = np.random.randn(h, w, ch)
        noisy_image = image+ image * noise_vals.reshape(image.shape)

    # for i in range(0, 2):
    #     noisy_image[:, :, i] = (noisy_image[:,:,i] / np.max(noisy_image[:,:,i]) ) * 255
    return  noisy_image


def compute_and_save_histogram(image1, image2, filename):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)

    ax1.hist(image1.ravel(), bins=256, fc='k', ec='k')
    ax1.set_title('Before')

    ax2.hist(image2.ravel(), bins=256, fc='k', ec='k')
    ax2.set_title('After')

    fig.savefig(filename)


def post_process_image(image):
    """Post process the image to create a full contrast stretch of the image
    takes as input:
    image: the image obtained from the inverse fourier transform
    return an image with full contrast stretch
    -----------------------------------------------------
    1. Full contrast stretch (fsimage)
    2. take negative (255 - fsimage)
    """
    fcs_image = np.array(image, dtype=np.uint8)
    hist = [0 for i in range(256)]
    for i in fcs_image:
        for j in i:
            hist[j] += 1

    K = 255
    A = 0
    B = 255

    for i in range(256):
        if hist[i] > 0:
            A = i
            break

    for i in range(255, -1, -1):
        if hist[i] > 0:
            B = i
            break

    stretched_image = np.zeros(fcs_image.shape)
    for i in range(stretched_image.shape[0]):
        for j in range(stretched_image.shape[1]):
            stretched_image[i, j] = round(((K - 1) / (B - A)) * (fcs_image[i, j] - A + 0.5))

    return stretched_image

# img2 = cv2.imread('data/board_gaussian.tif', 0)
# mean, variance = estimate_params(img2)
# print(mean, variance)
#
# img2 = cv2.imread('data/board_pepper.tif', 0)
# mean, variance = estimate_params(img2)
# print(mean, variance)
#


# img = cv2.imread('data/pattern1.tif', 0)
# img2 = cv2.imread('data/pattern1_gn.tif', 0)
# if len(img.shape) == 3:
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
# noisy_image = add_noise_to_image(img, 1, gauss_sigma=40)
# plt.imshow(noisy_image)
# plt.show()

# compute_and_save_histogram(img, img2, 'as.png')