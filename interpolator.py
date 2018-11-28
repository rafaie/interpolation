
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""

import numpy as np
import pandas as pd
import argparse
import os


class Interpolator:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def read_data(self, file, column1, column2):
        data = np.genfromtxt(file, delimiter=',', skip_header=1)
        data = pd.read_csv(file)
        return data.iloc[:, [column1, column2]]

    def run(self, file, column1, column2, verbose=None):
        verbose = self.verbose if verbose is None else verbose
        base_data = self.read_data(file, column1, column2)
        print(base_data[:10])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="define the max_transitions",
                        default=os.path.join("data", "AAPL.csv"))
    parser.add_argument("-c1", "--column1",
                        help="The base column number in CSV file",
                        type=int,
                        default=0)
    parser.add_argument("-c2", "--column2",
                        help="The second column number in CSV file",
                        type=int,
                        default=4)
    parser.add_argument("-v", "--verbose", help="Show more details",
                        action='store_true')

    args = parser.parse_args()

    i = Interpolator()
    i.run(args.file, args.column1, args.column2, args.verbose)
