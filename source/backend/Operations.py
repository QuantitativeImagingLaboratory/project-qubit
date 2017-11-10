import numpy as np
import config
import cv2
import logging
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

__all__ = ['Operations']

class Operations:

    def __init__(self):
        logging.info('init')


    def apply_filter(self, parameters):
        logging.info('apply filter function')
        filter = self.create_filter(parameters)

        image = cv2.imread(parameters['image_path'])
        dft = np.fft.fft2(parameters)

        # Needs to be completed


    def create_filter(self, parameters):
        print(parameters)
        f = parameters['filter_name']
        return f(params = parameters)