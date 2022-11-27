"""
@brief      test log(time=2s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
import numpy


class TestOv(ExtTestCase):

    def test_initialize(self):
        from mloptonnx.experimentation.ov import initialize
        initialize()


if __name__ == "__main__":
    unittest.main()
