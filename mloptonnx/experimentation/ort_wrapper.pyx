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


#cdef extern from "onnxruntime_cxx_api.h":
#    
#    cdef cppclass OrtDevice:
#        
#        OrtDevice()
#        OrtDevice(int8_t, int8_t, int16_t)
#        int8_t Type()
#        int8_t MemType()
#        int16_t Id()


cdef extern from "ort_interface.h":
    
    cdef void OrtInitialize() except *
    cdef int _ORT_API_VERSION()


cdef class Device:
    """
    Wraps :epkg:`C_OrtDevice`.

    :param t: device type
    :param mem_type: memory type
    :param device_id: device id
    
    ::

      static const DeviceType CPU = 0;
      static const DeviceType GPU = 1;  // Nvidia or AMD
      static const DeviceType FPGA = 2;
      static const DeviceType NPU = 3;  // Ascend

      struct MemType {
        // Pre-defined memory types.
        static const MemoryType DEFAULT = 0;
        static const MemoryType CUDA_PINNED = 1;
        static const MemoryType HIP_PINNED = 2;
        static const MemoryType CANN_PINNED = 3;
      };    
    """

    cdef int8_t type_
    cdef int8_t mem_type_
    cdef int8_t device_id_
    
    def __init__(self, t, mem_type, device_id):
        self.type_ = t
        self.mem_type_ = mem_type
        self.device_id_ = device_id

    @property
    def type(self):
        return self.type_

    @property
    def mem_type(self):
        return self.mem_type_

    @property
    def device_id(self):
        return self.device_id_


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
