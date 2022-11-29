"""
@brief      test log(time=4s)
"""
# pylint: disable=E0611
import os
import sys
from ctypes import cdll, CDLL
import unittest
from pyquickhelper.pycode import ExtTestCase


class TestOv(ExtTestCase):

    def test_dll(self):
        this = os.path.normpath(os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "..", "..", "mloptonnx",
            "experimentation")))
        if sys.platform == "win32":
            res = cdll.LoadLibrary("onnxruntime.dll")
        else:
            res = cdll.LoadLibrary(
                os.path.join(
                    this, "onnxruntime", "lib",
                    "libonnxruntime.so.1.13.1"))
        self.assertIsInstance(res, CDLL)
        self.assertNotEmpty(res.OrtGetApiBase)

    def test_ORT_API_VERSION(self):
        from mloptonnx.experimentation.ov import ORT_API_VERSION
        vers = ORT_API_VERSION()
        self.assertEqual(vers, 10)

    def test_initialize(self):
        from mloptonnx.experimentation.ov import initialize_onnxruntime
        initialize_onnxruntime()


if __name__ == "__main__":
    unittest.main(verbosity=2)
