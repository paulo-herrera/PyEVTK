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
# * Example of how to use the high level pointsToVTK function. *
# **************************************************************
import os
from evtk.hl import polyLinesToVTK
import numpy as np

FILE_PATH = "poly_lines"
def clean():
    try:
        os.remove(FILE_PATH + ".vtu")
    except:
        pass
        
def run():
    # Positions of points that define lines
    npoints = 7
    x = np.zeros(npoints)
    y = np.zeros(npoints)
    z = np.zeros(npoints)

    # First line
    x[0], y[0], z[0] = 0.0, 0.0, 0.0
    x[1], y[1], z[1] = 1.0, 1.0, 0.0
    x[2], y[2], z[2] = 2.0, 0.0, 0.0
    x[3], y[3], z[3] = 3.0, -1.0, 0.0

    # Second line
    x[4], y[4], z[4] = 0.0, 0.0, 3.0
    x[5], y[5], z[5] = 1.0, 1.0, 3.0
    x[6], y[6], z[6] = 2.0, 0.0, 3.0

    # Connectivity of the lines
    pointsPerLine = np.zeros(2)
    pointsPerLine[0] = 4
    pointsPerLine[1] = 3

    # Some variables
    pressure = np.random.rand(npoints)
    temp = np.random.rand(npoints)
    vel = np.zeros(6)
    vel[0:3] = 1.0
    vel[4:6] = 5.0

    polyLinesToVTK(FILE_PATH, x, y, z, pointsPerLine = pointsPerLine, cellData = {"vel" : vel}, pointData = {"temp" : temp, "pressure" : pressure})

if __name__ == "__main__":
    run()
