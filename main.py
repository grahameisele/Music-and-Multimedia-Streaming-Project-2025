import argparse
import server
import audio
#main program file

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    args =  parser.parse_args()
    return args

# main function
def main():
    
    # start the web server
    server.start_server()

    #samples, sample_rate = audio.get_samples_and_sample_rate("input.wav")

    #new_samples = audio.apply_audio_delay(samples, sample_rate, 5000)

    #audio.save_audio("output.wav", new_samples, sample_rate)

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main() 


