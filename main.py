import argparse
import audio
import server
import video
#main program file

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help = "input filename")
    args =  parser.parse_args()
    return args

# main function
def main(args):
    #samples, sample_rate = audio.get_samples_and_sample_rate(args.input)
    #samples = audio.apply_gain_compression(samples)
    #audio.save_audio("output.wav", samples, sample_rate)

    # start the web server
    #video.greyScaleVideo()
    server.start_server()

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main(args) 


