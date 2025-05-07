import os
import util

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

    ffmpeg_command = ["ffmpeg", "-y", "-i", "static/videos/video.mp4", "-filter:v", "hue=s=0", "static/videos/output.mp4"]

    util.apply_ffmpeg_video_filter(ffmpeg_command)

    return True

# Purpose
# to invert the colors of a video
def invertVideo():

    # checks that the video exists first
    if(len(os.listdir("static//videos"))) <= 0:
        return False
    
    # ffmpeg command with video filter
    # 
    # filter:v means apply a video filter
    # negate: inverts the colors of a video: 
    # I found in: https://ffmpeg.org/ffmpeg-filters.html

    ffmpeg_command = ["ffmpeg", "-y", "-i", "static/videos/video.mp4", "-filter:v", "negate", "static/videos/output.mp4"]

    util.apply_ffmpeg_video_filter(ffmpeg_command)

    return True

# Purpose
# to interoplate the fps of a video

# Parameters
# fps
# the fps in which to interoplate to

def fps_interpolate(fps):

    # checks that the video exists first
    if(len(os.listdir("static//videos"))) <= 0:
        return False

    # ffmpeg command for interpolating the fps of a video
    ffmpeg_command = ["ffmpeg", "-i", "static/videos/video.mp4", "-filter:v", f"fps={fps}", "static/videos/output.mp4"]
    
    util.apply_ffmpeg_video_filter(ffmpeg_command)

    return True

# Purpose
# to upscale a video

# Parameters
#
# width: the width to which to scale the video to
# 
# height: the height to which to scale the video to

def upscale_video(width, height):

    print(width)
    print(height)

    print("Width less than 0: ", width <= 0)
    print("Height less than 0: ", height <= 0)

    if(width <= 0 or height <= 0):
        return False
    
    # calls ffmpeg to scale a video to certain width and height
    ffmpeg_command = ["ffmpeg", "-y", "-i", "static/videos/video.mp4", "-filter:v", f"scale={width}:{height}", "static/videos/output.mp4"]
    
    util.apply_ffmpeg_video_filter(ffmpeg_command)

    return True

