
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""

import numpy as np
import pandas as pd
import argparse
import os

CROSS_VARS = [5, 10, 15, 20, 30]
RETRY_COUNT = 5


class Interpolator:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def read_data(self, file, column1, column2):
        df = pd.read_csv(file)
        return df.iloc[:, [column1, column2]]

    def create_dataset(self, df, cross_num):
        df2 = df.sample(frac=1)
        dfs = np.split(df2, [cross_num], axis=1)
        return dfs

    def run(self, file, column1, column2, verbose=None):
        verbose = self.verbose if verbose is None else verbose
        base_data = self.read_data(file, column1, column2)
        print(base_data[:10])
        for i in CROSS_VARS[1]:
            dfs = self.create_dataset(df, i)
            print(i, dfs[i])


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
