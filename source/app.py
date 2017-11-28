import os
import config
import logging
import utilities as webutils
from backend.Filters import Filters
from backend.Operations import Operations
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

from flask import Flask
from flask import render_template, request, redirect, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.DATA_PATH


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file and webutils.allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('image.html', source=filename)


@app.route('/render/<filename>')
def send_image(filename):
    return send_from_directory('data/', filename)


@app.route('/apply', methods=['POST'])
def apply_filter():
    print(request.json)

    # # The display choice: 'filtered', 'dft', 'mask', 'histogram'
    # display = request.json['display']
    #
    # # The filter name: 'bandreject', 'notch', 'invfilter', 'wiener'
    # filter = request.json['filter']
    #
    # # The settings for each filter
    # # for bandreject: {'type': 'gaussian', 'thickness': '1', 'radius': '1'}
    # # for notch: {'type': 'ideal'}
    # # else: {}
    # filter_settings = request.json['filter_settings']


    """
    TODO: 1) call a backend function to apply filters
          2) then generate an image in the data folder
          3) send the name of the image instead of Lenna.png below
    """

    return render_template('image.html', source='Lenna.png')


def process_image():
    op = Operations()
    op.apply_filter({'filter_name': Filters.MEAN_ARITHMETIC_FILTER,
                     'filter_shape': (5, 4),
                     'high_pass': True
                     })

    return None


if __name__ == "__main__":
    app.run(port=8805, debug=True)
    # process_image()