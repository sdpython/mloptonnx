"""
@brief      test log(time=0s)
"""
import unittest
import io
from pyquickhelper.pycode import ExtTestCase
from mloptonnx import check


class TestCheck(ExtTestCase):

    def test_check(self):
        check()


if __name__ == "__main__":
    unittest.main()
