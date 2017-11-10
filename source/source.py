from flask import Flask
import config
import logging
from backend import Operations

logging.basicConfig(level=config.logging_level, format='%(levelname)s - %(message)s')

app = Flask(__name__)

operations = Operations.Operations()

@app.route('/')
def hello_world():
    return 'Hello World!'


def process_image():
    return 0

if __name__ == '__main__':
    app.run()
