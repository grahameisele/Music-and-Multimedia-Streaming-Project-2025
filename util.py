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


# purpose
# to parse the gain compresor filter provided by the user
#
# params
# gain_compressor_filter: the unparsed gain_compressor_filter found in the html element
#
# returns
# the parsed gain_compressor_filter

def parse_gain_compressor_filter(gain_compressor_filter):

    # ex unparsed filter
    # gainCompressor: gainCompressorThreshold=-1, limiterThreshold=0,

    # get the compresor threshold
    
    first_equal_sign_index = gain_compressor_filter.find("=")
    first_comma_index = gain_compressor_filter.find(",")

    gain_compressor_threshold = gain_compressor_filter[first_equal_sign_index + 1 : first_comma_index]

    # try to convert gain compressor threshold to integer from string
    try:
        gain_compressor_threshold = int(gain_compressor_threshold) 
    except ValueError:
        print("Error parsing gain compressor threshold")
    
    # get the limiter threshold

    limiter_threshold_filter = gain_compressor_filter[first_comma_index + 1:]

    limiter_threshold_first_equal_index = limiter_threshold_filter.find("=")
    limiter_threshold_first_comma_index = limiter_threshold_filter.find(",")

    limiter_threshold = limiter_threshold_filter[limiter_threshold_first_equal_index + 1 : limiter_threshold_first_comma_index]

     # try to convert gain limiter threshold to integer from string
    try:
        limiter_threshold = int(limiter_threshold) 
    except ValueError:
        print("Error parsing limiter threshold")

    return gain_compressor_threshold, limiter_threshold

# Purpose: to parse the voice enhancement filter in the html webpage
#
# params
# voice_enhancement_filter: the unparsed voice enhancement filter
#
# returns
# a Pre-emphasis alpha value and a High pass filter order value

def parse_voice_enhancement_filter(voice_enhancement_filter):
    
    # ex unparsed filter
    # gainCompressor: voiceEnhancement: preemphasisAlpha=3, highPassFilter=2,

    # get the preemphasisAlpha value
    
    first_equal_sign_index = voice_enhancement_filter.find("=")
    first_comma_index = voice_enhancement_filter.find(",")

    preemphasisAlpha = voice_enhancement_filter[first_equal_sign_index + 1 : first_comma_index]

    # try to convert preemphasisAlpha to integer from string
    try:
        print("Pre-emphasis alpha: ", preemphasisAlpha)
        preemphasisAlpha = float(preemphasisAlpha) 
    except ValueError:
        print("Error parsing preemphasis alpha")
    
    # get the highPassFilter value

    highPassFilter_filter = voice_enhancement_filter[first_comma_index + 1:]

    highPassFilter_first_equal_index = highPassFilter_filter.find("=")
    highPassFilter_first_comma_index = highPassFilter_filter.find(",")

    highPassFilter = highPassFilter_filter[highPassFilter_first_equal_index + 1 : highPassFilter_first_comma_index]

     # try to convert gain limiter threshold to integer from string
    try:
        highPassFilter = int(highPassFilter) 
    except ValueError:
        print("Error parsing limiter threshold")
        return "error", "error"

    return preemphasisAlpha, highPassFilter

# Purpose
#
# parses raw denoise delay filter
#
# returns the parsed parameters passed by the user
# 

def parse_denoise_delay_filter(denoise_delay_filter):

    parameters = []
    
    first_equal_sign_index = denoise_delay_filter.find("=")
    first_comma_index = denoise_delay_filter.find(",")


    while(first_equal_sign_index > 0):

        current_param = denoise_delay_filter[first_equal_sign_index + 1 : first_comma_index]
        
        current_param = int(current_param)

        parameters.append(current_param)

        denoise_delay_filter = denoise_delay_filter[first_comma_index + 1:]        
        
        first_equal_sign_index = denoise_delay_filter.find("=")
        first_comma_index = denoise_delay_filter.find(",")

    return parameters

# Purpose 
# 
# extracts wav audio from the uploaded user video
#
def extract_audio_from_video():

    # path of the video to extract audio from
    video_file_path = "static//videos//video.mp4"

    # checks if an uploaded video file already exists
    if(os.path.exists(video_file_path)) <= 0:
        print("User uploaded video to extract audio from does not exist")
        return False

    # -acodec: audio codec
    # -c: is a stream specifier and a means audio tream
    # the audio codec to use, 16 bit audio
    # -ar : set audio sampple rate
    # -ac: number of audio channels which is 2 for stereo  

    ffmpeg_command = ["ffmpeg", "-y", "-i", video_file_path, "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2", "static/audio/output.wav"]
    
    subprocess.call(ffmpeg_command) 

    return True

# Purpose
#
# to combine audio located in the audio folder with the user uploaded video applied with filters
#
# Params
# video_to_combine_audio_with_path: path of the video to combine with
#
def combine_audio_with_video(at_least_one_video_filter):

    # the path of which to combine the modified video and modified audio
    video_to_combine_audio_with_path = "static//videos//output.mp4"
    
    # the path which to output the filtered video with the filtered audio
    output_video_path =  "static//videos//new_output.mp4"

    # if there is no video filters, just combined the modified audio with the original video
    if not at_least_one_video_filter:
        print("No video filters")
        video_to_combine_audio_with_path = "static//videos//video.mp4"
        output_video_path =  "static//videos//output.mp4"

    # ffmpeg command for combining video with filters with audio with filters
    ffmpeg_command = ["ffmpeg", "-y", "-i", video_to_combine_audio_with_path, "-i", "static//audio//output.wav", "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", output_video_path]

    subprocess.call(ffmpeg_command)

    os.remove("static//videos/output.mp4")
    os.rename("static//videos/new_output.mp4", "static//videos/output.mp4")

