from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing


class Latest(CustomFactor):
    """
    latest close price of two days
    **Default Inputs:** USEquityPricing.close
     **Default Window Length:** 2
    """
    inputs = (USEquityPricing.close,)
    window_length = 2
    outputs = 'two_days_ago', 'yesterday'

    def compute(self, today, assets, out, close):
        out.yesterday = close[-1]
        out.two_days_ago = close[-2]