from flask import Flask, render_template, request, redirect, flash, url_for
from flask import jsonify

import os
import video

# creates flask instance
app = Flask(__name__)

filters = []
filters_applied = False

# default home page 
@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template('project_template.html')

# api call/route for uploading videos
@app.route("/uploadvideo", methods=['GET, POST'])
def upload_video():

    # checks if an uploaded video file already exists
    if(len(os.listdir("static//videos"))) > 0:
        return jsonify(
            message='Video Already Uploaded',
        )

    # makes sure that the user actually provided a file
    if 'file' not in request.files:
        return jsonify(
            message='No file part in the request',
        )

    # gets file from the request and checks that it has a name
    file = request.files['file']
    if file.filename == '':
         return jsonify(
            message='No file selected',
        )
    
    # checks if file is mp4 file
    if (not file.filename.endswith('.mp4')):
        return jsonify(
            message='File Not MP4 Format',
        )
    
    # saves the file to the local server folder in the statics folder
    file.save("static//videos//video.mp4")
    
    return jsonify(
            message='Video Sucessfully Uploaded',
        )

# api call/route for deleting the video on the server
@app.route("/deletevideo", methods=['POST'])
def delete_video():

    # checks if the video file actually exists
    if os.path.exists("videos//video.mp4"):

        # delete the file
        os.remove("static//videos//video.mp4")
        return redirect('/')
    
    flash('No file found to delete')
    return redirect('/')

# api call/route for configuring the filters into a global variable
# that lasts while the python server is running
@app.route("/configurefilters", methods=['POST'])
def configure_filters():

    # global word allows to be used outside of this function
    global filters
    # converts filters to python dictionary
    filters = request.form.getlist('filter')

    for filter in filters:
       print(filter)
    
    return redirect('/')

# api call/route for applying the filters stored in the global variable
@app.route("/applyfilters", methods=['GET'])
def applyfilters():

    # checks that there is a video to apply the filters to
    if(not os.path.exists("static//videos//video.mp4")):
        return jsonify(
        message="No video exists",
        )

    # checks that 
    if(len(filters) == 0):
        return jsonify(
        message="No filters were configured",
        )

    # iterates over the list of filters and applies them
    for filter in filters:
        if('grayscale:' in filter):
            video.greyScaleVideo()

    global filters_applied
    filters_applied = True

    return jsonify(
        message="Filters Applied Sucessfully",
    )

# api call / route for starting to stream the video
@app.route("/startstreaming", methods=['GET'])
def startstreaming():
    
    # returns json saying wether video can procede to play
    return jsonify(
        canPlay=filters_applied,
    )

# Purpose
# starts python flask web server 
def start_server():
    app.run("0.0.0.0", port=80, debug=True)

