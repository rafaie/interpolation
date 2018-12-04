
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""

import pandas as pd
from datetime import datetime
from scipy import interpolate
import argparse
import os
import math
import csv


INTERPOLATION_FUNC = [{'func': interpolate.interp1d, 'name': "interp1d"}]
CROSS_VARS = [5, 10, 15, 20, 30]
RETRY_COUNT = 1


class Interpolator:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def read_data(self, file, column1, column2):
        df = pd.read_csv(file)
        # print()
        df = df.sort_values(list(df)[column1])
        d1 = datetime.strptime(df.iloc[0, column1], "%Y-%m-%d")
        df['x'] = [(datetime.strptime(d2, "%Y-%m-%d") - d1).days for d2 in
                   df.iloc[:, column1]]
        print(d1)
        return df.iloc[:, [column1, column2, -1]]

    def create_dataset(self, df, cross_num):
        df2 = df.sample(frac=1)
        c = df2.shape[0]
        d = math.floor(c / cross_num)
        dfs = [df2.iloc[d * (i - 1):d * i - 1, :]
               for i in range(1, cross_num+1)]
        dfs[-1] = pd.concat([dfs[-1], df2.iloc[cross_num * d:, :]])

        return dfs

    def open_csv(self):
        fname = os.path.join("output",
                             "result_" +
                             datetime.now().strftime('%Y%m%d%H%M%S') +
                             ".csv")
        with open(fname, 'w') as outfile:
            outfile_csv = csv.writer(outfile, delimiter=',',
                                     quotechar="'", quoting=csv.QUOTE_MINIMAL)
        return outfile_csv

    def create_train_test_dataset(self, dfs, df, i):
        df_train = pd.concat([dfs[ii] for ii in range(len(dfs)) if i != ii])
        df_train = df_train.sort_values(list(df_train)[2])

        df_test = dfs[i]
        df_test = df_test.sort_values(list(df_train)[2])

        # Add start and end range to df_train and remove from df_test
        if df_train.iloc[0, 2] != 0:
            df_train = pd.concat([df_test.iloc[0:1, :], df_train])
            df_test = df_test.iloc[1:, :]
            print('CASE1')

        if df_train.iloc[-1, 2] != df.iloc[-1, 2]:
            df_train = pd.concat([df_train, df_test.iloc[-1:, :]])
            df_test = df_test.iloc[:-1, :]
            print('CASE2')

        return (df_train, df_test)

    def analysis_result(self, df1, df2):
        pass

    def run_interpolation(self, dfs, df, cross_num, r, in_func, csv_file):
        for i in range(cross_num):
            print('------------')
            print("====>", i)
            df_train, df_test = self.create_train_test_dataset(dfs, df, i)
            # print("=======\n", df_train)
            # print("=======\n", df_test)
            model = in_func['func'](df_train.iloc[:, 2], df_train.iloc[:, 1])
            df_test['new_x'] = model(df_test.iloc[:, 2])
            # self.analysis_result(df_test.iloc[:, 1], df_test.iloc[:, 3])

    def run(self, file, column1, column2, verbose=None):
        verbose = self.verbose if verbose is None else verbose
        df = self.read_data(file, column1, column2)
        csv_file = self.open_csv()
        for i in CROSS_VARS[:1]:
            for r in range(RETRY_COUNT):
                dfs = self.create_dataset(df, i)
                for in_func in INTERPOLATION_FUNC:
                    self.run_interpolation(dfs, df, i, r, in_func, csv_file)


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
