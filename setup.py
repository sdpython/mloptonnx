# -*- coding: utf-8 -*-
import sys
import os
import platform
import warnings
from setuptools import setup, Extension, find_packages
from pyquicksetup import read_version, read_readme, default_cmdclass

#########
# settings
#########

project_var_name = "mloptonnx"
versionPython = f"{sys.version_info.major}.{sys.version_info.minor}"
path = "Lib/site-packages/" + project_var_name
readme = 'README.rst'
history = "HISTORY.rst"
requirements = None

KEYWORDS = [project_var_name, 'Xavier Dupré', 'ONNX', 'onnxruntime']
DESCRIPTION = """Experimentation around ONNX."""
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering',
    'Topic :: Education',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable'
]


#######
# data
#######

packages = find_packages()
package_dir = {k: os.path.join('.', k.replace(".", "/")) for k in packages}
package_data = {
    project_var_name + ".experimentation": [
        "*.cpp", "*.hpp", "*.pyx", "*.pyd", "*.h", "*.dll", "*.so"],
    project_var_name + ".experimentation.onnxruntime": ["*.*"],
    project_var_name + ".experimentation.onnxruntime.include": ["*.*"],
    project_var_name + ".experimentation.onnxruntime.lib": ["*.*"],
}


def get_compile_args():

    if sys.platform.startswith("win"):
        libraries_thread = ['kernel32']
        extra_compile_args_thread = None
        extra_compile_args_numbers = ['/EHsc', '/O2', '/Gy', '/openmp']
        extra_compile_args_bench = extra_compile_args_numbers.copy()
        extra_link_args = None
        define_macros = [('USE_OPENMP', None)]
    elif sys.platform.startswith("darwin"):
        # see https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/_build_utils/openmp_helpers.py#L30
        # export CPPFLAGS="$CPPFLAGS -Xpreprocessor -fopenmp"
        # export CFLAGS="$CFLAGS -I/usr/local/opt/libomp/include"
        # export CXXFLAGS="$CXXFLAGS -I/usr/local/opt/libomp/include"
        # export LDFLAGS="$LDFLAGS -Wl,-rpath,/usr/local/opt/libomp/lib
        #                          -L/usr/local/opt/libomp/lib -lomp"
        libraries_thread = None
        extra_compile_args_thread = ['-lpthread', '-stdlib=libc++', '-std=c++11',
                                     '-mmacosx-version-min=10.7', '-fpermissive',
                                     '-Xpreprocessor']
        extra_compile_args_thread.append('-fopenmp')

        extra_compile_args_numbers = ['-stdlib=libc++', '-mmacosx-version-min=10.7',
                                      '-std=c++11', '-fpermissive', '-Xpreprocessor']
        extra_compile_args_numbers.append('-fopenmp')

        extra_compile_args_bench = extra_compile_args_numbers.copy()
        extra_link_args = ["-lomp"]
        define_macros = [('USE_OPENMP', None)]
    else:
        libraries_thread = None
        extra_compile_args_thread = ['-lpthread', '-fopenmp', '-std=c++11']
        # option -mavx512f enable AVX 512 instructions
        # see https://blog.qiqitori.com/?p=390
        # , '-o2', '-mavx512f']
        extra_compile_args_numbers = ['-fopenmp', '-std=c++11']
        extra_compile_args_bench = extra_compile_args_numbers.copy()
        extra_link_args = ['-lgomp']
        define_macros = [('USE_OPENMP', None)]
    return (libraries_thread, extra_compile_args_numbers,
            extra_compile_args_bench, extra_compile_args_thread,
            extra_link_args, define_macros)


def get_extensions():
    import numpy
    this = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(os.path.dirname(__file__))
    (libraries_thread, extra_compile_args_numbers,
     extra_compile_args_bench, extra_compile_args_thread,
     extra_link_args, define_macros) = get_compile_args()

    name = 'numpyx'
    ext_numpyx = Extension(
        f"mloptonnx.experimentation.{name}",
        [f'mloptonnx/experimentation/{name}.pyx'],
        include_dirs=[numpy.get_include()],
        # extra_compile_args=["-O3"],
        define_macros=define_macros,
        language="c++")

    name = 'ov'
    ext_numpyx = Extension(
        f"mloptonnx.experimentation.{name}",
        [f'mloptonnx/experimentation/{name}.pyx',
         'mloptonnx/experimentation/ort_interface.cpp'],
        include_dirs=[
            numpy.get_include(),
            'mloptonnx/experimentation',
            'mloptonnx/experimentation/onnxruntime/include',
        ],
        libraries=[
            os.path.join(this, 'mloptonnx', 'experimentation', 'onnxruntime', 'lib', '*.so*'),
        ],
        # extra_compile_args=["-O3"],
        define_macros=define_macros,
        language="c++")

    # cythonize

    opts = dict(boundscheck=False, cdivision=True,
                wraparound=False, language_level=3,
                cdivision_warnings=True)

    try:
        from Cython.Build import cythonize
        ext_modules = cythonize([
            ext_numpyx,
        ], compiler_directives=opts)
    except ImportError:
        # Cython is not installed.
        warnings.warn(
            "cython is not installed. Only pure python subpckages will be available.")
        ext_modules = None

    return ext_modules


try:
    ext_modules = get_extensions()
except ImportError as e:
    warnings.warn(
        f"Unable to build C++ extension with missing dependencies {e!r}.")
    ext_modules = None


setup(
    name=project_var_name,
    ext_modules=ext_modules,
    version=read_version(__file__, project_var_name),
    author='Xavier Dupré',
    author_email='xavier.dupre@gmail.com',
    license="MIT",
    url="http://www.xavierdupre.fr/app/mloptonnx/helpsphinx/index.html",
    download_url="https://github.com/sdpython/mloptonnx/",
    description=DESCRIPTION,
    long_description=read_readme(__file__),
    cmdclass=default_cmdclass(),
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    setup_requires=["cython", "numpy"],
    install_requires=["numpy>=1.23", "cython", "onnx"],
)
