import os
import inspect
import logging

logging_level = logging.INFO

############################################################
## Directories

# Gets the working directory path
ROOT_DIR = os.path.abspath(inspect.getfile(inspect.currentframe()))
ROOT_DIR = '/'.join(ROOT_DIR.split('/')[:-2]) + '/'
print(ROOT_DIR)

# Directory for images and other data
DATA_PATH = ROOT_DIR + 'source/data/'

# Directory where the uploaded images are going to be saved
UPLOAD_PATH = DATA_PATH + 'uploads/'

############################################################
## Extensions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
