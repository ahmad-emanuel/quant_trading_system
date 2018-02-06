from TradingAlgorithm import backtester
import pandas as pd

# import optimization run results
test_result = pd.read_pickle('global_best_solutions')
#
# generate global best position
best_position = test_result.position[-1]

# rerun the global best position
bs = backtester(best_position)
mean_sharpe, backtest_result = bs.run()

backtest_result.to_pickle('zip_result_pickle')

#backtest_result.to_pickle('gbest_reslt')
# run pyfolio
# returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(backtest_result)
# pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions,
#                           live_start_date='2015-02-01', round_trips=True)

# mean_sharpe = 0
# max = 0
# for i in range(1,20):
#     best_position = test_result.position[-i]
#
#     bs = backtester(best_position)
#     new_scharpe, backtest_result = bs.run()
#
#     if new_scharpe > mean_sharpe:
#         mean_sharpe = new_scharpe
#         max = i
#
# print(max)

print('finito')