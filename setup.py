# -*- coding: utf-8 -*-
import sys
import os
import platform
import tarfile
from urllib.request import urlopen
import warnings
import zipfile
from setuptools import setup, Extension, find_packages, Command
from setuptools.command.build_ext import build_ext
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
        "*.cpp", "*.hpp", "*.pyx", "*.pyd", "*.h", "*.dll",
        "*.so*", "*.cc", "*.dylib*"],
    project_var_name + ".experimentation.onnxruntime": [
        "*.txt", "*.md", "LICENSE", "VERSION_NUMBER", "GIT_COMMIT_ID"],
    project_var_name + ".experimentation.onnxruntime.include": ["*.h"],
    project_var_name + ".experimentation.onnxruntime.lib": [
        "*.dll", "*.so*", "*.dylib*"],
}


def get_compile_args():

    if sys.platform.startswith("win"):
        libraries_thread = ['kernel32']
        extra_compile_args = ['/EHsc', '/O2', '/Gy', '/openmp']
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
        extra_compile_args = ['-mmacosx-version-min=10.7', '-fopenmp',  # '-lpthread',
                              '-std=c++11', '-fpermissive', '-Xpreprocessor']
        extra_link_args = ["-lomp"]
        define_macros = [('USE_OPENMP', None)]
    else:
        libraries_thread = None
        extra_compile_args = ['-lpthread', '-fopenmp']
        extra_link_args = ['-lgomp']
        define_macros = [('USE_OPENMP', None)]
    return (libraries_thread, extra_compile_args,
            extra_link_args, define_macros)


def get_extensions():
    import numpy
    this = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(os.path.dirname(__file__))
    (libraries_thread, extra_compile_args,
     extra_link_args, define_macros) = get_compile_args()

    name = 'numpyx'
    ext_numpyx = Extension(
        f"mloptonnx.experimentation.{name}",
        [f'mloptonnx/experimentation/{name}.pyx'],
        include_dirs=[numpy.get_include()],
        # extra_compile_args=["-O3"],
        define_macros=define_macros,
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args)

    name = 'ort_wrapper'
    dirlib = os.path.join(this, 'mloptonnx', 'experimentation',
                          'onnxruntime', 'lib')
    dirinclude = os.path.join(this, 'mloptonnx', 'experimentation',
                              'onnxruntime', 'include')
    
    if sys.platform.startswith("win"):
        libraries = ["onnxruntime", "onnxruntime_providers_shared"]
    elif sys.platform == "darwin":
        libraries = ["onnxruntime"]
    else:
        libraries = ["onnxruntime"]

    ext_ov = Extension(
        f"mloptonnx.experimentation.{name}",
        [f'mloptonnx/experimentation/{name}.pyx',
         'mloptonnx/experimentation/ort_interface.cc'],
        include_dirs=[
            numpy.get_include(), dirinclude,
            os.path.join(this, 'mloptonnx', 'experimentation'),
        ],
        libraries=libraries,
        library_dirs=[dirlib],
        # extra_compile_args=["-O3"],
        define_macros=define_macros,
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args)

    # cythonize

    opts = dict(boundscheck=False, cdivision=True,
                wraparound=False, language_level=3,
                cdivision_warnings=True)

    try:
        from Cython.Build import cythonize
        ext_modules = cythonize([
            ext_numpyx,
            ext_ov,
        ], compiler_directives=opts)
    except ImportError:
        # Cython is not installed.
        warnings.warn(
            "cython is not installed. Only pure python subpckages will be available.")
        ext_modules = None

    return ext_modules


class build_ext_subclass(build_ext):

    def set_ORT_API_VERSION(self, version=10):
        filename = os.path.join("mloptonnx", "experimentation",
                                "onnxruntime", "include",
                                "onnxruntime_c_api.h")
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        modified = False
        for line in lines:
            if line.startswith("#define ORT_API_VERSION "):
                new_lines.append(f"#define ORT_API_VERSION {version}\n")
                modified = True
                continue
            new_lines.append(line)
        if not modified:
            raise RuntimeError(
                f"No line with '#define ORT_API_VERSION' was found in {filename!r}.")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("".join(new_lines))

    def build_extensions(self):
        from pyquickhelper.filehelper import synchronize_folder
        version = "1.13.1"
        dirbuild = "_build"
        if not os.path.exists(dirbuild):
            os.mkdir(dirbuild)
        dest = os.path.join("mloptonnx", "experimentation", "onnxruntime")
        if not os.path.exists(dest):
            os.mkdir(dest)

        if sys.platform.startswith("win"):
            # download
            url = (f"https://github.com/microsoft/onnxruntime/releases/download/"
                   f"v{version}/onnxruntime-win-x64-{version}.zip")
            name = url.split('/')[-1]
            filename = os.path.join(dirbuild, name)
            dirname = os.path.splitext(filename)[0]
            if not os.path.exists(filename):
                if self.verbose:
                    print(f"download {url!r}")
                with urlopen(url) as f:
                    with open(filename, "wb") as g:
                        g.write(f.read())
            if not os.path.exists(os.path.join(dest, "__init__.py")):
                # unzip
                if self.verbose:
                    print(f"unzip {filename!r}")
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall(dirbuild)                
                # copy                
                if self.verbose:
                    print(f"copy onnxruntime")
                    synchronize_folder(dirname, dest, fLOG=print)
                else:
                    synchronize_folder(dirname, dest)

        elif sys.platform.startswith("darwin"):
            url = (f"https://github.com/microsoft/onnxruntime/releases/download/"
                   f"v{version}/onnxruntime-osx-universal2-{version}.tgz")
            name = url.split('/')[-1]
            name = url.split('/')[-1]
            filename = os.path.join(dirbuild, name)
            dirname = os.path.splitext(filename)[0]
            if not os.path.exists(filename):
                if self.verbose:
                    print(f"download {url!r}")
                with urlopen(url) as f:
                    with open(filename, "wb") as g:
                        g.write(f.read())
            if not os.path.exists(os.path.join(dest, "__init__.py")):
                # untar
                if self.verbose:
                    print(f"untar {filename!r}")
                with tarfile.open(filename, 'r:gz') as f:
                    f.extractall(path=dirbuild)
                # copy
                if self.verbose:
                    print(f"copy onnxruntime")
                    synchronize_folder(dirname, dest, fLOG=print)
                else:
                    synchronize_folder(dirname, dest)

        else:
            from pyquickhelper.filehelper import synchronize_folder
            # download
            url = (f"https://github.com/microsoft/onnxruntime/releases/download/"
                   f"v{version}/onnxruntime-linux-x64-{version}.tgz")
            name = url.split('/')[-1]
            filename = os.path.join(dirbuild, name)
            dirname = os.path.splitext(filename)[0]
            if not os.path.exists(filename):
                if self.verbose:
                    print(f"download {url!r}")
                with urlopen(url) as f:
                    with open(filename, "wb") as g:
                        g.write(f.read())
            if not os.path.exists(os.path.join(dest, "__init__.py")):
                # untar
                if self.verbose:
                    print(f"untar {filename!r}")
                with tarfile.open(filename, 'r:gz') as f:
                    f.extractall(path=dirbuild)
                # copy
                if self.verbose:
                    print(f"copy onnxruntime")
                    synchronize_folder(dirname, dest, fLOG=print)
                else:
                    synchronize_folder(dirname, dest)

        # writing __init__.py
        if self.verbose:
            print("create __init__.py")
        for d in [
                os.path.join("mloptonnx", "experimentation", "onnxruntime"),
                os.path.join("mloptonnx", "experimentation", "onnxruntime", "lib"),
                os.path.join("mloptonnx", "experimentation", "onnxruntime", "include"),
            ]:
            name = os.path.join(d, "__init__.py")
            if self.verbose:
                print(f"create file {name!r}")
            with open(name, "w") as f:
                pass

        # fix ORT_API_VERSION
        if self.verbose:
            print("change ORT_API_VERSION")
        self.set_ORT_API_VERSION(10)

        # complete the build
        build_ext.build_extensions(self)

try:
    ext_modules = get_extensions()
except ImportError as e:
    warnings.warn(
        f"Unable to build C++ extension with missing dependencies {e!r}.")
    ext_modules = None


commands = default_cmdclass()
commands.update({'build_ext': build_ext_subclass})

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
    cmdclass=commands,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    setup_requires=["cython", "numpy"],
    install_requires=["numpy>=1.23", "cython", "onnx"],
)
