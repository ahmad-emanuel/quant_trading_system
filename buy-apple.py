from zipline.api import order, record, symbol
from zipline import run_algorithm
from zipline.pipeline import Pipeline
from zipline.api import attach_pipeline, pipeline_output
import pandas as pd


def make_pipeline():
    print("make_pipe_ran")
    return Pipeline(
    )

def initialize(context):
    my_pipe = make_pipeline()
    attach_pipeline(my_pipe, "my_pipeline")


def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))


def before_trading_start(context, data):
    print('before trading ran')
    context.output = pipeline_output("my_pipeline")


if __name__ == '__main__':
    START = pd.Timestamp("2015-01-01", tz="EST")
    END = pd.Timestamp("2015-03-03", tz="EST")
    result = run_algorithm(start=START, end=END,
                           initialize=initialize,
                           capital_base=10000,
                           handle_data=handle_data,
                           before_trading_start=before_trading_start,
                           bundle='quantopian-quandl')
    result.to_pickle('Zipline_result')