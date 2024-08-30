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
# * Example of how to use the high level imageToVTK function.  *
# **************************************************************
import os
from evtk.hl import imageToVTK
import numpy as np

FILE_PATH = "./image"
def clean():
    try:
        os.remove(FILE_PATH + ".vti")
    except:
        pass
        
def run():
    print("Running image...")

    # Grid dimensions
    origin  = (0.0, 0.0 , 0.0)
    spacing = (1.0, 1.0, 1.0)

    # Dimensions
    nx, ny, nz = 6, 6, 2
    ncells = nx * ny * nz
    npoints = (nx + 1) * (ny + 1) * (nz + 1)

    # Variables
    pressure = np.random.rand(ncells).reshape( (nx, ny, nz), order = 'C')
    temp = np.random.rand(npoints).reshape( (nx + 1, ny + 1, nz + 1))

    comments = [ "comment 1", "comment 2" ]
    imageToVTK(FILE_PATH, origin, spacing, cellData = {"pressure" : pressure}, pointData = {"temp" : temp}, comments = comments )

if __name__ == "__main__":
    run()

