import subprocess
import os

# Purpose
# greyscale the video uploaded by the user

def greyScaleVideo():

    # checks that the video exists first
    if(len(os.listdir("static//videos"))) <= 0:
        return False

    # args
    # -y : auto overwrite existing output file if there already is one
    # -i : input video in the user uploaded directory
    # -filter:v : create the filtergraph specified by v and use it to filter the stream. 
    # v meaning video
    # "hue=s=0" hue and saturation = 0 for greyscale
    # last param is the output directory 


    subprocess.call(["ffmpeg", "-y", "-i", "static/videos/video.mp4", "-filter:v", "hue=s=0", "static/videos/output.mp4"]) 
    
    os.remove("static//videos//video.mp4")
    os.rename("static//videos//output.mp4", "static//videos//video.mp4")

    return True