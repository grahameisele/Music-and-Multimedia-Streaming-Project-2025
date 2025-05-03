import argparse
import server
#main program file

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    args =  parser.parse_args()
    return args

# main function
def main():
   

    # start the web server
    # util.extract_audio_from_video()

    server.start_server()

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main() 


