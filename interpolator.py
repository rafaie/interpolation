
"""
interpolator.py: a class to study different Univariate interpolation¶
                 on a given dataset in CSV format

"""

import pandas as pd
import numpy as np
from datetime import datetime
from scipy import interpolate
import argparse
import os
import math
import csv



def interpolate_linear(x, y):
    return interpolate.interp1d(x, y, kind='linear')

def interpolate_next(x, y):
    return interpolate.interp1d(x, y, kind='next')

def interpolate_previous(x, y):
    return interpolate.interp1d(x, y, kind='previous')

def interpolate_slinear(x, y):
    return interpolate.interp1d(x, y, kind='slinear')

def interpolate_nearest(x, y):
    return interpolate.interp1d(x, y, kind='nearest')

def interpolate_quadratic(x, y):
    return interpolate.interp1d(x, y, kind='quadratic')

def interpolate_cubic(x, y):
    return interpolate.interp1d(x, y, kind='cubic')

def interpolate_lagrange(x, y):
    return interpolate.lagrange(x.values, y.values)

INTERPOLATION_FUNC = [
                      # {'func': interpolate_lagrange, 'name': "Lagrange"},
                      {'func': interpolate_linear,   'name': "Linear"},
                      {'func': interpolate_previous,  'name': "Previous"},
                      {'func': interpolate_next,  'name': "Next"},
                      {'func': interpolate_nearest,  'name': "Nearest"},
                      {'func': interpolate_quadratic,
                       'name': "Quadratic Spline"},
                      {'func': interpolate_cubic,    'name': "Cubic Spline"},
                      {'func': interpolate_slinear,   'name': "Linear Spline"},
                      # {'func': interpolate.LinearNDInterpolator,
                      #  'name': "Piecewise linear"},

                      ]
CROSS_VARS = [5, 10, 15, 20, 30]
RETRY_COUNT = 10


class Interpolator:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def read_data(self, file, column1, column2):
        df = pd.read_csv(file)
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
        self.outfile = open(fname, 'w')
        outfile_csv = csv.writer(self.outfile, delimiter=',',
                                 quotechar="'", quoting=csv.QUOTE_MINIMAL)
        outfile_csv.writerow(['datetime', 'method', 'cross_num',
                              'runtime', 'retry',
                              'min_rmse', 'min_min', 'min_max', 'min_std',
                              'max_rmse', 'max_min', 'max_max', 'max_std',
                              'mean_rmse', 'mean_min', 'mean_max', 'mean_std',
                              ])
        return outfile_csv

    def close_csv(self):
        self.outfile.close()

    def create_train_test_dataset(self, dfs, df, i):
        df_train = pd.concat([dfs[ii] for ii in range(len(dfs)) if i != ii])
        df_train = df_train.sort_values(list(df_train)[2])

        df_test = dfs[i]
        df_test = df_test.sort_values(list(df_train)[2])

        # Add start and end range to df_train and remove from df_test
        if df_train.iloc[0, 2] != 0:
            df_train = pd.concat([df_test.iloc[0:1, :], df_train])
            df_test = df_test.iloc[1:, :]
            # print('CASE1')

        if df_train.iloc[-1, 2] != df.iloc[-1, 2]:
            df_train = pd.concat([df_train, df_test.iloc[-1:, :]])
            df_test = df_test.iloc[:-1, :]
            # print('CASE2')

        return (df_train, df_test)

    def analysis_result(self, df):
        df_tmp = (df.iloc[:, 1] - df.iloc[:, 3])
        rmse = (df_tmp ** 2).mean() ** .5
        min = df_tmp.abs().min()
        max = df_tmp.abs().max()
        std = df_tmp.abs().std()

        return (rmse, min, max, std)

    def run_interpolation(self, dfs, df, cross_num, r, in_func, csv_file):
        analysis = []
        start_t = datetime.now()
        for i in range(cross_num):
            print('==>', in_func['name'], ',', r, ',', cross_num, ',', i)
            df_train, df_test = self.create_train_test_dataset(dfs, df, i)
            model = in_func['func'](df_train.iloc[:, 2], df_train.iloc[:, 1])
            df_test['new_x'] = model(df_test.iloc[:, 2])
            analysis.append(self.analysis_result(df_test))

        end_t = datetime.now()
        analysis = np.array(analysis)
        min = np.min(analysis, axis=0)
        max = np.max(analysis, axis=0)
        mean = np.mean(analysis, axis=0)
        csv_file.writerow([start_t, in_func['name'], cross_num,
                          (end_t - start_t).microseconds, r] +
                          list(min) + list(max) + list(mean))

    def run(self, file, column1, column2, verbose=None):
        verbose = self.verbose if verbose is None else verbose
        df = self.read_data(file, column1, column2)
        csv_file = self.open_csv()
        for i in CROSS_VARS:
            for r in range(RETRY_COUNT):
                dfs = self.create_dataset(df, i)
                for in_func in INTERPOLATION_FUNC:
                    self.run_interpolation(dfs, df, i, r, in_func, csv_file)
        self.close_csv()


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
