from flask import Flask
import logging
from logging.config import dictConfig
import os
from flask import Blueprint, current_app, flash, redirect, request, render_template, send_file, send_from_directory
# import tabula
from werkzeug.utils import secure_filename

import tabula


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

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

bp = Blueprint("tableetl", __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def setup_file_logging():
    logging.config.dictConfig(yaml.load(open('logging.conf')))
    logfile = logging.getLogger()
    logfile.debug("<<setup_file_logging")


app = Flask(__name__)
app.logger.basicConfig(filename='debug.log', level=app.logger.DEBUG)
app.logger.basicConfig(filename='info.log', level=app.logger.INFO)
setup_file_logging()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            app.logger.info("file.filename")
            input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_file_path = os.path.join(UPLOAD_FOLDER, 'output.csv')
            file.save(input_file_path)
            tabula.convert_into(input_file_path, output_file_path, output_format="csv", pages='all')
            return send_file(output_file_path, as_attachment=True)
        flash('只能上传 pdf 文件')
        return redirect(request.url)

    return render_template("tableetl/index.html")
