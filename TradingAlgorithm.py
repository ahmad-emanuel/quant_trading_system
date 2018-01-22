import numpy as np
import pandas as pd
from zipline import run_algorithm
from zipline.api import attach_pipeline, pipeline_output
# schedule function
from zipline.api import schedule_function
from zipline.utils.events import date_rules
from zipline.utils.events import time_rules
from zipline.api import order_target_percent
# Pipeline Imports
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import RSI
from Indicators.CCI_self import CCI
from Indicators.ADX_Self import ADX
from Indicators.Bollinger_Bands_self import BollingerBands
from Indicators.Latest_self import Latest
from Indicators.Stochastic_Oscillator_self import Stochastic
from Indicators.Momentum_self import Momentum
from Indicators.MACD_self import MovingAverageConvergenceDivergence
from Indicators.EWMA_self import EWMA
from Indicators.chaikin_oscilator import AD
from Indicators.money_flow_index import MFI
# reevaluate
from reevaluate_asset import reevaluate_pipeline
from normalize_weights import normalize_weights
# helper
from helper import auto_attr_check


@auto_attr_check
class backtester:

    weights_trend = []
    weights_non_trend = []
    DB = float
    DS = float
    result = pd.DataFrame

    def __init__(self, position):

        # for each indicator, we must have a weight coefficient
        if len(position[0]) != 9 or len(position[1]) != 9:
            raise ValueError("the length of weights must be equal to number of indicators!")
        if abs(np.sum(position[0]) - np.sum(position[1])) > 0.0000001:
            raise ValueError("the sum of weights array must be equal to one!")

        self.weights_trend = position[0]
        self.weights_non_trend = position[1]
        self.DB = position[2]
        self.DS = position[3]

    def make_pipeline(self):
        macd = MovingAverageConvergenceDivergence()
        rsi = RSI()
        adx = ADX()
        cci = CCI()
        bol_band = BollingerBands(k=2.0)
        latest = Latest()
        stoch = Stochastic()
        momentum = Momentum()
        ewma = EWMA()

        return Pipeline(
            columns={
                'RSI': rsi,     # Default Inputs: [USEquityPricing.close]  Default Window Length: 15-day
                'MACD': macd,   # Moving average convergence divergence
                'ADX': adx,
                'Commodity Channel Index': cci,
                'Bollinger Bands': bol_band,     # Default Window Length: 20-day     Default K=2 (Coefficient of Standard diviation)
                'latest close': latest,          # Default Window Length: 2-day      generate last 2 close prices
                'Stochastic': stoch,             # Default Window Length: 5-day      generte %K lines of today and yesterday
                'Momentum': momentum,            # Default Window Length: 20-day     geneate the Momentum of yesterday and today related to close price of 20days ago
                'EWMA': ewma,                    # Default Window Length: 38       span = 7 (one week)
                'CHO': AD(),                     # Default Window Length: 14-day
                'MFI': MFI()                     # Default Window Length: 14-day
            }
        )

    def initialize(self, context):
        # Schedule our rebalance function to run every day, after a 1 hour, when the market opens.
        schedule_function(
            self.rebalance,
            date_rules.every_day(),
            time_rules.market_open(hours = 1, minutes = 0)
        )

        my_pipe = self.make_pipeline()
        attach_pipeline(my_pipe, "my_pipeline")

    def handle_data(self,context, data):
        pass

    def before_trading_start(self, context, data):

        # pandas Dataframe of pipeline Output
        context.output = pipeline_output("my_pipeline")

        # generate weights based on pipeline output to go or long
        context.weights = self.compute_target_weights(context, data)


        #### TEST ######
        #context.output.to_pickle('pipeline_result')
        # test = pd.DataFrame(index=final_signal.index)
        # test['weighted Signal'] = weighted_signal
        # test['final Signal'] = final_signal
        # test.to_pickle('test_signal')

        print('before trading ran',len(context.weights))

    def run(self):
        START = pd.Timestamp("2015-02-10", tz="EST")
        END = pd.Timestamp("2015-03-01", tz="EST")
        self.result = run_algorithm(start=START, end=END,
                                    initialize=self.initialize,
                                    before_trading_start=self.before_trading_start,
                                    capital_base=100000,
                                    handle_data=self.handle_data,
                                    bundle='quantopian-quandl')


        #self.result.to_csv('Trading_result')
        #print(np.mean(self.result.sharpe))
        #return np.mean(self.result.sharpe)
        #####test
        mean_sharpe = np.mean(self.result.sharpe)
        print(mean_sharpe)
        return mean_sharpe,self.result

    def compute_target_weights(self, context, data):

        # will be filled with weights  -1<float<1
        weighted_signal = pd.Series(index=context.output.index, dtype=np.float32)

        for index, value in context.output.iterrows():

            if value.ADX >= 30:  # there is a trend
                weighted_signal[index] = reevaluate_pipeline(value, self.weights_trend)
            else:  # there is either non-trend or NAN
                weighted_signal[index] = reevaluate_pipeline(value, self.weights_non_trend)

        # will be filled with trade signals  int: -1,0,1
        final_signal = pd.Series(index=context.output.index, dtype=np.int8)

        for index, value in weighted_signal.iteritems():
            if value >= self.DB and data.can_trade(index):
                final_signal[index] = 1
            elif value <= self.DS and data.can_trade(index):
                final_signal[index] = -1
            else:
                final_signal[index] = 0

        # Initialize empty target weights dictionary.
        # This will map securities to their target weight.
        weights = {}

        for asset, signal in final_signal.iteritems():
            if signal != 0:
                weights[asset] = abs(weighted_signal[asset]) * final_signal[asset]

        # Exit positions in our portfolio if they are not
        # in our longs or shorts lists.
        for security in context.portfolio.positions:
            if security not in context.weights.keys():
                weights[security] = 0

        return normalize_weights(weights)

    def rebalance(self, context, data):

        for asset, percent in context.weights.items():
            order_target_percent(
                asset=asset,
                target=percent
            )