"""
@brief      test log(time=2s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
import numpy
from mloptonnx.experimentation.numpyx import (  # pylint: disable=E0611
    add_eye_inplace)


class TestNumpyx(ExtTestCase):

    def test_add_eye_inplace(self):
        m = numpy.random.randn(4, 4).astype(numpy.float64)
        expected = m + numpy.identity(4)
        add_eye_inplace(m)
        self.assertEqualArray(expected, m)


if __name__ == "__main__":
    unittest.main()
