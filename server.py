from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/video/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template('project_template.html')

@app.route("/uploadvideo", methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No file part in the request')
        return redirect('/')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect('/')
    
    if (not file.filename.endswith('.mp4')):
        flash('File Not MP4 Format')
        return redirect('/')
    
    file.save("video//" + file.filename)
    
    print(file.filename)
    return redirect('/')

def start_server():
    app.run("0.0.0.0", port=80, debug=True)

