"""
@brief      test log(time=2s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase


class TestOv(ExtTestCase):

    def test_initialize(self):
        from mloptonnx.experimentation.ov import initialize  # pylint: disable=E0611
        initialize()


if __name__ == "__main__":
    unittest.main()
