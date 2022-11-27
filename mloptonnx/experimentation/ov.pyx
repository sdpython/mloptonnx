"""
@file
@brief Direct calls to libraries :epkg:`BLAS` and :epkg:`LAPACK`.
"""
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
    

cdef void initialize():
    """
    Initializes :epkg:`onnxruntime` C API.
    """
    OrtInitialize()
