from sympy import *
from .model_old import ModelOld

"""
NOTE: 
Susuki, Y., Koo, T.J., Ebina, H., Yamazaki, T., Ochi, T., Uemura, T., Hikihara,
T.: A hybrid system approach to the analysis and design of power grid dynamic
performance. Proc. IEEE 100, 225–239 (2012)
"""


def _f(x, u):
    dxdt = [None] * 2

    dxdt[0] = x[1]
    dxdt[1] = 0.2 - 0.7 * sin(x[0]) - 0.05 * x[1]

    return Matrix(dxdt)


class SynchronousMachine(ModelOld):
    vars = symbols(("x:2", "u:1"))
    f = _f(*vars)
    name = "Synchronous Machine"
    dim = f.rows
