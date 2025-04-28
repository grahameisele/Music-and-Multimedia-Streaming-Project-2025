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
    
