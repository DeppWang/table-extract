import os
from flask import Blueprint, current_app, flash, redirect, request, render_template, send_file

import tabula

UPLOAD_FOLDER = '/home/table-extract/uploads'
ALLOWED_EXTENSIONS = {'pdf','png','jpg'}

bp = Blueprint("index", __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('请选择文件！')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('文件名称不能为空！')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_file_path)
            filename_prefix = file.filename.rsplit('.', 1)[0]
            filename_suffix = file.filename.rsplit('.', 1)[1].lower()
            if filename_suffix != 'pdf':
                tess_cmd = 'sudo tesseract {} {} -l eng pdf'.format(file.filename, filename_prefix)
                os.system(tess_cmd)
            input_file_path = os.path.join(UPLOAD_FOLDER, filename_prefix + '.pdf')
            output_file_path = os.path.join(UPLOAD_FOLDER, filename_prefix + '.csv')
            tabula.convert_into(input_file_path, output_file_path, output_format="csv", pages='all')
            uploads = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            print(uploads)
            return send_file(output_file_path, as_attachment=True)
        flash('只能上传 PDF、PNG、JPG 格式文件！')
        return redirect(request.url)
        
    return render_template("tableetl/index.html")