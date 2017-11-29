import numpy as np
import config
import cv2
import time
import logging
from backend import Filters, StatisticalFilters
from matplotlib import pyplot as plt
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

__all__ = ['Operations']

class Operations:

    def __init__(self):
        logging.info('init')


    def parse_request_json(self, json_dict):

        return

    def post_process_image(self, image):
        # Full contrast stretch
        a = np.min(image)
        b = np.max(image)
        k = 255
        image = (image - a) * (k / (b - a))
        avg = np.average(image)
        return (image if avg > 50 else 255 - image).astype('uint8')


    def apply_filter(self, req_parameters):

        print('============')
        print(req_parameters)
        print('============')
        if 'filter_name' not in req_parameters['settings']:
            req_parameters['settings']['filter_name'] = req_parameters['settings']['filter_type']

        input_image = cv2.imread(config.UPLOADED_IMAGE_FILE_PATH, 0)
        image_shape = input_image.shape
        print(image_shape, ' >> image shape')

        image_name = str(time.time()) + '.jpg'
        input_params = {}
        input_params['method'] = req_parameters['method']
        input_params['filter_shape'] = image_shape
        for k, v in req_parameters['settings'].items():
            input_params[k] = v
        input_params['image_name'] = image_name

        if req_parameters['method'] == 'statistical':
            input_params['image'] = input_image
            input_params['window'] = (input_params['window'], input_params['window'])
            input_params['filt_func'] = Filters.__getattribute__(input_params['filter_name'])
            result_image = StatisticalFilters.convolve(input_params)
        else:

            logging.info('apply filter function')

            # 1 FFT
            fft_image = np.fft.fft2(input_image)  # nunpy
            # 2 shift the fft to center
            fft_shift = np.fft.fftshift(fft_image)

            input_params['image_dft'] = fft_shift

            # input_params['spectrum_noise_orgimg'] = 0.0001
            filter = self.create_filter(input_params)
            cv2.imwrite('data/mask_'+input_params['image_name'], filter)

            denoise_dft = fft_shift * filter

            # plt.imshow(denoise_dft.real)
            # plt.show()

            # Get image back
            f_ishift = np.fft.ifftshift(denoise_dft)
            img_back = np.fft.ifft2(f_ishift).real
            result_image = self.post_process_image(img_back)

        cv2.imwrite('data/'+ image_name, result_image)

        # Needs to be completed
        logging.info("COMPLETED")

        return image_name

    def create_filter(self, parameters):
        filter_function = Filters.__getattribute__(parameters['filter_name'])
        return filter_function(parameters)

#
# op = Operations()
#
# op.apply_filter({'settings': {"filter": "BR",
# 		"filter_name": "BR_IDEAL_FILTER",
# 		"width": 3,
# 		"order": 1,
# 		"cutoff": 74,
# 		"notch_centerbox": 0,
# 		"notch_sd": 0,
# 		"invfilter_k": 0,
# 		"wiener_k": 0
# } })