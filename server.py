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

    if(len(os.listdir("video"))) > 0:
        flash('Video Already Uploaded')
        return redirect('/')

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
    
    file.save("video//video.mp4")
    
    print(file.filename)
    return redirect('/')

@app.route("/deletevideo", methods=['POST'])
def delete_video():

    print("test")

    if os.path.exists("video//video.mp4"):
        os.remove("video//video.mp4")
        return redirect('/')
    
    flash('No file found to delete')
    return redirect('/')


def start_server():
    app.run("0.0.0.0", port=80, debug=True)

