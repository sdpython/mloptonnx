"""
@file
@brief cython + onnxruntime.
"""
from ctypes import cdll
import os
import sys
# from libc.stdlib cimport calloc, free
# from libc.string cimport memcpy
# from libc.stdio cimport printf
# from libc.math cimport NAN

import numpy
cimport numpy
# from numpy cimport int64_t
cimport cython
numpy.import_array()


cdef extern from "ort_interface.h":
    
    cdef void OrtInitialize()
    

def initialize_onnxruntime():
    """
    Initializes :epkg:`onnxruntime` C API.
    """
    this = os.path.join(os.path.dirname(__file__))
    if sys.platform == "win32":
        cdll.LoadLibrary("onnxruntime.dll")
    else:
        cdll.LoadLibrary(os.path.join(this, "onnxruntime", "lib", "libonnxruntime.so"))
    OrtInitialize()
