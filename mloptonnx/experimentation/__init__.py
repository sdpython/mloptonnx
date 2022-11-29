"""
@file
@brief Shortcut to experimentation. Set `LD_LIBRARY_PATH`.
"""
import os
import sys


if "mloptonnx" not in os.environ.get("LD_LIBRARY_PATH", ""):
    sep = ";" if sys.platform == "win32" else ":"
    existing = os.environ.get("LD_LIBRARY_PATH", "")
    dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           "onnxruntime", "lib")
    os.environ["LD_LIBRARY_PATH"] = f"{existing}{sep}{dirname}"
    print("***", [os.environ["LD_LIBRARY_PATH"]])
