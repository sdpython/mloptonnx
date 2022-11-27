"""

.. _l-example-add_eye_inplace:

======================
numpyx.add_eye_inplace
======================

Simple benchmark to show that custom code may be faster.
The goal is to add the matrix identity inplace.

.. contents::
    :local:

Discrepancies
============
"""
import time
from numpy.testing import assert_allclose
import numpy
from pandas import DataFrame
import matplotlib.pyplot as plt
from mloptonnx.experimentation.numpyx import add_eye_inplace
from tqdm import tqdm


m = numpy.random.randn(4, 4).astype(numpy.float64) * 0
m1 = m + numpy.identity(m.shape[0])
add_eye_inplace(m)

assert_allclose(m1, m)

##################################
# Everything works fine. Let's benchmark it.
#
# Benchmark
# =========


repeat = 100
data = []
for i in tqdm([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]):
    M = numpy.random.randn(i, i).astype(numpy.float64)
    begin = time.perf_counter()
    for _ in range(repeat):
        M += numpy.identity(i)
    end = time.perf_counter() - begin
    
    obs = {'N': i, 'time_numpy': end}

    begin = time.perf_counter()
    for _ in range(repeat):
        add_eye_inplace(M)
    end = time.perf_counter() - begin
    
    obs.update({'time_add_eye_inplace': end})
    data.append(obs)

df = DataFrame(data).set_index('N')
df


#####################################
# Graphs
# ======


fig, ax = plt.subplots(1, 2, figsize=(10, 4))
df.plot(ax=ax[0], title="add_eye_inplace", logy=True, logx=True)
df["ratio"] = df["time_add_eye_inplace"] / df["time_numpy"]
df[["ratio"]].plot(ax=ax[1], title="ratio, lower is better", logx=True)

######################################
# A custom function may be worth implementing where the operator
# to do does not involve contiguous portions of arrays.

plt.show()
