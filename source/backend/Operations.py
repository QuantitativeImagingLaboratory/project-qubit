import numpy as np
import config
import cv2
import logging
from backend import Filters
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

        input_image = cv2.imread(config.UPLOADED_IMAGE_FILE_PATH)
        image_shape = input_image.shape
        print(image_shape, ' >> image shape')

        input_params = {}
        input_params['filter_shape'] = image_shape
        for k, v in req_parameters['settings'].items():
            input_params[k] = v

        print('>>>', input_params)

        filter = self.create_filter(input_params)

        logging.info('apply filter function')

        # 1 FFT
        fft_image = np.fft.fft2(input_image)  # nunpy
        # 2 shift the fft to center
        fft_shift = np.fft.fftshift(fft_image)
        denoise_dft = fft_shift * filter

        # Get image back
        f_ishift = np.fft.ifftshift(denoise_dft)
        img_back = np.fft.ifft2(f_ishift).real
        img_back = self.post_process_image(img_back)
        cv2.imwrite(config.RESULT_IMAGE_FILE_PATH, img_back)

        # Needs to be completed
        logging.info("COMPLETED")

    def create_filter(self, parameters):
        filter_function = Filters.__getattribute__(parameters['filter_name'])

        return filter_function(parameters)