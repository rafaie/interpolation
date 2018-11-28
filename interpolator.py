
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""


import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="define the max_transitions",
                        default=os.path.join("data", "AAPL.csv"))
    parser.add_argument("-c", "--column",
                        help="column number in CSV file",
                        type=int,
                        default=1)
    parser.add_argument("-v", "--verbose", help="Show more details",
                        action='store_true')

    args = parser.parse_args()
    print(args.file, args.column)
    # max_transitions = args.max_transitions if args.max_transitions else \
    #     MAX_TRANSITION
    # init_string = args.init_string
    # if args.file is True:
    #     with open(args.init_string, "r") as fi:
    #         init_string = fi.readlines()[0].strip()
    # t = Turing(init_string, max_transitions, args.verbose)
    # t.run()
