# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, ALL,DEFAULTS,patch_request_class
from flask import send_from_directory,render_template
from flask import send_file, make_response

app = Flask(__name__)
app.config['UPLOADED_FRA_DEST'] = 'TestFolder/upload'  # 上传文件储存地址
app.config['DOWNLOADED_FRA_DEST'] = 'TestFolder/download'  # 下载文件储存地址

fra = UploadSet('fra', ALL)
configure_uploads(app, fra)
patch_request_class(app)  # 文件大小限制，默认为16MB


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'allfiles' in request.files:
        filename = fra.save(request.files['allfiles'], get_text())
        file_url = fra.url(filename)
        return render_template('upload.html') + '<p>file name :' + filename + '</p> ' + '<p>file url :' + file_url + '</p>'
    return render_template('upload.html')

def get_text():
    subfolderpath = request.form['subfolderpath']
    return subfolderpath


@app.route('/download/<path:filename>',methods=['GET', 'POST'])
def download_file(filename):

    return send_from_directory(app.config['DOWNLOADED_FRA_DEST'],filename,as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)