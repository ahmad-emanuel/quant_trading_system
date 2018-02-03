import numpy as np
from zipline.pipeline import CustomFactor
from zipline.pipeline.data import USEquityPricing


class CCI(CustomFactor):
    """
        Commodity Channel Index

        Momentum indicator

        **Default Inputs:** USEquityPricing.close, USEquityPricing.high, USEquityPricing.low
        **Default Window Length:** 14

        http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci
    """
    inputs = [USEquityPricing.high, USEquityPricing.low, USEquityPricing.close]
    window_length = 14 + 1
    outputs = ['CCI_t_1', 'CCI_t']

    def compute(self, today, assets, out, high, low, close):
        # typical price matrix
        typical_prices = (high + low + close) / 3.

        # mean of each column
        mean_typical_t = np.nanmean(typical_prices[-1:0:-1], axis=0)
        mean_typical_t_1 = np.nanmean(typical_prices[-2::-1], axis=0)

        # mean deviation
        mean_deviation_t = np.sum(
            np.abs(typical_prices[-1:0:-1] - np.tile(mean_typical_t, (len(typical_prices) - 1, 1))), axis=0) / (
                           self.window_length - 1)
        mean_deviation_t_1 = np.sum(
            np.abs(typical_prices[-2::-1] - np.tile(mean_typical_t_1, (len(typical_prices) - 1, 1))), axis=0) / (
                             self.window_length - 1)

        # CCI
        out.CCI_t[:] = (typical_prices[-1] - mean_typical_t) / (.015 * mean_deviation_t)
        out.CCI_t_1[:] = (typical_prices[-2] - mean_typical_t_1) / (.015 * mean_deviation_t_1)