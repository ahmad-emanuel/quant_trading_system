from zipline.pipeline.factors import CustomFactor
from zipline.pipeline.data import USEquityPricing
from zipline.utils.input_validation import expect_bounded
from numpy import average, full, arange
from zipline.utils.numpy_utils import float64_dtype, rolling_window
import pandas as pd

class MovingAverageConvergenceDivergence(CustomFactor):
    """
    Moving Average Convergence/Divergence (MACD) Signal line
    https://en.wikipedia.org/wiki/MACD

    A technical indicator originally developed by Gerald Appel in the late
    1970's. MACD shows the relationship between two moving averages and
    reveals changes in the strength, direction, momentum, and duration of a
    trend in a stock's price.

    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.close`

    Parameters
    ----------
    fast_period : int > 0, optional
        The window length for the "fast" EWMA. Default is 12.
    slow_period : int > 0, > fast_period, optional
        The window length for the "slow" EWMA. Default is 26.
    signal_period : int > 0, < fast_period, optional
        The window length for the signal line. Default is 9.

    Notes
    -----
    Unlike most pipeline expressions, this factor does not accept a
    ``window_length`` parameter. ``window_length`` is inferred from
    ``slow_period`` and ``signal_period``.
    """
    inputs = (USEquityPricing.close,)
    outputs = 'macd_yesterday','trigger_yesterday','macd_today','trigger_today'
    #outputs = 'MACD_yesterday','trigger_yesterday','MACD_today','trigger_today'
    # We don't use the default form of `params` here because we want to
    # dynamically calculate `window_length` from the period lengths in our
    # __new__.
    params = ('fast_period', 'slow_period', 'signal_period')

    @expect_bounded(
        __funcname='MACDSignal',
        fast_period=(1, None),  # These must all be >= 1.
        slow_period=(1, None),
        signal_period=(1, None),
    )
    def __new__(cls,
                fast_period=12,
                slow_period=26,
                signal_period=9,
                *args,
                **kwargs):

        if slow_period <= fast_period:
            raise ValueError(
                "'slow_period' must be greater than 'fast_period', but got\n"
                "slow_period={slow}, fast_period={fast}".format(
                    slow=slow_period,
                    fast=fast_period,
                )
            )

        return super(MovingAverageConvergenceDivergence, cls).__new__(
            cls,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
            window_length=slow_period + signal_period,      # extra one day for generate signal of yesterday
            *args, **kwargs
        )

    def _ewma(self, data, length):
        decay_rate = 1.0 - (2.0 / (1.0 + length))
        return average(
            data,
            axis=1,
            weights=exponential_weights(length, decay_rate)
        )

    def compute(self, today, assets, out, close, fast_period, slow_period,
                signal_period):

        ### today
        slow_EWMA_today = self._ewma(
            rolling_window(close[1:], slow_period),
            slow_period
        )

        fast_EWMA_today = self._ewma(
            rolling_window(close[1:], fast_period)[-signal_period:],
            fast_period
        )
        macd_today = fast_EWMA_today - slow_EWMA_today
        out.macd_today[:] = macd_today[-1]
        out.trigger_today[:] = self._ewma(macd_today.T, signal_period)

        ### yesterday
        slow_EWMA_yesterday = self._ewma(
            rolling_window(close[:-1], slow_period),
            slow_period
        )

        fast_EWMA_yesterday = self._ewma(
            rolling_window(close[:-1], fast_period)[-signal_period:],
            fast_period
        )
        macd_yesterday = fast_EWMA_yesterday - slow_EWMA_yesterday
        out.macd_yesterday[:] = macd_yesterday[-1]
        out.trigger_yesterday[:] = self._ewma(macd_yesterday.T, signal_period)



def exponential_weights(length, decay_rate):
    """
    Build a weight vector for an exponentially-weighted statistic.

    The resulting ndarray is of the form::

        [decay_rate ** length, ..., decay_rate ** 2, decay_rate]

    Parameters
    ----------
    length : int
        The length of the desired weight vector.
    decay_rate : float
        The rate at which entries in the weight vector increase or decrease.

    Returns
    -------
    weights : ndarray[float64]
    """
    return full(length, decay_rate, float64_dtype) ** arange(length + 1, 1, -1)