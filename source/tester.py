import cv2
import sys
from numpy.random import rand
import numpy as np
from backend import PeriodicFilters as PF


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)

def post_process_image(image):
    # Full contrast stretch
    a = np.min(image)
    b = np.max(image)
    k = 255
    image = (image - a) * (k / (b - a))
    avg = np.average(image)
    return (image if avg > 50 else 255 - image).astype('uint8')


def import_image(image_name):
    input_image = cv2.imread(image_name, 0)
    # display_image("Testing", input_image)
    return input_image

def show_dft(window_name, dft_image):
    fft_mag = np.log(np.abs(dft_image))
    fft_mag  = (255 * (fft_mag  / np.max(fft_mag))).astype('uint8')
    display_image(window_name, fft_mag)


def getDFT(image):
    # 1 FFT
    fft_image = np.fft.fft2(image)  # nunpy
    # fft_image = cv2.dft(np.float32(image),flags = cv2.DFT_COMPLEX_OUTPUT)
    # 2 shift the fft to center
    fft_shift = np.fft.fftshift(fft_image)

    return fft_shift


def getImage(dft_img):
    f_ishift = np.fft.ifftshift(dft_img)
    img_back = np.fft.ifft2(f_ishift).real
    # img_back = np.abs(img_back)

    return img_back

#################Generate Noise
params={}
params['image'] = import_image("data/charlie.jpg")
params['filter_shape'] = params['image'].shape
params['image_dft'] = getDFT(params['image'])
noisy_dft = PF.generate_noise(params)
img_back = getImage(noisy_dft)
img_back = post_process_image(img_back)
# display_image("Original", img_back)

##save noisy image
cv2.imwrite('data/noisy_img.png', img_back)


#################Bandreject Testing
# params={}
# params['image'] = import_image("noisy_img.png")
# params['filter_shape'] = params['image'].shape
#
# params['image_dft'] = getDFT(params['image'])
# params['cutoff'] = 87
# params['width'] = 4
# params['order'] = 2
#
# display_image("Original", params['image'])
#
# #apply the noise remover mask
# denoise_dft = params['image_dft']  * PF.band_reject_gaussian_filter(params)
# show_dft("Denoised DFT", denoise_dft)
#
# #get filtered img
# img_back = getImage(denoise_dft)
# img_back = post_process_image(img_back)
# display_image("Fixed Image", img_back)
# #


##################Notch Testing#####################################
##################### ideal
# params={}
# params['image'] = import_image("noisyimg.png")
# params['type'] = 'ideal' # or 'gaussian'
# params['filter_shape'] = params['image'].shape
#
# params['image_dft'] = getDFT(params['image'])
# params['notch_size'] = 2
# params['cutoff'] = 4
# params['std_num'] = 4
# params['center_box'] = 32
#
# #apply the noise remover mask
# denoise_dft = params['image_dft']  * PF.notch_filter(params)
# show_dft("Denoised DFT", denoise_dft)
#
# #get filtered img
# img_back = getImage(denoise_dft)
# img_back = post_process_image(img_back)
# display_image("Fixed Image", img_back)
##



#######################Butterworth
# params={}
# params['image'] = import_image("img1.tif")
# params['type'] = 'butterworth'
# params['filter_shape'] = params['image'].shape
#
# params['image_dft'] = getDFT(params['image'])
# params['notch_size'] = 2
# params['cutoff'] = 1
# params['std_num'] = 2
# params['order'] = 2
# params['center_box'] = 45
#
# #apply the noise remover mask
# denoise_dft = params['image_dft']  * PF.notch_filter(params)
# show_dft("Denoised DFT", denoise_dft)
#
# #get filtered img
# img_back = getImage(denoise_dft)
# img_back = post_process_image(img_back)
# display_image("Fixed Image", img_back)
###

#########################Inverse Filters
###Generate Gaussian blur
# params={}
# params['image'] = import_image("img5.tif")
# params['filter_shape'] = params['image'].shape
# params['image_dft'] = getDFT(params['image'])
# params['k_param'] = 0.0025
#
# blurimg = PF.generate_blur(params)
#
# img_back = getImage(blurimg)
# img_back = post_process_image(img_back)
# display_image("Blur img", img_back)
# cv2.imwrite("blurimg.png", img_back)
#
# ####Only Inverse
# params={}
# params['image'] = import_image("blurimg.png")
# params['filter_shape'] = params['image'].shape
# params['image_dft'] = getDFT(params['image'])
# params['k_param'] = 0.0025
#
# denoised_img = PF.inverse_filter(params)
#
# img_back = getImage(denoised_img)
# img_back = post_process_image(img_back)
# display_image("Inverse filtering", img_back)
#
#
#
# ####Winer Inverser Filter
# params = {}
# params['image'] = import_image("blurimg.png")
# params['filter_shape'] = params['image'].shape
# params['image_dft'] = getDFT(params['image'])
# params['k_param'] = 0.0025
# params['spectrum_noise_orgimg'] = 0.0001
#
# reconstructed = PF.inverse_wiener_filter(params)
#
# back = getImage(reconstructed)
# back = post_process_image(back)
# display_image("Winer filtering", back)