from TradingAlgorithm import backtester
from PSO import rand_arr_sum_one
import numpy as np


weights_trend = rand_arr_sum_one(9)

weights_non_trend = rand_arr_sum_one(9)

DB = 0.15
DS = -0.20

if abs(np.sum(weights_non_trend) - np.sum(weights_trend)) < 0.0000001:
    position = [weights_trend, weights_non_trend, DB, DS]
    b = backtester(position)
    mean_sharpe = b.run()
    print(mean_sharpe)
else:
    print('weights array are not correct')
    print(np.sum(weights_non_trend), np.sum(weights_trend))