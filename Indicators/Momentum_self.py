from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing


class Momentum(CustomFactor):
    """
    Momentum technical indicator
    non trend indicator
    **Default Inputs:** USEquityPricing.close
     **Default Window Length:** 20
    """
    inputs = (USEquityPricing.close,)
    window_length = 20 + 1
    outputs = 'yesterday', 'today'

    def compute(self, today, assets, out, close):
        out.today = (close[-1] / close[-20]) * 100
        out.yesterday = (close[-2] / close[-21]) * 100
