from TradingAlgorithm import backtester
import numpy as np
import pandas as pd
### Warnings
import traceback
import warnings
import sys


# sum of array equal to 1
def sum_equal_one(arr):
    s = np.sum(arr, axis=0)
    return arr / s


#  print traceback of occurred warnings
def warn_with_traceback(message, category, filename, lineno, file=None, line=None):

    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))


warnings.showwarning = warn_with_traceback


weights_trend = np.random.random_sample(9)
weights_trend = sum_equal_one(weights_trend)

weights_non_trend = np.random.random_sample(9)
weights_non_trend = sum_equal_one(weights_non_trend)

DB = 0.15
DS = -0.20

if abs(np.sum(weights_non_trend) - np.sum(weights_trend)) < 0.0000001:
    START = pd.Timestamp("2015-02-10", tz="EST")
    END = pd.Timestamp("2015-03-01", tz="EST")
    b = backtester(weights_trend, weights_non_trend, DB, DS)
    b.run(START,END)
else:
    print('weights array are not correct')
    print(np.sum(weights_non_trend), np.sum(weights_trend))
