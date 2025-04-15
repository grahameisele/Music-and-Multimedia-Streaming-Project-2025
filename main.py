import argparse
import audio
#main program file

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help = "input filename")
    args =  parser.parse_args()
    return args

# main function
def main(args):
    samples, sample_rate = audio.get_samples_and_sample_rate(args.input)
    samples, audio.add_gain_compression(samples, sample_rate)

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main(args)