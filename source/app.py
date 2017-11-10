import config
import logging
from backend.Filters import Filters
from backend.Operations import Operations
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

from flask import Flask
app = Flask(__name__)


@app.route("/")
def main():
    return "Image Restoration Project"


def process_image():
    op = Operations()
    op.apply_filter({'filter_name': Filters.MEAN_ARITHMETIC_FILTER,
                     'filter_shape': (5, 4),
                     'high_pass': True
                     })

    return None


if __name__ == "__main__":
    # app.run()
    process_image()