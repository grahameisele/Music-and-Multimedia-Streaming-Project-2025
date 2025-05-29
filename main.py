# main.py
import argparse
import server

# parse arguments given by the user
def parse_arguments():
    parser = argparse.ArgumentParser()
    args =  parser.parse_args()
    return args

# main function
def main():
    
    # start the web server
    server.start_server()

# to tell that it is main program
if __name__ == "__main__":
    args = parse_arguments()
    main() 


