from __future__ import annotations

import numbers

import numpy as np
from numpy.typing import ArrayLike
from scipy.sparse import csc_matrix, vstack

import pyrat.util.functional.auxiliary as aux
from .geometry import Geometry


class Interval(Geometry):
    def __init__(self, inf: ArrayLike, sup: ArrayLike):
        inf = csc_matrix([inf]) if isinstance(inf, numbers.Real) else csc_matrix(inf)
        sup = csc_matrix([sup]) if isinstance(sup, numbers.Real) else csc_matrix(sup)
        inf.eliminate_zeros()
        sup.eliminate_zeros()
        assert inf.shape == sup.shape
        assert inf.ndim <= 2
        assert (sup - inf).min() >= 0
        self._inf = inf
        self._sup = sup

    # =============================================== property
    @property
    def inf(self) -> csc_matrix:
        return self._inf

    @property
    def sup(self) -> csc_matrix:
        return self._sup

    @property
    def dim(self) -> tuple:
        return (-1) if self.is_empty else self.inf.shape

    @property
    def is_empty(self) -> bool:
        return aux.is_empty(self.inf) or aux.is_empty(self.sup)

    @property
    def is_scalar(self):
        if self.is_empty:
            return False
        return np.prod(self.dim) == 1

    @property
    def c(self) -> csc_matrix:
        assert not self.is_empty
        return (self._inf + self._sup) * 0.5

    @property
    def vertices(self) -> np.ndarray:
        raise NotImplementedError

    @property
    def info(self):
        raise NotImplementedError

    # =============================================== class method
    @classmethod
    def functions(cls):
        return {
            "__add__": cls.__add__,
            "__radd__": cls.__radd__,
            "__iadd__": cls.__iadd__,
            "__sub__": cls.__sub__,
            "__rsub__": cls.__rsub__,
            "__isub__": cls.__isub__,
            "__mul__": cls.__mul__,
            "__rmul__": cls.__rmul__,
            "__imul__": cls.__imul__,
            "__matmul__": cls.__matmul__,
            "__rmatmul__": cls.__rmatmul__,
            "__imatmul__": cls.__imatmul__,
            "__truediv__": cls.__truediv__,
            "__rtruediv__": cls.__rtruediv__,
            "__pow__": cls.__pow__,
            "__getitem__": cls.__getitem__,
            "__abs__": cls.__abs__,
            "__or__": cls.__or__,
            "__ror__": cls.__ror__,
            "__ior__": cls.__ior__,
            "sin": cls.sin,
            "cos": cls.cos,
            "asin": cls.asin,
            "acos": cls.acos,
            "asinh": cls.asinh,
            "acosh": cls.acosh,
            "tan": cls.tan,
            "tanh": cls.tanh,
            "sinh": cls.sinh,
            "cosh": cls.cosh,
            "atan": cls.atan,
            "atan2": cls.atan2,
            "exp": cls.exp,
            "sqrt": cls.sqrt,
        }

    # =============================================== operators
    def __contains__(self, item):
        raise NotImplementedError

    def __str__(self):
        return (
            "------------------------ Interval Info Begin ---------------------------\n"
            + str(self.dim)
            + "\n"
            + str(self.inf)
            + "\n"
            + str(self.sup)
            + "\n"
            + "------------------------ Interval Info End ---------------------------\n"
        )

    def __abs__(self):
        np_idx = (self.inf < 0).multiply(self.sup > 0)
        nn_idx = (self.inf < 0) > (self.sup > 0)

        inf, sup = self.inf, self.sup

        sup[np_idx] = csc_matrix(abs(self.inf[np_idx])).maximum(
            csc_matrix(abs(self.sup[np_idx]))
        )
        inf[np_idx] = 0

        sup[nn_idx] = abs(self.inf[nn_idx])
        inf[nn_idx] = abs(self.sup[nn_idx])

        return Interval(inf, sup)

    def __len__(self):
        raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, Interval):
            assert self.dim == other.dim
            return Interval(self.inf + other.inf, self.sup + other.sup)
        elif isinstance(other, (numbers.Real, np.ndarray)):
            return Interval(self.inf + other, self.sup + other)
        else:
            raise NotImplementedError

    def __radd__(self, other):
        return other + self

    def __iadd__(self, other):
        return self + other

    def __getitem__(self, item):
        assert isinstance(item, (int, ArrayLike))
        return Interval(self.inf[:, item], self.sup[:, item])

    def __setitem__(self, key, value):
        assert isinstance(key, (int, ArrayLike))
        assert isinstance(value, (numbers.Real, Interval, ArrayLike))
        if isinstance(value, Interval):
            self._inf[:, key] = value.inf
            self._sup[:, key] = value.sup
        elif isinstance(value, (numbers.Real, ArrayLike)):
            self._inf[:, key] = value
            self._sup[:, key] = value
        else:
            raise NotImplementedError

    def __matmul__(self, other):
        if isinstance(other, numbers.Real):
            return self * -1
        elif isinstance(other, (np.ndarray, list, tuple)):
            other = np.array(other) if isinstance(other, (list, tuple)) else other
            # TODO
            raise NotImplementedError
        elif isinstance(other, Interval):
            raise NotImplementedError  # TODO
        else:
            raise NotImplementedError

    def __rmatmul__(self, other):
        return self @ other

    def __imatmul__(self, other):
        return self @ other

    def __mul__(self, other):
        if isinstance(other, Interval):
            print(self.inf.shape, self.sup.shape)
            bd = vstack(
                [
                    self.inf.multiply(other.inf),
                    self.inf.multiply(other.sup),
                    self.sup.multiply(other.inf),
                    self.sup.multiply(other.sup),
                ]
            )
            inf = np.min(bd, axis=0)
            sup = np.max(bd, axis=0)
            return Interval(inf, sup)
        elif isinstance(other, (numbers.Real, np.ndarray, list, tuple)):
            other = np.array(other) if isinstance(other, (list, tuple)) else other
            inf = np.minimum(self.inf * other, self.sup * other)
            sup = np.maximum(self.inf * other, self.sup * other)
            return Interval(inf, sup)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return other * self

    def __imul__(self, other):
        return self * other

    def __pos__(self):
        return self

    def __neg__(self):
        return -1 * self

    def __or__(self, other):
        raise NotImplementedError

    def __ror__(self, other):
        raise NotImplementedError

    def __ior__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __rsub__(self, other):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __rtruediv__(self, other):
        raise NotImplementedError

    def __pow__(self, power, modulo=None):
        if self.is_scalar:
            if isinstance(power, numbers.Real):
                if abs(round(power) - power) <= np.finfo(np.float).eps:
                    if power >= 0:  # positive scalar integer exponent
                        temp0 = self.inf.power(power)
                        temp1 = self.sup.power(power)
                        inf = temp0.minimum(temp1)
                        sup = temp0.maximum(temp1)

                        # modification for even power
                        if power % 2 == 0 and power != 0:
                            ind = (inf < 0) + (sup > 0)
                            inf[ind] = 0
                        return Interval(inf, sup)
                    else:  # negative scalar integer power
                        return (1 / self) ** (-power)
                else:
                    if power >= 0:  # positive scalar real valued power
                        raise NotImplementedError
                    raise NotImplementedError
            elif isinstance(power, Interval):
                raise NotImplementedError
        else:
            raise NotImplementedError
        raise NotImplementedError

    # =============================================== public method
    def diag(self):
        assert not self.is_empty
        return Interval(np.diag(self.inf), np.diag(self.sup))

    def reduce(self, method: str, order: int):
        raise NotImplementedError

    def proj(self, dims):
        raise NotImplementedError

    # =============================================== static method

    @staticmethod
    def sin(x: Interval):
        raise NotImplementedError

    @staticmethod
    def cos(x: Interval):
        raise NotImplementedError

    @staticmethod
    def asin(x: Interval):
        raise NotImplementedError

    @staticmethod
    def acos(x: Interval):
        raise NotImplementedError

    @staticmethod
    def asinh(x: Interval):
        raise NotImplementedError

    @staticmethod
    def acosh(x: Interval):
        raise NotImplementedError

    @staticmethod
    def tan(x: Interval):
        raise NotImplementedError

    @staticmethod
    def tanh(x: Interval):
        raise NotImplementedError

    @staticmethod
    def sinh(x: Interval):
        raise NotImplementedError

    @staticmethod
    def cosh(x: Interval):
        raise NotImplementedError

    @staticmethod
    def atan(x: Interval):
        raise NotImplementedError

    @staticmethod
    def atan2(x: Interval):
        raise NotImplementedError

    @staticmethod
    def exp(x: Interval):
        raise NotImplementedError

    @staticmethod
    def sqrt(x: Interval):
        raise NotImplementedError

    @staticmethod
    def empty(dim: int):
        raise NotImplementedError

    @staticmethod
    def rand(dim: int):
        raise NotImplementedError
