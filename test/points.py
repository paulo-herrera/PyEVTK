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
from evtk.hl import pointsToVTK, pointsToVTKAsTIN
import numpy as np

FILE_PATH1 = "./rnd_points"
FILE_PATH2 = "./rnd_points_TIN"
FILE_PATH3 = "./line_points"
FILE_PATH4 = "./points_as_lists"
def clean():
    try:
        os.remove(FILE_PATH1 + ".vtu")
        os.remove(FILE_PATH2 + ".vtu")
        os.remove(FILE_PATH3 + ".vtu")
        os.remove(FILE_PATH4 + ".vtu")
    except:
        pass
    
def run():
    print("Running points...")
    
    # Example 1: Random points
    npoints = 100
    x = np.random.rand(npoints)
    y = np.random.rand(npoints)
    z = np.random.rand(npoints)
    pressure = np.random.rand(npoints)
    temp = np.random.rand(npoints)
    comments = [ "comment 1", "comment 2" ]

    # keys are sorted before exporting, hence it is useful to prefix a number to determine an order
    pointsToVTK(FILE_PATH1, x, y, z, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments) 

    # Example 2: Export as TIN
    ndim = 2 #only consider x, y coordinates to create the triangulation
    pointsToVTKAsTIN(FILE_PATH2, x, y, z, ndim = ndim, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments)

    # Example 3: Regular point set
    x = np.arange(1.0,10.0,0.1)
    y = np.arange(1.0,10.0,0.1)
    z = np.arange(1.0,10.0,0.1)

    comments = [ "comment 1", "comment 2" ]
    pointsToVTK(FILE_PATH3, x, y, z, data = {"elev" : z}, comments = comments)

    # Example 4: Point set of 5 points
    x = [0.0, 1.0, 0.5, 0.368, 0.4]
    y = [0.3, 2.0, 0.7, 0.1, 0.6]
    z = [1.0, 1.0, 0.3, 0.75, 0.9]
    pressure = [1.0, 2.0, 3.0, 4.0, 5.0]
    temp = [1.0, 2.0, 3.0, 4.0, 5.0]
    comments = [ "comment 1", "comment 2" ]

    # keys are sorted before exporting, hence it is useful to prefix a number to determine an order
    pointsToVTK(FILE_PATH4, x, y, z, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments) 

if __name__ == "__main__":
    run()
