from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
import numpy as np


def recurs_sum(arr):
    arr_sum = np.zeros(arr.shape)
    arr_sum[0] = arr[0]

    for i in range(1, len(arr)):
        arr_sum[i] = arr_sum[i-1]+arr[i]

    return arr_sum


class AD(CustomFactor):
    """
    Chaikin Accumulation Distribution Oscillator

    Volume indicator

    **Default Inputs:** USEquityPricing.high, USEquityPricing.low, USEquitypricing.close, USEquityPricing.volume

    **Default Window Length:** 14

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:accumulation_distribution_line
    """
    inputs = [USEquityPricing.close, USEquityPricing.high, USEquityPricing.low, USEquityPricing.volume]
    window_length = 14 + 1
    outputs = 'cho_yesterday', 'AD_yesterday', 'cho_today', 'AD_today'

    def compute(self, today, assets, out, close, high, low, vol):
        # close location value
        clv = ((close - low) - (high - close)) / (high - low)
        ad = clv * vol

        # today
        ad_revised = recurs_sum(ad[-14:])

        sma_3d = np.nanmean(ad_revised[-3:], axis=0)
        sma_10d = np.nanmean(ad_revised[-10:], axis=0)

        cho_today = sma_3d - sma_10d

        out.cho_today[:] = cho_today
        out.AD_today[:] = ad_revised[-1]

        # yesterday
        ad_revised = recurs_sum(ad[:14])

        sma_3d = np.nanmean(ad_revised[-3:], axis=0)
        sma_10d = np.nanmean(ad_revised[-10:], axis=0)

        cho_yesterday = sma_3d - sma_10d

        out.cho_yesterday[:] = cho_yesterday
        out.AD_yesterday[:] = ad_revised[-1]
