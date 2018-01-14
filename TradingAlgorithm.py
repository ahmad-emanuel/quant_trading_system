import numpy as np
import pandas as pd
from zipline import run_algorithm
from zipline.api import attach_pipeline, pipeline_output
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
# helper
from helper import auto_attr_check


@auto_attr_check
class backtester:

    weights_trend = []
    weights_non_trend = []
    DB = float
    DS = float
    result = pd.DataFrame

    def __init__(self, weights_trend, weights_non_trend, db, ds):

        # for each indicator, we must have a weight coefficient
        if len(weights_non_trend) != 9 or len(weights_trend) != 9:
            raise ValueError("the length of weights must be equal to number of indicators!")

        self.weights_trend = weights_trend
        self.weights_non_trend = weights_non_trend
        self.DB = db
        self.DS = ds

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
                'Bollinger Bands': bol_band,     # Default Window Length: 20-day    Default K=2 (Coefficient of Standard diviation)
                'latest close': latest,          # Default Window Length: 2-day      generate last 2 close prices
                'Stochastic': stoch,             # Default Window Length: 5-day      generte %K lines of today and yesterday
                'Momentum': momentum,            # Default Window Length: 20-day     geneate the Momentum of yesterday and today related to close price of 20days ago
                'EWMA': ewma,                    # Default Window Length: 38       span = 7 (one week)
                'CHO': AD(),                     # Default Window Length: 14-day
                'MFI': MFI()                     # Default Window Length: 14-day
            }
        )

    def initialize(self, context):
        my_pipe = self.make_pipeline()
        attach_pipeline(my_pipe, "my_pipeline")

    def handle_data(self,context, data):
        pass

    def before_trading_start(self, context, data):
        # pandas Dataframe of pipeline Output
        output = pipeline_output("my_pipeline")

        # will be filled with weights  -1<float<1
        weighted_signal = pd.Series(index=output.index, dtype=np.float32)

        for index, value in output.iterrows():

            if value.ADX >= 30:  # there is a trend
                weighted_signal[index] = reevaluate_pipeline(value,self.weights_trend)
            else:  # there is either non-trend or NAN
                weighted_signal[index] = reevaluate_pipeline(value, self.weights_non_trend)

        # will be filled with trade signals  int: -1,0,1
        final_signal = pd.Series(index=output.index, dtype=np.int8)

        for index, value in weighted_signal.iteritems():
            if value > self.DB:
                final_signal[index] = 1
            elif self.DS <= value <= self.DB:
                final_signal[index] = 0
            else:
                final_signal[index] = -1


        #### TEST ######
        # output.to_pickle('pip_result')
        #
        # test = pd.DataFrame(index=final_signal.index)
        # test['weighted Signal'] = weighted_signal
        # test['final Signal'] = final_signal
        # test.to_pickle('test_signal')

        print('before trading ran')

    def run(self):
        START = pd.Timestamp("2015-02-10", tz="EST")
        END = pd.Timestamp("2015-03-01", tz="EST")
        self.result = run_algorithm(start=START, end=END,
                                    initialize=self.initialize,
                                    before_trading_start=self.before_trading_start,
                                    capital_base=10000,
                                    handle_data=self.handle_data,
                                    bundle='quantopian-quandl')


        self.result.to_csv('Trading_result')