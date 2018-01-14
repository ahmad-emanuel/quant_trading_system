import numpy as np
from zipline.pipeline import CustomFactor
from zipline.pipeline.data import USEquityPricing

class ADX(CustomFactor):
    """
    Average Directional Movement Index

    Momentum indicator. Smoothed DX

    **Default Inputs:** USEquityPricing.high, USEquityPricing.low, USEquitypricing.close

    **Default Window Length:** 29

    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/DMI
    """
    inputs = [USEquityPricing.high, USEquityPricing.low, USEquityPricing.close]
    window_length = 29

    def compute(self, today, assets, out, high, low, close):

        # positive directional index
        plus_di = 100 * np.cumsum(plus_dm_helper(high, low) / trange_helper(high, low, close), axis=0)

        # negative directional index
        minus_di = 100 * np.cumsum(minus_dm_helper(high, low) / trange_helper(high, low, close), axis=0)

        # full dx with 15 day burn-in period
        dx_frame = (np.abs(plus_di - minus_di) / (plus_di + minus_di) * 100.)[14:]

        # 14-day EMA
        span = 14
        decay_rate = 2. / (span + 1.)
        weights = np.full(span, decay_rate, float) ** np.arange(span + 1, 1, -1)

        # return EMA
        out[:] = np.average(dx_frame, axis=0, weights=weights)


"""
HELPER FUNCTIONS
"""


def plus_dm_helper(high, low):
    """
    Returns positive directional movement. Abstracted for use with more complex factors

    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/DMI

    Parameters
    ----------
    high : np.array
        matrix of high prices
    low : np.array
        matrix of low prices

    Returns
    -------
    np.array : matrix of positive directional movement

    """
    # get daily differences between high prices
    high_diff = (high - np.roll(high, 1, axis=0))[1:]

    # get daily differences between low prices
    low_diff = (np.roll(low, 1, axis=0) - low)[1:]

    # matrix of positive directional movement
    return np.where(((high_diff > 0) | (low_diff > 0)) & (high_diff > low_diff), high_diff, 0.)

def minus_dm_helper(high, low):
    """
    Returns negative directional movement. Abstracted for use with more complex factors

    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/DMI

    Parameters
    ----------
    high : np.array
        matrix of high prices
    low : np.array
        matrix of low prices

    Returns
    -------
    np.array : matrix of negative directional movement

    """
    # get daily differences between high prices
    high_diff = (high - np.roll(high, 1, axis=0))[1:]

    # get daily differences between low prices
    low_diff = (np.roll(low, 1, axis=0) - low)[1:]

    # matrix of megative directional movement
    return np.where(((high_diff > 0) | (low_diff > 0)) & (high_diff < low_diff), low_diff, 0.)


def trange_helper(high, low, close):
    """
    Returns true range

    http://www.macroption.com/true-range/

    Parameters
    ----------
    high : np.array
        matrix of high prices
    low : np.array
        matrix of low prices
    close: np.array
        matrix of close prices

    Returns
    -------
    np.array : matrix of true range

    """
    # define matrices to be compared
    close = close[:-1]
    high = high[1:]
    low = low[1:]

    # matrices for comparison
    high_less_close = high - close
    close_less_low = close - low
    high_less_low = high - low

    # return maximum value for each cel
    return np.maximum(high_less_close, close_less_low, high_less_low)