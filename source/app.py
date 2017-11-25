import os
import config
import logging
from backend.Filters import Filters
from backend.Operations import Operations
logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

from flask import Flask
from flask import render_template, request, redirect, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_PATH


@app.route("/")
def main():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('image.html', source=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('data/uploads/', filename)


def process_image():
    op = Operations()
    op.apply_filter({'filter_name': Filters.MEAN_ARITHMETIC_FILTER,
                     'filter_shape': (5, 4),
                     'high_pass': True
                     })

    return None


if __name__ == "__main__":
    app.run(port=4321, debug=True)
    # process_image()