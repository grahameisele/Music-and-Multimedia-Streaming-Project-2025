import re
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
