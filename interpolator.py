
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""


import argparse
import os


class Interpolator:
    def __init__(self, file, column, verbose):
        self.file

    def run(self, file=None, column=None, verbose=None):
        pass


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

    i = Interpolator(args.file, args.column, args.verbose)
    i.run()
