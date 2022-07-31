import os
from flask import Blueprint, current_app, flash, redirect, request, render_template, send_file, send_from_directory
# import tabula
from werkzeug.utils import secure_filename

import tabula

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

bp = Blueprint("tableetl", __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import Flask
app = Flask(__name__)

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
            # filename = secure_filename(file.filename)
            input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_file_path = os.path.join(UPLOAD_FOLDER, 'output.csv')
            file.save(input_file_path)
            dfs = tabula.read_pdf(input_file_path, pages='all')
            tabula.convert_into(input_file_path, output_file_path, output_format="csv", pages='all')
            uploads = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            # tabula.convert_into("test.pdf", "output.csv", output_format="csv", pages='all')
            # return send_from_directory(directory=uploads, path='output.csv')
            return send_file(output_file_path, as_attachment=True)
        flash('只能上传 pdf 文件')
        return redirect(request.url)
        
    return render_template("tableetl/index.html")