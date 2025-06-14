from os.path import isfile
from flask import Flask, render_template, request, flash, abort
from flask import jsonify
import util
import audio
import os
import video

# creates flask instance
app = Flask(__name__)
app.secret_key = 'lWXE02osxb'


filters = []
filters_applied = False
filters_configured = False

# default home page 
@app.route("/", methods=['GET', 'POST'])
def homepage():
    return render_template('project_template.html')

# api call/route for uploading videos
@app.route("/uploadvideo", methods=['POST', 'GET'])
def upload_video():

    video_file_path = "static//videos//video.mp4"

    # checks if an uploaded video file already exists
    if(os.path.exists(video_file_path)) > 0:
        return jsonify(message='Video Already Uploaded / Exists')   

    # gets file from the request and checks that it has a name
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify(message='No video to upload')   
    
    # saves the file to the local server folder in the statics folder
    file.save("static//videos//video.mp4")
    
    return jsonify(message='Video uploaded successfully!')   

# api call/route for deleting the video on the server
@app.route("/deletevideo", methods=['GET'])
def delete_video():

    # checks that the filters have been applied before deleting the file
    # "The server must store the uploaded video until the filtered version has been 
    #  created, then it is no longer needed and can be deleted"

    if(not filters_applied):
       return jsonify(message="Video can only be deleted after the filtered version has been made.") 

    # file path of the originally uploaded video by the user
    video_file_path = "static//videos//video.mp4"

    # checks if the video file actually exists
    if os.path.exists(video_file_path):
        # delete the original file user inputed video file along with the output file
        os.remove(video_file_path)

        return jsonify(
        message="Video Deleted Sucessfully")
    else:
        return jsonify(message="There is no video to delete")
    
# api call/route for configuring the filters into a global variable
# that lasts while the python server is running
@app.route("/configurefilters", methods=['POST', 'GET'])
def configure_filters():

    global filters_configured
    filters_configured = False
    global configureFilters
    filters_applied = False

    # resets the filters
    global filters
    filters = []

    if request.method == "POST":
        # global word allows to be used outside of this function
       
        # converts filters to python dictionary
        filters = request.form.getlist('filter')

        if(len(filters)) <= 0:
             return jsonify(
                    message="There are no filters to configure, please configure them")  

        # checks if the user tries to use any filters that are not implemented
        for filter in filters:

            print("Filter: ", filter)

            if('denoiseDelay' in filter):
                return jsonify(
                    message="Error, the denoise delay is not implemented. Please remove it.")  
            
            if('phone' in filter):
                return jsonify(
                    message="Error, the phone filter is not implemented. Please remove it.")  

            if('car' in filter):
                return jsonify(
                    message="Error, the car filter is not implemented. Please remove it.")

       
        filters_configured = True
        return jsonify(
        message="Filters configured",
        )
        
    return '/'
# api call/route for applying the filters stored in the global variable
@app.route("/applyfilters", methods=['GET'])
def applyfilters():

    if(isfile("static//videos/output.mp4")):
        os.remove("static//videos/output.mp4")

    if(not filters_configured):
        return jsonify(
        message="Please configure filters first",
        ) 

    at_least_one_video_filter = False

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
    
    # extract the audio from the video to apply the audio filters
    util.extract_audio_from_video()

    # iterates over the list of filters and applies them
    for filter in filters:
        if('grayscale:' in filter):
            at_least_one_video_filter = True
            video.greyScaleVideo()
        if('colorinvert:' in filter):
            at_least_one_video_filter = True
            video.invertVideo()
        if('frameInterpolate:' in filter):
            at_least_one_video_filter = True
            fps_value = util.parse_fps_filter(filter)

            if(fps_value <= 1):
                 return jsonify(
                message="FPS Value Cannot be less than or equal to 1.",
            )
            elif(fps_value >= 1):
                video.fps_interpolate(fps_value)
        if('upscale:' in filter):
            at_least_one_video_filter = True
            width, height = util.parse_upscale_filter(filter)
            
            if(not video.upscale_video(width, height)):
                  return jsonify(
                message="Error, width or height are less than 1. Both must be greater than or equal to one")    
        
        if('gainCompressor' in filter):
            filter_params = util.parse_audio_filter(filter)

            compressor_threshold = filter_params[0]
            limiter_threshold = filter_params[1]

            # check that user has entered valid integers for both of the input fields
            if len(str(compressor_threshold)) == 0 or len(str(limiter_threshold)) == 0:
               return jsonify(
                message="Error, one of the values entered for the gain compression filter are empty.")
            
            else:
               # apply the gain compression with the user provided variables
               audio.apply_gain_compression(compressor_threshold, limiter_threshold)

        if('voiceEnhancement' in filter):

            filter_params = util.parse_audio_filter(filter)

            preemphasisAlpha = filter_params[0]
            highPassFilter = filter_params[1]

            # check if the filter is valid
            if(preemphasisAlpha == "error" or highPassFilter == "error"):
                return jsonify(
                message="Error, one of the values entered for the voice enhancement filter are invalid or empty.")  
            
            # applies the simple voice enhancement filter to the audio
            audio.apply_voice_enchancement_filter(preemphasisAlpha, highPassFilter)
    
    # combine the audio with filters applied with the video that has the filters appleid
    util.combine_audio_with_video(at_least_one_video_filter)

    global filters_applied
    filters_applied = True
    
    return jsonify(
        message="Filters Applied Sucessfully",
    )


# api call / route for starting to stream the video
@app.route("/startstreaming", methods=['GET'])
def startstreaming():
    
    # returns json saying whether the video can proceed to play
    return jsonify(
        canPlay=filters_applied,
    )

# Purpose
# starts python flask web server 
def start_server():
    app.run("0.0.0.0", port=80, debug=True)

