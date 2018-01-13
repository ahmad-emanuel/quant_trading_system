from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
import numpy as np
import warnings


class Stochastic(CustomFactor):
    """
    Stocahstic Oscillator
    non trend indicator
    **Default Inputs:** USEquityPricing.close, USEquityPricing.high, USEquityPricing.low
     **Default Window Length:** 5
    """
    inputs = [USEquityPricing.high, USEquityPricing.low, USEquityPricing.close]
    window_length = 5 + 1
    outputs = 'yesterday', 'today'

    def compute(self, today, assets, out, high, low, close):

        # ignore unimportant nan warnings
        warnings.filterwarnings('ignore')

        # tiefstes Tief der Periode für heute
        LL_t = np.nanmin(low[-1:0:-1], axis=0)

        # gestern
        LL_t_1 = np.nanmin(low[-2::-1], axis=0)

        # höchstes Hoch der Periode für heute
        HH_t = np.nanmax(high[-1:0:-1], axis=0)

        # gestern
        HH_t_1 = np.nanmax(high[-2::-1], axis=0)

        out.today = (close[-1] - LL_t) / (HH_t - LL_t) * 100
        out.yesterday = (close[-2] - LL_t_1) / (HH_t_1 - LL_t_1) * 100