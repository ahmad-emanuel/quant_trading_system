from zipline.pipeline import Pipeline
from zipline.api import attach_pipeline, pipeline_output
from zipline import run_algorithm
from zipline.pipeline.factors import MovingAverageConvergenceDivergenceSignal
import pandas as pd
# indicator
from Indicators.TEst_indicator import MFI


def make_pipeline():

    return Pipeline(
        columns={
            'MFI': MFI()
        }
    )


def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, "my_pipeline")


def handle_data(context, data):
    pass


def before_trading_start(context, data):
    # pandas Dataframe of pipeline Output
    context.output = pipeline_output("my_pipeline")

    # test
    #context.output.to_pickle('pip_result')
    print('before trading ran')
    exit()

#### run #####
START = pd.Timestamp("2015-02-10", tz="EST")
END = pd.Timestamp("2015-02-12", tz="EST")
result = run_algorithm(start=START, end=END,
                            initialize=initialize,
                            before_trading_start=before_trading_start,
                            capital_base=10000,
                            handle_data=handle_data,
                            bundle='quantopian-quandl')
