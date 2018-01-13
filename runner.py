from TradingAlgorithm import backtester
### Warnings
import traceback
import warnings
import sys

#  print traceback of occurred warnings
def warn_with_traceback(message, category, filename, lineno, file=None, line=None):

    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))

warnings.showwarning = warn_with_traceback


weights_trend = [0.7, 0.3]
weights_non_trend = [0.2,0.3,0.1,0.2,0.2]
DB = 0.6
DS = -0.5

b = backtester(weights_trend, weights_non_trend, DB, DS)
b.run()
