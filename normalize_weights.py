import numpy as np


def normalize_weights(weights):

    long = 0.0
    short = 0.0

    for w in weights.values():
        if w>0:
            long = long + w
        elif w<0:
            short = short + w

    # we go long (short) with 0.5 (half) of capital base
    long = long * 2
    short = short * 2

    for key, value in weights.items():
        if value>0:
            weights[key] = value / long
        elif value<0:
            weights[key] = value / abs(short)

    return weights