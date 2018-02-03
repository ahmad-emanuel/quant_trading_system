from TradingAlgorithm import backtester
import pandas as pd

# import optimization run results
test_result = pd.read_pickle('global_best_solutions_1')

# generate global best position
best_position = test_result.position[-1]

#### test
trend = sum(best_position[0])
non_trend = sum(best_position[1])
print(trend - non_trend)
######
# rerun the global best position
bs = backtester(best_position)
mean_sharpe, backtest_result = bs.run()

backtest_result.to_csv('result_csv')
#backtest_result.to_pickle('gbest_reslt')
# run pyfolio
# returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(backtest_result)
# pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions,
#                           live_start_date='2015-02-01', round_trips=True)



print('finito')