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

    def test_a_dll(self):
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

    def test_a_initialize(self):
        from mloptonnx.experimentation.ort_wrapper import initialize_onnxruntime
        initialize_onnxruntime()

    def test_ort_api_version(self):
        from mloptonnx.experimentation.ort_wrapper import initialize_onnxruntime, ORT_API_VERSION
        initialize_onnxruntime()
        vers = ORT_API_VERSION()
        self.assertEqual(vers, 10)

    def test_ort_device(self):
        from mloptonnx.experimentation.ort_wrapper import Device
        d = Device(1, 2, 3)
        self.assertEqual(d.type, 1)
        self.assertEqual(d.mem_type, 2)
        self.assertEqual(d.device_id, 3)
        d = Device(Device.CPU, Device.DEFAULT, 0)
        self.assertEqual(d.type, 0)
        self.assertEqual(d.mem_type, 0)
        self.assertEqual(d.device_id, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
