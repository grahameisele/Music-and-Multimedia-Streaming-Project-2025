import os
import re
import subprocess
# module with utility functions

# Purpose
# converts the fps filter to a integer value from string

# Params
# fps_filter
# the string value of the fps filter inputted by the user

# returns
# the fps value the user inputted if it is >= 0, -1 otherwise


def parse_fps_filter(fps_filter):

    fps_filter = fps_filter.replace('frameInterpolate: frameInterpolateTargetFps=', '')
    fps_filter = fps_filter.replace(',', '')
    
    try:
        fps_filter = int(fps_filter)
        
        if(fps_filter <= 0):
            return -1
        
        return fps_filter

    except ValueError:
        # Handle the exception
        print('Please enter an integer')
        return -1
    

# Purpose
# converts the upscale filter to a integer width and height values

# Params
# upscale_filter
# the string value of the fps filter inputted by the user

# returns
# the fps value the user inputted if it is >= 0, -1 otherwise
def parse_upscale_filter(upscale_filter):

    start = 'upscaleTargetWidth='
    end = ','

    width = -1
    height = -1

    pattern = re.compile(rf'(?<={re.escape(start)}).*?(?={re.escape(end)})')
    m = pattern.search(upscale_filter)
    if m:
       width = m.group(0)

    start = 'upscaleTargetHeight='
    pattern = re.compile(rf'(?<={re.escape(start)}).*?(?={re.escape(end)})')
    m = pattern.search(upscale_filter)
    if m:
        height = m.group(0)
    
    width = int(width)
    height = int(height)

    return [width, height]


# Purpose
#  applies a given ffmpeg command to the video that the user gives
#
# Params
#
# ffmpeg_command : the given ffmpeg command

def apply_ffmpeg_video_filter(ffmpeg_command):

    input_video_path_arg_index = -1
    output_video_path_arg_index = -1

    input_video_path_arg_index = ffmpeg_command.index("static/videos/video.mp4")
    output_video_path_arg_index = ffmpeg_command.index("static/videos/output.mp4")

    # if there already has been a processed video
    if(len(os.listdir("static//videos"))) >= 2:

        ffmpeg_command[input_video_path_arg_index] = "static/videos/output.mp4"
        ffmpeg_command[output_video_path_arg_index] = "static/videos/new_output.mp4"

        subprocess.call(ffmpeg_command) 
        os.remove("static//videos//output.mp4")
        os.rename("static//videos//new_output.mp4", "static//videos//output.mp4")

        return True
    
    #if there has not already been a processed vdeo
    else:
        subprocess.call(ffmpeg_command) 
