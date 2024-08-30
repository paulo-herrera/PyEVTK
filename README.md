# INTRODUCTION

EVTK (Export VTK) package allows exporting data to binary VTK files for
visualization and data analysis with any of the visualization packages that
support VTK files, e.g.  Paraview, VisIt and Mayavi. EVTK does not depend on any
external library (e.g. VTK), so it is easy to install in different systems.

Since version 0.9 the package is composed only of a set of pure Python files, hence
it is straightforwrd to install and run in any system where Python is installed.
EVTK provides low and high level interfaces.  While the low level interface 
can be used to export data that is stored in any type of container, the high 
level functions make easy to export data stored in Numpy arrays. Since version 1.3.1,
some of the high level functions that expect 1D list-type objects, e.g. pointsToVTK, 
accept list or tuples as input that are internally converted (copied) to Numpy arrays.

**NEW:** If you are a Java user or are interested in an alternative to Python, you
         can check JEVTK (https://github.com/paulo-herrera/JEVTK), 
         which is a Java version of EVTK.

# EXAMPLE

To export the topography of an open pit (excavation) given a set of x, y, z coordinates, use:

```
# Consider only x and y coordinates to create the triangulation
ndim = 2 
pointsToVTKAsTIN("./open_pit", x, y, z, ndim = ndim, data = {"1_temp" : temp}, comments = comments)
```

<a href="url"><img src="https://github.com/paulo-herrera/PyEVTK/blob/master/images/open_pit.png" align="center" height="400" width="550" ></a>


# INSTALLATION

Go to the source directory and type:

>>> python setup.py install


# DOCUMENTATION

This file together with the included examples in the examples directory in the
source tree provide enough information to start using the package.


# SUPPORTED GRIDS

PyEVTK supports all grid formats included in VTK. For example,

**Image:**

<a href="url"><img src="https://github.com/paulo-herrera/PyEVTK/blob/master/images/image_vti.png" align="center" height="400" width="550" ></a>

**Structured:**

<a href="url"><img src="https://github.com/paulo-herrera/PyEVTK/blob/master/images/structured_vts.png" align="center" height="400" width="550" ></a>

**Unstructured:**

<a href="url"><img src="https://github.com/paulo-herrera/PyEVTK/blob/master/images/unstructured_vtu.png" align="center" height="400" width="550" ></a>


# REQUIREMENTS

    - Numpy. Tested with Numpy 1.8.0 to 1.13.3.
    - Scipy only to export points as a triangular irregular network (TIN) [OPTIONAL].
      Tested with Scipy 1.2.

It is compatible with Python 3 (3.3+). 
Since version 0.9 it is only compatible with VTK 6.0 and newer versions.


# DEVELOPMENT

## DESIGN GUIDELINES:

The design of the package considered the following objectives:

1. Self-contained. The package does not require any external library with
the exception of Numpy, which is becoming a standard package in many Python
installations.

2. Flexibility. It is possible to use EVTK to export data stored in any
container and in any of the grid formats supported by VTK by using the low level
interface.

3. Easy of use. The high level interface makes very easy to export data stored
in Numpy arrays. The high level interface provides functions to export most of
the grids supported by VTK: image data, rectilinear and structured grids. It
also includes a function to export point sets and associated data that can be
used to export results from particle and meshless numerical simulations.

4. Performance. The aim of the package is to be used as a part of
post-processing tools. Thus, good performance is important to handle the results
of large simulations.  However, latest versions give priority to ease of installation
and use over performance.

## DEVELOPER NOTES:

It is useful to build and install the package to a temporary location without
touching the global python site-packages directory while developing. To do
this, while in the root directory, one can type:

    1. python setup.py build --debug install --prefix=./tmp
    2. export PYTHONPATH=./tmp/lib/python2.7/site-packages/:$PYTHONPATH

In more recent versions of Python, it may be better to use:

    1. python setup.py install --install-lib PATH_TO_DIR
    2. export PYTHONPATH=$PATH_TO_DIR:$PYTHONPATH
    
NOTE: you may have to change the Python version depending of the installed
version on your system.

To test the package after installation, go to the directory evtk/examples and type: 
>> python runall.py run

That should create several VTK files that can be imported into Paraview.
To delete all VTK files, type:
>> python runall.py clean

To generate distribution files (tar.gz and .whl files) in build directory:

    1. python setup.py sdist
    2. python setup.py bdist_wheel

## CONTRIBUTE:

I am open to incorporate bug fixes and additional improvements contributed by other
developers. As a non-native English speaker, I would also appreciate proof reading of
the this page and interesting pictures of grids exported using EVTK.

# SUPPORT:

I will continue releasing this package as open source, so it is free to be used 
in any kind of project. I will also continue providing support for simple questions 
and making incremental improvements as time allows. 

For further details, please contact me to: paulo.herrera.eirl@gmail.com.

**NOTE: PyEVTK moved to GitHub. The new official page is this one (https://github.com/paulo-herrera/PyEVTK)**
