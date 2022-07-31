from distutils.log import INFO
from flask import Flask
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file_handler']
    }
})

app = Flask(__name__)


@app.route('/')
def index():
    app.logger.info('test info')
    return 'Hello World!'
