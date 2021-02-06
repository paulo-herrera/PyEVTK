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
from evtk.hl import linesToVTK
import numpy as np

FILE_PATH = "./lines"
def clean():
    try:
        os.remove(FILE_PATH + ".vtu")
    except:
        pass
        
def run():
    print("Running lines...")
    npoints = 4
    x = np.zeros(npoints)
    y = np.zeros(npoints)
    z = np.zeros(npoints)
    pressure = np.random.rand(npoints)
    temp = np.random.rand(npoints)
    vel = np.zeros(2)
    vel[0] = 1.0
    vel[1] = 5.0

    x[0], y[0], z[0] = 0.0, 0.0, 0.0
    x[1], y[1], z[1] = 1.0, 1.0, 1.0
    x[2], y[2], z[2] = 0.0, 0.0, 0.0
    x[3], y[3], z[3] = -1.0, 1.0, 1.0

    comments = [ "comment 1", "comment 2" ]
    linesToVTK(FILE_PATH, x, y, z, cellData = {"vel" : vel}, pointData = {"temp" : temp, "pressure" : pressure}, comments = comments)

if __name__ == "__main__":
    run()

