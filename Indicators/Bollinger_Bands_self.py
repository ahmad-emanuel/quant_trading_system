from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
import numpy as np


class BollingerBands(CustomFactor):
    """
    Bollinger Bands technical indicator.

    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.close`

    Parameters
    ----------
    inputs : length-1 iterable[BoundColumn]
        The expression over which to compute bollinger bands.
    window_length : int > 0
        Length of the lookback window over which to compute the bollinger
        bands.
    k : float
        The number of standard deviations to add or subtract to create the
        upper and lower bands.
    """
    params = ('k',)
    inputs = (USEquityPricing.close,)
    window_length = 20 + 1
    outputs = 'lower_t_1', 'middle_t_1', 'upper_t_1', 'lower_t', 'middle_t', 'upper_t'

    def compute(self, today, assets, out, close, k):
        difference_t = k * np.nanstd(close[-1:0:-1], axis=0)

        out.middle_t = middl = np.nanmean(close[-1:0:-1], axis=0)
        out.upper_t = middl + difference_t
        out.lower_t = middl - difference_t

        difference_t_1 = k * np.nanstd(close[-2::-1], axis=0)

        out.middle_t_1 = middle = np.nanmean(close[-2::-1], axis=0)
        out.upper_t_1 = middle + difference_t_1
        out.lower_t_1 = middle - difference_t_1