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
from numpy cimport int64_t, int8_t, int16_t
cimport cython
numpy.import_array()


cdef extern from "ort_interface.h":
    
    cdef void OrtInitialize() except *
    cdef int _ORT_API_VERSION()

    cdef cppclass ApiDevice:
        int8_t type
        int8_t mem_type
        int16_t device_id
        ApiDevice()
        ApiDevice(int8_t, int8_t, int16_t)


cdef class Device:
    """
    Wraps :epkg:`C_OrtDevice`.

    :param t: device type
        (`CPU`, `GPU`, `FPGA`, `NPU`)
    :param mem_type: memory type
        (`DEFAULT`, `CUDA_PINNED`, `HIP_PINNED`, `CANN_PINNED`)
    :param device_id: device id
    """

    CPU = 0
    GPU = 1
    FPGA = 2
    NPU = 3

    DEFAULT = 0
    CUDA_PINNED = 1
    HIP_PINNED = 2
    CANN_PINNED = 3

    cdef ApiDevice device

    def __init__(self, t, mt, devid):
        self.device = ApiDevice(t, mt, devid)

    @property
    def type(self):
        return self.device.type

    @property
    def mem_type(self):
        return self.device.mem_type

    @property
    def device_id(self):
        return self.device.device_id


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


def ORT_API_VERSION():
    return _ORT_API_VERSION()
