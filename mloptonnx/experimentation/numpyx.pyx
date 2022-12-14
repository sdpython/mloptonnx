"""
@file
@brief Direct calls to libraries :epkg:`BLAS` and :epkg:`LAPACK`.
"""
# from libc.stdlib cimport calloc, free
# from libc.string cimport memcpy
# from libc.stdio cimport printf
# from libc.math cimport NAN
import numpy
cimport numpy
cimport cython
numpy.import_array()


@cython.boundscheck(False)
@cython.wraparound(False)
def add_eye_inplace(double[:, :] m):
    """
    Adds the identity matrix to a square matrix inplace.

    :param m: matrix
    :noreturn:
    """
    if m.shape[0] != m.shape[0]:
        raise ValueError(
            f"m is not a square matrix, its shape is {m.shape}.")

    cdef int i
    cdef int I = m.shape[0]
    with nogil:
        for i in range(0, I):
            m[i, i] += 1
