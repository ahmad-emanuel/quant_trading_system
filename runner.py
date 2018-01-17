from TradingAlgorithm import backtester
from PSO import PSO
import numpy as np
import pandas as pd
# Warnings
import warnings
from helper import warn_with_traceback


warnings.showwarning = warn_with_traceback

pso = PSO(backtester,10,100)
pso.run()

print('pso done')