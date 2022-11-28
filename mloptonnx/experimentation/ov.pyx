"""
@file
@brief cython + onnxruntime.
"""
from ctypes import cdll
import sys
from libc.stdlib cimport calloc, free
from libc.string cimport memcpy
from libc.stdio cimport printf
from libc.math cimport NAN

import numpy
cimport numpy
from numpy cimport int64_t
cimport cython
numpy.import_array()


cdef extern from "ort_interface.h":
    
    cdef void OrtInitialize()
    

def initialize():
    """
    Initializes :epkg:`onnxruntime` C API.
    """
    if sys.platform == "win32":
        cdll.LoadLibrary("onnxruntime.dll")
    else:
        cdll.LoadLibrary("onnxruntime.so")
    OrtInitialize()
