from TradingAlgorithm import backtester
import pandas as pd

def result_topickle():
    # import optimization run results
    test_result = pd.read_pickle('global_best_solutions')

    # generate global best position
    best_position = test_result.position[-1]

    # rerun the global best position
    bs = backtester(best_position)
    mean_sharpe, backtest_result = bs.run()

    backtest_result.to_pickle('gbest_zipresult')
    # excell
    s_alg = backtest_result['algorithm_period_return']


if __name__ == '__main__':

    # df result
    zipline_result = pd.read_pickle('gbest_zipresult')

    s_algo_return = zipline_result.iloc[:,1]
    s_benchmark = zipline_result.loc[:,'benchmark_period_return']

    df = pd.DataFrame(columns=list(s_algo_return.index))

    df.loc[s_algo_return.name] = s_algo_return
    df.loc[s_benchmark.name] = s_benchmark

    ## to excell
    writer = pd.ExcelWriter('output.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()



posiotions = [0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,3,0]
print('finito')

