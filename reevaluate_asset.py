import numpy as np


def reevaluate_pipeline(asset, weights):
    temp = np.zeros(9, dtype=np.int8)

    # reevaluate moving average convergence divergence
    if (asset.MACD[0] <= asset.MACD[1]) and (asset.MACD[2] >= asset.MACD[3]):
        temp[0] = 1
    elif (asset.MACD[0] >= asset.MACD[1]) and (asset.MACD[2] <= asset.MACD[3]):
        temp[0] = -1
    else:
        temp[0] = 0

    # reevaluate RSI
    if asset.RSI <= 30:
        temp[1] = 1
    elif asset.RSI >= 70:
        temp[1] = -1
    else:
        temp[1] = 0

    # reevaluate Exponentially weighted moving average
    if (asset.EWMA[0] >= asset['latest close'][0]) and (asset.EWMA[1] <= asset['latest close'][1]):
        temp[2] = 1
    elif (asset.EWMA[0] <= asset['latest close'][0]) and (asset.EWMA[1] >= asset['latest close'][1]):
        temp[2] = -1
    else:
        temp[2] = 0

    # reevaluate CCI
    if (asset['Commodity Channel Index'][0] <= -100.0) and (asset['Commodity Channel Index'][1] >= -100.0):
        temp[3] = 1
    elif (asset['Commodity Channel Index'][0] >= 100.0) and (asset['Commodity Channel Index'][1] <= 100.0):
        temp[3] = -1
    else:
        temp[3] = 0

    # reevaluate Bollinger Bands with the aid of latest close price
    if (asset['Bollinger Bands'][0] >= asset['latest close'][0]) and (
            asset['Bollinger Bands'][3] <= asset['latest close'][1]):
        temp[4] = 1
    elif (asset['Bollinger Bands'][2] <= asset['latest close'][0]) and (
            asset['Bollinger Bands'][5] >= asset['latest close'][1]):
        temp[4] = -1
    else:
        temp[4] = 0

    # reevaluate Stochastic Oscillator
    if (asset['Stochastic'][0] >= 20.) and (asset['Stochastic'][1] <= 20.):
        temp[5] = 1
    elif (asset['Stochastic'][0] <= 80.) and (asset['Stochastic'][1] >= 80.):
        temp[5] = -1
    else:
        temp[5] = 0

    # reevaluate Momentum indicator
    if (asset['Momentum'][0] <= 100.) and (asset['Momentum'][1] >= 100.):
        temp[6] = 1
    elif (asset['Momentum'][0] >= 100.) and (asset['Momentum'][1] <= 100.):
        temp[6] = -1
    else:
        temp[6] = 0

    # reevaluate Chaikin oscillator
    if (asset.CHO[0] <= 0) and (asset.CHO[2] >= 0):
        temp[7] = 1
    elif (asset.CHO[0] >= 0) and (asset.CHO[2] <= 0):
        temp[7] = -1
    else:
        temp[7] = 0

    # reevaluate Money flow index
    if asset.MFI <= 20:  # oversold
        temp[8] = 1
    elif asset.MFI >= 80:  # overbought
        temp[8] = -1
    else:
        temp[8] = 0

    return (temp * weights).sum()