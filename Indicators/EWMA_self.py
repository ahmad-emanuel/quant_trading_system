from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
import pandas as pd
import warnings


class EWMA(CustomFactor):
    """
    exponentially weighted moving average of latest close price of two days
    **Default Inputs:** USEquityPricing.close
     **Default Window Length:** 38
     span = 7 (one week)
    """

    inputs = (USEquityPricing.close,)
    window_length = 38 + 1
    outputs = 'yesterday','today'

    def compute(self, today, assets, out, close):

        # ignore unimportant future version warnings
        warnings.filterwarnings('ignore')

        temp = pd.ewma(close, span=7)
        out.today[:] = temp[-1]
        out.yesterday[:] = temp[-2]