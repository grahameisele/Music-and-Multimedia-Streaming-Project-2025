import argparse
#main program file


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help = "input filename")
    args =  parser.parse_args()
    return args

def main(args):
    print(args.input)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)