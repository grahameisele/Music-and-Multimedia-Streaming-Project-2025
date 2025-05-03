import argparse
import server
import audio
import util
#main program file

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    args =  parser.parse_args()
    return args

# main function
def main():
   

    # start the web server
    util.extract_audio_from_video()

    samples, sample_rate = audio.get_samples_and_sample_rate("test.wav")
    samples = audio.apply_gain_compression(samples, 50, 50)
    audio.save_audio("output.wav", samples, sample_rate)

    # server.start_server()

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main() 


