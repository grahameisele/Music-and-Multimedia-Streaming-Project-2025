import argparse
import audio
#main program file


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help = "input filename")
    args =  parser.parse_args()
    return args

def main(args):
    audio.get_samples_and_sample_rate(args.input)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)