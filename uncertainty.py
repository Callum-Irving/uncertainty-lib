import math
import numpy as np
import unittest

# Python module that provides utilities for working with uncertainty


class UncertainValue:
    """A Python float with uncertainty."""

    value: float
    uncertainty: float

    def __init__(self, value, uncertainty):
        self.value = float(value)
        self.uncertainty = float(uncertainty)

    def __repr__(self) -> str:
        return f"{self.value}±{self.uncertainty}"

    def __add__(self, other):
        if isinstance(other, UncertainValue):
            new_uncertainty = math.sqrt(self.uncertainty**2 + other.uncertainty**2)
            return UncertainValue(self.value + other.value, new_uncertainty)
        elif (
            isinstance(other, float)
            or isinstance(other, int)
            or isinstance(other, np.number)
        ):
            return UncertainValue(self.value + other, self.uncertainty)
        else:
            raise Exception("other must be an UncertaintyValue or number type")

    def __sub__(self, other):
        return self.__add__(other * -1)

    def __mul__(self, other):
        if isinstance(other, UncertainValue):
            product = self.value * other.value
            uncertainty = product * math.sqrt(
                (self.uncertainty / self.value) ** 2
                + (other.uncertainty / other.value) ** 2
            )
            return UncertainValue(product, uncertainty)
        elif (
            isinstance(other, float)
            or isinstance(other, int)
            or isinstance(other, np.number)
        ):
            product = self.value * other
            uncertainty = self.uncertainty * other
            return UncertainValue(product, uncertainty)
        else:
            raise Exception("other must be an UncertaintyValue or number type")

    def __truediv__(self, other):
        if isinstance(other, UncertainValue):
            quotient = self.value / other.value
            uncertainty = quotient * math.sqrt(
                (self.uncertainty / self.value) ** 2
                + (other.uncertainty / other.value) ** 2
            )
            return UncertainValue(quotient, uncertainty)
        elif (
            isinstance(other, float)
            or isinstance(other, int)
            or isinstance(other, np.number)
        ):
            quotient = self.value / other
            uncertainty = self.uncertainty / other
            return UncertainValue(quotient, uncertainty)
        else:
            raise Exception("other must be an UncertaintyValue or number type")


class TestUncertaintyValue(unittest.TestCase):

    EPSILON = 10e-12

    def float_equal(self, a, b):
        """
        Check if two floating point numbers are within self.EPSILON of each other.
        """
        return abs(a - b) < self.EPSILON

    def test_add(self):
        a = UncertainValue(1, 0.1)
        b = UncertainValue(2, 0.1)
        res = a + b
        self.assertTrue(self.float_equal(res.uncertainty, math.sqrt(2) * 0.1))

    def test_mul(self):
        a = UncertainValue(3.5, 3.5)
        b = UncertainValue(2, 2)
        res = a * b
        self.assertTrue(self.float_equal(res.value, 7))
        self.assertTrue(self.float_equal(res.uncertainty, 7 * math.sqrt(2)))


if __name__ == "__main__":
    unittest.main()
