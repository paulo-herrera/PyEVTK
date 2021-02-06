#! /usr/bin/env python

######################################################################################
# MIT License
# 
# Copyright (c) 2010-2021 Paulo A. Herrera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################

# **************************************************************
# * Example of how to use the high level gridToVTK function.   *
# * This example shows how to export a rectilinear grid.       *
# **************************************************************
import os
from evtk.hl import rectilinearToVTK
import numpy as np

FILE_PATH = "./rectilinear"
def clean():
    try:
        os.remove(FILE_PATH + ".vtr")
    except:
        pass
        
def run():
    print("Running rectilinear...")

    # Dimensions
    nx, ny, nz = 6, 6, 2
    lx, ly, lz = 1.0, 1.0, 1.0
    dx, dy, dz = lx/nx, ly/ny, lz/nz

    ncells = nx * ny * nz
    npoints = (nx + 1) * (ny + 1) * (nz + 1)

    # Coordinates
    x = np.arange(0, lx + 0.1*dx, dx, dtype='float64')
    y = np.arange(0, ly + 0.1*dy, dy, dtype='float64')
    z = np.arange(0, lz + 0.1*dz, dz, dtype='float64')

    # Variables
    pressure = np.random.rand(ncells).reshape( (nx, ny, nz))
    temp = np.random.rand(npoints).reshape( (nx + 1, ny + 1, nz + 1))

    comments = [ "comment 1", "comment 2" ]
    rectilinearToVTK(FILE_PATH, x, y, z, cellData = {"pressure" : pressure}, pointData = {"temp" : temp}, comments = comments)

if __name__ == "__main__":
    run()
