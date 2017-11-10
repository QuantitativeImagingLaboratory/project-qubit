import numpy as np
import config
import logging
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

__all__ = ['Operations']

class Operations:

    def __init__(self):
        logging.info('init')


    def apply_filter(self, parameters):
        logging.info('apply filter function')
        filter = self.create_filter(parameters)

        dft = np.fft.fft2(parameters)

        # Needs to be completed


    def create_filter(self, parameters):
        print(parameters)
        f = parameters['filter_name']
        return f(params = parameters)