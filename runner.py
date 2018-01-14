from TradingAlgorithm import backtester
import numpy as np
### Warnings
import traceback
import warnings
import sys


# sum of array equal to 1
def sum_equal_one(arr):
    sum = np.sum(arr, axis=0)
    return arr / sum


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

DB = 0.6
DS = -0.5

b = backtester(weights_trend, weights_non_trend, DB, DS)
b.run()
