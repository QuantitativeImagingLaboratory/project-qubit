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
    output_image = 'Lenna.png'
    if request.json['method'] == 'statistical':
        output_image = handle_statistical(request.json)
    elif request.json['method'] == 'periodic':
        output_image = handle_periodic(request.json)
    elif request.json['method'] == 'noise':
        output_image = handle_noise(request.json)
    else:
        print("TRY AGAIN: NOT METHOD SPECIFY!")
        return redirect(request.url)

    return render_template('image.html', source=output_image)


# TODO move these functions to the backend
def handle_statistical(json):
    print("handle statistical:", json)
    return "Lenna.png"

def handle_periodic(json):
    print("handle periodic:", json)
    return "Lenna.png"

def handle_noise(json):
    print("handle noise:", json)
    return "Lenna.png"


def process_image():
    op = Operations()
    op.apply_filter({'filter_name': Filters.MEAN_ARITHMETIC_FILTER,
                     'filter_shape': (5, 4),
                     'high_pass': True
                     })

    return None


if __name__ == "__main__":
    app.run(port=8815, debug=True)
    # process_image()