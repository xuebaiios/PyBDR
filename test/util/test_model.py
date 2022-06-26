import inspect

import numpy as np

from pyrat.model import ModelNEW
from pyrat.model import Model
from sympy import *


def test_fx():
    def f(x):
        dxdt = [None] * 6

        dxdt[0] = (0.5 - 9.963e-6 * x[0] * x[4] - 1.925e-5 * x[0]) * 3600
        dxdt[1] = (
            1.5e-3 + 1.5e-2 * (x[0] ** 2 / (547600 + x[0] ** 2)) - 8e-4 * x[1]
        ) * 3600
        dxdt[2] = (8e-4 * x[1] - 1.444e-4 * x[2]) * 3600
        dxdt[3] = (1.66e-2 * x[2] - 9e-4 * x[3]) * 3600
        dxdt[4] = (9e-4 * x[3] - 1.66e-7 * x[3] * 2 - 9.963e-6 * x[4] * x[5]) * 3600
        dxdt[5] = (0.5 - 3.209e-5 * x[5] - 9.963e-6 * x[4] * x[5]) * 3600

        return Matrix(dxdt)

    x = symbols("x:6")
    model = ModelNEW(f(x), x)
    print()
    print(model)


def test_fxu():
    import pyrat.util.functional.auxiliary as aux

    def f(x, u):
        # parameters
        k0, k1, g = 0.015, 0.01, 9.81
        # dynamic
        dxdt = [None] * 6

        dxdt[0] = u[0] + 0.1 + k1 * (4 - x[5]) - k0 * sqrt(2 * g) * sqrt(x[0])
        dxdt[1] = k0 * sqrt(2 * g) * (sqrt(x[0]) - sqrt(x[1]))
        dxdt[2] = k0 * sqrt(2 * g) * (sqrt(x[1]) - sqrt(x[2]))
        dxdt[3] = k0 * sqrt(2 * g) * (sqrt(x[2]) - sqrt(x[3]))
        dxdt[4] = k0 * sqrt(2 * g) * (sqrt(x[3]) - sqrt(x[4]))
        dxdt[5] = k0 * sqrt(2 * g) * (sqrt(x[4]) - sqrt(x[5]))
        return Matrix(dxdt)

    modelref = Model(f, [6, 1])
    start = aux.performance_counter_start()

    x, u = np.random.rand(6), np.random.rand(1)
    start = aux.performance_counter(start, "xu")
    pre_temp = modelref.evaluate((x, u), "numpy", 3, 1)
    start = aux.performance_counter(start, "pre_temp")
    suc_temp = modelref.evaluate((x, u), "numpy", 3, 0)
    print(suc_temp.shape)
    start = aux.performance_counter(start, "suc_temp")
    tt = modelref.evaluate((x, u), "numpy", 0, 0)
    print(tt.shape)

    from pyrat.geometry import Interval

    x, u = Interval.rand(6), Interval.rand(1)

    temp0 = modelref.evaluate((x, u), "interval", 3, 0)
    start = aux.performance_counter(start, "modref1")
    temp1 = modelref.evaluate((x, u), "interval", 2, 0)
    start = aux.performance_counter(start, "modref2")
    temp2 = modelref.evaluate((x, u), "interval", 2, 0)
    start = aux.performance_counter(start, "modref3")
    temp3 = modelref.evaluate((x, u), "interval", 0, 1)
    print(temp0.dim)
    print(temp1.dim)
    print(temp2.dim)
    print(temp3.dim)
