import os
import config
import logging
import utilities as webutils
from backend import PeriodicFilters
from backend import Filters
from backend.Operations import Operations
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')
import cv2
from flask import Flask
from flask import render_template, request, redirect, send_from_directory
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.DATA_PATH

current_image = ''


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
        file.save(config.UPLOADED_IMAGE_FILE_PATH)
        return render_template('image.html', source=filename)


@app.route('/render/<filename>')
def send_image(filename):
    return send_from_directory('data/', filename)


@app.route('/display', methods=['POST', 'GET'])
def change_display():
    if current_image == '':
        return redirect(request.url)

    if request.json['display'] != 'filtered':
        filename = '{}_{}'.format(request.json['display'], current_image)
    else:
        filename = current_image

    if not os.path.isfile(os.path.join(config.DATA_PATH, filename)):
        return render_template('image.html', source='not_available.png')
    return render_template('image.html', source=filename)


@app.route('/apply', methods=['POST'])
def apply_filter():
    image_path = process_image(request.json)
    global current_image
    current_image = image_path
    return render_template('image.html', source=image_path)


def process_image(json_dict):
    op = Operations()

    # op.apply_filter({'filter_name': Filters.MEAN_ARITHMETIC_FILTER,
    #                  'filter_shape': (5, 4),
    #                  'high_pass': True
    #                  })

    return op.apply_filter(json_dict)


if __name__ == "__main__":
    app.run(port=5009, debug=True)
    # process_image()