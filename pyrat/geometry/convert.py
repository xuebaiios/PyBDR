from __future__ import annotations

import numpy as np

from .geometry import Geometry
from .interval import Interval
from .zonotope import Zonotope


def _interval2zonotope(source: Interval):
    raise NotImplementedError  # TODO


def _zonotope2interval(source: Zonotope):
    """
    over approximate a zonotope by an interval
    :param source: given zonotope
    :return:
    """
    c = source.c
    # determine left and right limit, specially designed for high performance
    delta = np.sum(abs(source.z), axis=1) - abs(c)
    left_limit = c - delta
    right_limit = c + delta
    return Interval(left_limit, right_limit)


def cvt2(source, target: Geometry.TYPE):
    if source.type == Geometry.TYPE.INTERVAL and target == Geometry.TYPE.INTERVAL:
        return source
    elif source.type == Geometry.TYPE.INTERVAL and target == Geometry.TYPE.ZONOTOPE:
        return _interval2zonotope(source)
    elif source.type == Geometry.TYPE.ZONOTOPE and target == Geometry.TYPE.INTERVAL:
        return _zonotope2interval(source)
    elif source.type == Geometry.TYPE.ZONOTOPE and target == Geometry.TYPE.ZONOTOPE:
        return source
    else:
        raise NotImplementedError
