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
# * Example of how to use the low level VtkFile class.         *
# **************************************************************
import os
from evtk.vtk import VtkFile, VtkRectilinearGrid
import numpy as np

FILE_PATH = "low_level"
def clean():
    try:
        os.remove(FILE_PATH + ".vtr")
    except:
        pass
        
def run():
    print("Running lowlevel...")

    nx, ny, nz = 6, 6, 2
    lx, ly, lz = 1.0, 1.0, 1.0
    dx, dy, dz = lx/nx, ly/ny, lz/nz
    ncells = nx * ny * nz
    npoints = (nx + 1) * (ny + 1) * (nz + 1)
    x = np.arange(0, lx + 0.1*dx, dx, dtype='float64')
    y = np.arange(0, ly + 0.1*dy, dy, dtype='float64')
    z = np.arange(0, lz + 0.1*dz, dz, dtype='float64')
    start, end = (0,0,0), (nx, ny, nz)

    w = VtkFile(FILE_PATH, VtkRectilinearGrid)
    w.openGrid(start = start, end = end)
    w.openPiece( start = start, end = end)

    # Point data
    temp = np.random.rand(npoints)
    vx = vy = vz = np.zeros([nx + 1, ny + 1, nz + 1], dtype="float64", order = 'F')
    w.openData("Point", scalars = "Temperature", vectors = "Velocity")
    w.addData("Temperature", temp)
    w.addData("Velocity", (vx,vy,vz))
    w.closeData("Point")

    # Cell data
    pressure = np.ones([nx, ny, nz], dtype="float64", order='F')
    w.openData("Cell", scalars = "Pressure")
    w.addData("Pressure", pressure)
    w.closeData("Cell")

    # Coordinates of cell vertices
    w.openElement("Coordinates")
    w.addData("x_coordinates", x);
    w.addData("y_coordinates", y);
    w.addData("z_coordinates", z);
    w.closeElement("Coordinates");

    w.closePiece()
    w.closeGrid()

    w.appendData(data = temp)
    w.appendData(data = (vx,vy,vz))
    w.appendData(data = pressure)
    w.appendData(x).appendData(y).appendData(z)
    w.save()

if __name__ == "__main__":
    run()

