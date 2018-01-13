from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
import numpy as np
import pandas as pd


def up_or_down_func(arr):
    arr_pos_neg = np.zeros(arr.shape, dtype=np.int8)
    arr_pos_neg[0] = 0

    for i in range(1, len(arr)):
        for j in range(len(arr[i])):
            if arr[i, j] > arr[i - 1, j]:
                arr_pos_neg[i, j] = 1
            else:
                arr_pos_neg[i, j] = -1

    return arr_pos_neg


def pos_neg_money_flow(tp, up_or_down):
    pos_money_flow = np.zeros(len(tp[0]))
    neg_money_flow = np.zeros(len(tp[0]))

    for i in range(1, len(tp)):
        for j in range(len(tp[i])):
            if up_or_down[i,j] == 1:
                pos_money_flow[j] = pos_money_flow[j] + tp[i,j]
            else:
                neg_money_flow[j] = neg_money_flow[j] + tp[i,j]

    return pos_money_flow, neg_money_flow


class MFI(CustomFactor):
    """
   Money Flow Index (MFI)

    Volume indicator

    **Default Inputs:** USEquityPricing.high, USEquityPricing.low, USEquitypricing.close, USEquityPricing.volume

    **Default Window Length:** 14

    http://stockcharts.com/school/doku.php?st=money+flow&id=chart_school:technical_indicators:money_flow_index_mfi
    """
    inputs = [USEquityPricing.close, USEquityPricing.high, USEquityPricing.low, USEquityPricing.volume]
    window_length = 14 + 1

    def compute(self, today, assets, out, close, high, low, vol):
        # typical price
        tp = (high + low + close) / 3

        up_or_down = up_or_down_func(tp)

        tp = tp * vol

        # 14_period posetive and negative money flow
        pos_money_flow, neg_money_flow = pos_neg_money_flow(tp, up_or_down)

        ### test
        test1 = pos_money_flow + neg_money_flow
        test2 = np.sum(tp[-14:], axis=0)

        # Money Flow Ratio = (14-period Positive Money Flow) / (14-period Negative Money Flow)
        money_flow_ratio = pos_money_flow / neg_money_flow

        # Money Flow Index = 100 - 100/(1 + Money Flow Ratio)
        money_flow_index = 100 - (100 / (1 + money_flow_ratio))

        out[:] = money_flow_index
