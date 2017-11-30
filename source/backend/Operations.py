from threading import Timer

import numpy as np
import config
import cv2
import time
import os
import logging
from backend import Filters, StatisticalFilters
from utilities import *
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

        logging.info('============')
        logging.info(req_parameters)
        logging.info('============')
        if 'filter_name' not in req_parameters['settings']:
            req_parameters['settings']['filter_name'] = req_parameters['settings']['filter_type']

        input_image = cv2.imread(config.UPLOADED_IMAGE_FILE_PATH, 0)
        image_shape = input_image.shape

        self.image_name = str(time.time()) + '.jpg'
        input_params = {}
        input_params['method'] = req_parameters['method']
        input_params['filter_shape'] = image_shape
        for k, v in req_parameters['settings'].items():
            input_params[k] = v
        input_params['image_name'] = self.image_name

        if req_parameters['method'] == 'statistical':
            input_params['image'] = input_image
            input_params['window'] = (input_params['window'], input_params['window'])
            input_params['window_size'] = (input_params['window'], input_params['window'])
            input_params['min_window_size'] = (3, 3)
            input_params['filt_func'] = Filters.__getattribute__(input_params['filter_name'])
            if input_params['filter_name'] == "ADAPTIVE_MEDIAN_FILTER":
                result_image = StatisticalFilters.adaptive_median_filter(input_params)
            else:
                result_image = StatisticalFilters.convolve(input_params)
        else:

            logging.info('apply filter function')

            # 1 FFT
            fft_image = np.fft.fft2(input_image)  # nunpy

            # 2 shift the fft to center
            fft_shift = np.fft.fftshift(fft_image)

            # Save
            w_dft = np.log(np.abs(fft_shift))
            w_dft = (255 * (w_dft / np.max(w_dft))).astype('uint8')
            cv2.imwrite('data/dft_' + input_params['image_name'], w_dft)

            input_params['image_dft'] = fft_shift

            ## CREATE FILTER
            # input_params['spectrum_noise_orgimg'] = 0.0001
            created_filter = self.create_filter(input_params)
            if np.max(created_filter) <= 1:
                w_filter = 255 * created_filter
            else:
                w_filter = created_filter
            w_filter = np.array(w_filter, dtype=np.uint8)

            # Save
            # with open('data/mask.txt', 'w') as dft_file:
            #     for r in w_filter:
            #         for c in r:
            #             dft_file.write(str(c) + ' ')
            #         dft_file.write('\n')

            cv2.imwrite('data/mask_'+input_params['image_name'], w_filter)

            if 'WIEN' in input_params['filter_name'] or 'INVE' in input_params['filter_name']:
                denoise_dft = created_filter
            else:
                denoise_dft = fft_shift * created_filter

            # Get image back
            f_ishift = np.fft.ifftshift(denoise_dft)
            img_back = np.fft.ifft2(f_ishift).real
            result_image = self.post_process_image(img_back)

        # Save the result image
        cv2.imwrite('data/'+ self.image_name, result_image)

        #Write histograms
        compute_and_save_histogram(input_image, result_image, 'data/hist_' + self.image_name.replace('jpg', 'png'))
        os.rename('data/hist_' + self.image_name.replace('jpg', 'png'), 'data/histogram_' + self.image_name)

        t = Timer(config.FILE_DELETE_TIME, self.delete_generated_files)
        t.start()

        logging.info("COMPLETED")

        return self.image_name

    def create_filter(self, parameters):
        filter_function = Filters.__getattribute__(parameters['filter_name'])
        return filter_function(parameters)

    def delete_generated_files(self):
        os.remove('data/' + self.image_name)
        os.remove('data/histogram_' + self.image_name)
        os.remove('data/mask_' + self.image_name)
        os.remove('data/dft_' + self.image_name)

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