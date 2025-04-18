import glob
from flask import Flask, render_template, request, flash, abort
from flask import jsonify
from os import access, R_OK
from os.path import isfile

import os
import video

# creates flask instance
app = Flask(__name__)
app.secret_key = 'lWXE02osxb'


filters = []
filters_applied = False

# default home page 
@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template('project_template.html')

# api call/route for uploading videos
@app.route("/uploadvideo", methods=['POST', 'GET'])
def upload_video():

    # checks if an uploaded video file already exists
    if(len(os.listdir("static//videos"))) > 0:
        flash(message='Video Already Uploaded')
        abort(404)
        return '/'        

    # gets file from the request and checks that it has a name
    file = request.files['file']
    if file.filename == '':
         flash('No file selected')
         app.abort(404)
         return '/'
    
    # saves the file to the local server folder in the statics folder
    file.save("static//videos//video.mp4")
    
    return '/'

# api call/route for deleting the video on the server
@app.route("/deletevideo", methods=['GET'])
def delete_video():

    # checks if the video file actually exists
    if os.path.exists("static//videos//video.mp4"):
        print("video exists")

        # delete the original file user inputed video file along with the output file
        files = glob.glob('static//videos//*')
        for f in files:
            os.remove(f)
    
        return jsonify(
        message="Video Deleted Sucessfully")
    
    return jsonify(message="Video Deleted Unsucessfully")

# api call/route for configuring the filters into a global variable
# that lasts while the python server is running
@app.route("/configurefilters", methods=['POST', 'GET'])
def configure_filters():
    if request.method == "POST":
        # global word allows to be used outside of this function
        global filters
        # converts filters to python dictionary
        filters = request.form.getlist('filter')
    return '/'
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
        message="No filters are configured. Please configure filters first",
        )

    # iterates over the list of filters and applies them
    for filter in filters:
        if('grayscale:' in filter):
            video.greyScaleVideo()
        if('colorinvert:' in filter):
            video.invertVideo()



    while(not (isfile("static//videos//output.mp4") and access("static//videos//output.mp4", R_OK))):
        print("waiting for file to be readable")

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

